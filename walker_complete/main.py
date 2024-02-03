#importing libraries
from matplotlib import pyplot as plt
import numpy as np
import math
import scipy
from scipy import interpolate
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

#creating instance of parameters class with default values
class parameters:
    def __init__(self):
        self.g = 1 #acc due to gravity
        self.m = 0.5 #mass of each leg
        self.M = 1 #mass of main body
        self.I = 0.02 #moment of inertia 
        self.l = 1.0 #length of leg
        self.c = 0.5 #distance of hip joint to CoM of leg
        self.gam = 0.01 #slope of the ground 
        self.pause = 0.01 #pause function to be used during animation
        self.fps = 10 #frames per second

#uses matplotlib to visualise the arrays that we calculate further in the code
def animate(t,z,params):
    
    #interpolation so that animation is smooth
    data_pts = 1/params.fps
    t_interp = np.arange(t[0],t[len(t)-1],data_pts)
    [m,n] = np.shape(z)
    shape = (len(t_interp),n)
    z_interp = np.zeros(shape)

    for i in range(0,n):
        f = interpolate.interp1d(t, z[:,i])
        z_interp[:,i] = f(t_interp)

    l = params.l
    c = params.c

    min_xh = min(z[:,4]); max_xh = max(z[:,4]);
    dist_travelled = max_xh - min_xh;
    camera_rate = dist_travelled/len(t_interp);

    window_xmin = -1*l; window_xmax = 1*l;
    window_ymin = -0.1; window_ymax = 1.1*l;

    R1 = np.array([min_xh-l,0])
    R2 = np.array([max_xh+l,0])

    ramp, = plt.plot([R1[0], R2[0]],[R1[1], R2[1]],linewidth=5, color='black')
    #plot
    
    #animation loop
    for i in range(0,len(t_interp)):

        #extraction of relevant angles and positions
        theta1 = z_interp[i,0];
        theta2 = z_interp[i,2];
        xh = z_interp[i,4];
        yh = z_interp[i,5];

        H = np.array([xh, yh])
        C1 = np.array([xh+l*sin(theta1), yh-l*cos(theta1)])
        G1 = np.array([xh+c*sin(theta1), yh-c*cos(theta1)])
        C2 = np.array([xh+l*sin(theta1+theta2),yh-l*cos(theta1+theta2)])
        G2 = np.array([xh+c*sin(theta1+theta2),yh-c*cos(theta1+theta2)])

        #plotting of walker components using matplotlib
        hip, = plt.plot(H[0],H[1],color='black',marker='o',markersize=10)
        leg1, = plt.plot([H[0], C1[0]],[H[1], C1[1]],linewidth=5, color='red')
        leg2, = plt.plot([H[0], C2[0]],[H[1], C2[1]],linewidth=5, color='green')
        com1, = plt.plot(G1[0],G1[1],color='black',marker='o',markersize=5)
        com2, = plt.plot(G2[0],G2[1],color='black',marker='o',markersize=5)

        #adjustment of limits of plot window
        window_xmin = window_xmin + camera_rate;
        window_xmax = window_xmax + camera_rate;
        plt.xlim(window_xmin,window_xmax)
        plt.ylim(window_ymin,window_ymax)
        plt.gca().set_aspect('equal')

        #pause animation, clear previous points and reiterate
        plt.pause(params.pause)
        hip.remove()
        leg1.remove()
        leg2.remove()
        com1.remove()
        com2.remove()

    plt.close()
    
#calc of sin and cos angles
def sin(angle):
    return np.sin(angle)

def cos(angle):
    return np.cos(angle)

#calculation of a single step
def one_step(t0,z0,params):

    #solution of obtained algebraic equations using rk45 method predefined in the scipy library
    tf = t0+4;
    t = np.linspace(t0, tf, 1001)
    collision.terminal = True
    # contact.direction = -1
    # sol = solve_ivp(single_stance,[t0, tf],z0,method='RK45', t_eval=t, dense_output=True, \
    #         args=(params.M,params.m,params.I,params.l,params.c,params.g,params.gam))
    sol = solve_ivp(single_stance,[t0, tf],z0,method='RK45', t_eval=t, dense_output=True, \
                    events=collision, atol = 1e-13,rtol = 1e-12, args=(params.M,params.m,params.I,params.l,params.c,params.g,params.gam))


    #get solution at different time steps from sol.y
    [m,n] = np.shape(sol.y)
    shape = (n,m)
    t = sol.t
    z = np.zeros(shape)

    #get event from sol.y_events and exact time sol.t_events
    [mm,nn,pp] = np.shape(sol.y_events)
    tt_last_event = sol.t_events[mm-1]
    yy_last_event = sol.y_events[mm-1]

    #save data in z
    for i in range(0,m):
        z[:,i] = sol.y[i,:]

    #get state before footstrike using events
    t_end = tt_last_event[0]
    theta1 = yy_last_event[0,0]
    omega1 = yy_last_event[0,1]
    theta2 = yy_last_event[0,2]
    omega2 = yy_last_event[0,3]

    zminus = np.array([theta1, omega1, theta2, omega2 ])

    #return state after footstrike
    zplus = footstrike(t_end,zminus,params)

    #replace last entry in z and t
    t[n-1] = t_end
    z[n-1,0] = zplus[0];
    z[n-1,1] = zplus[1];
    z[n-1,2] = zplus[2];
    z[n-1,3] = zplus[3];


    return z,t

#calculation of n steps that we define, with help of the one_step function
def n_steps(t0,z0,params,steps):

    z = z0
    t = t0

    #initalise walker's position variables
    theta1 = z0[0];
    l = params.l
    xh = 0
    yh = l*cos(theta1)
    xh_start = xh

    #initialise array to store walker's state and position over time
    zz = np.append(z0,np.array([xh,yh]))

    #loop that performs specified number of steps 
    for i in range(0,steps):
        [z_temp,t_temp] = one_step(t0,z0,params)
        [mm,nn] = np.shape(z_temp)
        zz_temp = np.zeros( (mm,6))
        for j in range(0,mm):
            xh = xh_start + l*sin(z_temp[0,0])-l*sin(z_temp[j,0]);
            yh = l*cos(z_temp[j,0]);
            zz_temp[j,:] = np.append(z_temp[j,:],np.array([xh,yh]))
        xh_start = zz_temp[mm-2,4]
        if i==0:
            #z = np.concatenate(([z], z_temp[1:mm-1,:]), axis=0)
            t = np.concatenate(([t], t_temp[1:mm-1]), axis=0)
            zz = np.concatenate(([zz], zz_temp[1:mm-1,:]), axis=0)
        else:
            #z = np.concatenate((z, z_temp[1:mm-1,:]), axis=0)
            t = np.concatenate((t, t_temp[1:mm-1]), axis=0)
            zz = np.concatenate((zz, zz_temp[1:mm-1,:]), axis=0)
        theta1 = z_temp[mm-1,0]
        omega1 = z_temp[mm-1,1]
        theta2 = z_temp[mm-1,2]
        omega2 = z_temp[mm-1,3]
        z0 = np.array([theta1, omega1, theta2, omega2])
        t0 = t_temp[mm-1]

    return zz,t

#defines event condition for collision
def collision(t, z, M,m,I,l,c,g,gam):

    theta1,omega1,theta2,omega2 = z

    if (theta1>-0.05): #allow legs to pass through for small hip angles (taken care in real walker using stepping stones)
        gstop = 1
    else:
        gstop = theta2 + 2*theta1

    return gstop

#defines the condition when the foot of the walker hits the ground
def footstrike(t, z, params):
    theta1_n,omega1_n,theta2_n,omega2_n = z

    theta1 = theta1_n + theta2_n;
    theta2 = -theta2_n;

    M = params.M
    m = params.m
    I = params.I
    l = params.l
    c = params.c
    g = params.g
    gam = params.gam

    J11 =  1
    J12 =  0
    J13 =  l*(-cos(theta1_n) + cos(theta1_n + theta2_n))
    J14 =  l*cos(theta1_n + theta2_n)
    J21 =  0
    J22 =  1
    J23 =  l*(-sin(theta1_n) + sin(theta1_n + theta2_n))
    J24 =  l*sin(theta1_n + theta2_n)

    J = np.array([[J11, J12, J13, J14], [J21,J22,J23,J24]])

    A11 =  1.0*M + 2.0*m
    A12 =  0
    A13 =  -1.0*M*l*cos(theta1_n) + m*(c - l)*cos(theta1_n) + 1.0*m*(c*cos(theta1_n + theta2_n) - l*cos(theta1_n))
    A14 =  1.0*c*m*cos(theta1_n + theta2_n)
    A21 =  0
    A22 =  1.0*M + 2.0*m
    A23 =  -1.0*M*l*sin(theta1_n) + m*(c - l)*sin(theta1_n) + m*(c*sin(theta1_n + theta2_n) - l*sin(theta1_n))
    A24 =  1.0*c*m*sin(theta1_n + theta2_n)
    A31 =  -1.0*M*l*cos(theta1_n) + m*(c - l)*cos(theta1_n) + 1.0*m*(c*cos(theta1_n + theta2_n) - l*cos(theta1_n))
    A32 =  -1.0*M*l*sin(theta1_n) + m*(c - l)*sin(theta1_n) + m*(c*sin(theta1_n + theta2_n) - l*sin(theta1_n))
    A33 =  2.0*I + M*l**2 + m*(c - l)**2 + m*(c**2 - 2*c*l*cos(theta2_n) + l**2)
    A34 =  1.0*I + c*m*(c - l*cos(theta2_n))
    A41 =  1.0*c*m*cos(theta1_n + theta2_n)
    A42 =  1.0*c*m*sin(theta1_n + theta2_n)
    A43 =  1.0*I + c*m*(c - l*cos(theta2_n))
    A44 =  1.0*I + c**2*m
    A_n_hs = np.array([[A11, A12, A13, A14], [A21, A22, A23, A24], [A31, A32, A33, A34], [A41, A42, A43, A44]])

    X_n_hs = np.array([0, 0, omega1_n, omega2_n])
    b_temp  = A_n_hs.dot(X_n_hs)
    b_hs = np.block([ b_temp, 0, 0 ])
    zeros_22 = np.zeros((2,2))
    A_hs = np.block([[A_n_hs, -np.transpose(J)] , [ J, zeros_22] ])
    invA_hs = np.linalg.inv(A_hs)
    X_hs = invA_hs.dot(b_hs)
    omega1 = X_hs[2] + X_hs[3]
    omega2 = -X_hs[3]

    return [theta1,omega1,theta2,omega2]

#calculation of lagrangian equations
def single_stance(t, z, M,m,I,l,c,g,gam):

    theta1,omega1,theta2,omega2 = z

    A11 =  2.0*I + M*l**2 + m*(c - l)**2 + m*(c**2 - 2*c*l*cos(theta2) + l**2)
    A12 =  1.0*I + c*m*(c - l*cos(theta2))
    A21 =  1.0*I + c*m*(c - l*cos(theta2))
    A22 =  1.0*I + c**2*m

    b1 =  -M*g*l*sin(gam - theta1) + c*g*m*sin(gam - theta1) - c*g*m*sin(-gam + theta1 + theta2) - 2*c*l*m*omega1*omega2*sin(theta2) - c*l*m*omega2**2*sin(theta2) - 2*g*l*m*sin(gam - theta1)
    b2 =  1.0*c*m*(-g*sin(-gam + theta1 + theta2) + l*omega1**2*sin(theta2))

    A_ss = np.array([[A11, A12], [A21,A22]])
    b_ss = np.array([b1,b2])

    invA_ss = np.linalg.inv(A_ss)
    thetaddot = invA_ss.dot(b_ss)
    alpha1 = thetaddot[0]
    alpha2 = thetaddot[1]

    return [omega1,alpha1,omega2,alpha2]

#function to find out current state of the system 
def fixedpt(z0,params):
    t0 = 0
    [z1,t1] = one_step(t0,z0,params)
    N = len(t1)-1
    #F(x0) - x0 = 0
    return z1[N,0]-z0[0], z1[N,1]-z0[1],z1[N,2]-z0[2],z1[N,3]-z0[3]

#calculation of jacobian matrix that helps in stability analysis
def partial_derv(z0,params):

    pert = 1e-5
    N = len(z0)

    J = np.zeros((N,N))
    z_temp1 = [0]*N
    z_temp2 = [0]*N
    for i in range(0,N):
        for j in range(0,N):
            z_temp1[j] = z0[j]
            z_temp2[j] = z0[j]
        z_temp1[i] = z_temp1[i]+pert
        z_temp2[i] = z_temp2[i]-pert
        [z1,t1] = one_step(0,z_temp1,params)
        [z2,t2] = one_step(0,z_temp2,params)
        for j in range(0,N):
            J[i,j] = (z1[len(t1)-1,j] - z2[len(t2)-1,j])/(2*pert)

    return J

params = parameters();

# initial guess used to create stable starting point for the system
q1 = 0.2; u1 = -0.25; q2 = -0.4; u2 = 0.2;

#creation of initial value array z0 to store state variables 
z0 = np.array([q1,u1,q2,u2])

#dz = fixedpt(z0,params)
zstar=fsolve(fixedpt, z0,params)
print(zstar)

J = partial_derv(zstar,params)
eigVal,eigVec = np.linalg.eig(J)
# print(eigVal)
# print(eigVec)
print(np.abs(eigVal))

t0 = 0;
#defines number of steps that you want the walker to walk
steps = 20;
[z,t] = n_steps(t0,zstar,params,steps)
# print(t[len(t)-1])

animate(t,z,params)