import numpy as np
from matplotlib import pyplot as plt

import scipy.optimize as opt
from scipy.integrate import solve_ivp, odeint

from powered_walker import single_stance as power_stance
from powered_walker import single_stance_ode_int as power_stance_ode_int

from main_walker import single_stance, single_stance2, single_stance_ode_int
from main_walker import footstrike, animate, plot

from main_walker import Parameters as WalkerParameters

# time_min = 0.3; time_max = 0.6;
# P_min = 0.1; P_max = 0.4;
# u_min = -2; u_max = 2;
# P = 0.1;
# X0 = [time z_ss0 z_bfs P u_opt];
# z_ss_lb = [0.1 -2 -2*0.4 -4];z_ss_ub = [0.4 -0.1 -2*0.1 4];
# z_bfs_lb = [-0.4 -2 2*0.1 -4];z_bfs_ub = [-0.1 -0.1 2*0.4 4];
# 
# LB = [time_min z_ss_lb z_bfs_lb P_min u_lb];
# UB = [time_max z_ss_ub z_bfs_ub P_max u_ub];
#
# constraints
# [z_ssT,z_afs,~,~,d_step,v_step] = simulator(x,walker);
# ceq = [z_ss0 - z_afs,z_ssT - z_bfs, collision_condition, (d_step-0.5), (v_step-1)];
# 
# simulator
# z_ssT = z_temp(end,1:4);
# d_step = 2*l*sin(0.5*z_ssT(3));
# time = x(1);
# t_step = time;
# v_step = d_step/t_step;
#
# cost
# P = x(10);
# F = sum(u_opt.*u_opt)*dt + P^2;

class OptParams:
    def __init__(self):
        self.N = 4

def cost(x, args):
    
    N = OptParams().N;
    
    time = x[0]
    dt = time / N
    u_opt = x[10:10+N+1]
    P = x[9]

    F = sum([ x*y for x,y in zip(u_opt, u_opt)] ) * dt + P*P
    return F

def simulator(x):
    
    z_ss0, z_bfs = x[1:5], x[5:9]
    u_opt = x[10:10+N+1]
    
    params = WalkerParameters()
    params.P = x[9]
    
    t_start = 0
    t_end = x[0]
    t_span = np.linspace(t_start, t_end, 100)
    t_opt = np.linspace(t_start, t_end, N+1)
    
    sol = solve_ivp(
        power_stance, [t_start, t_end], z_ss0, method='RK45', t_eval=t_span,
        dense_output=True, atol = 1e-13, rtol = 1e-13, 
        args=(params.M,params.m,params.I,params.l,params.c,params.g,params.gam, t_opt, u_opt)
    )
    
    t = sol.t
    # m : 4 / n : 100
    m, n = np.shape(sol.y)
    z = np.zeros((n, m))
    z = sol.y.T
    
    z_ssT = z[-1]
    z_afs = footstrike( 0, z_bfs, params);
    
    l = params.l
    # 2 l sin(theta2/2) 
    d_step = 2 * l * np.sin(0.5 * z_ssT[2])
    t_step = x[0]
    v_step = d_step / t_step
    
    xh = l * np.sin(z[0,0]) - l * np.sin(z[:,0])
    yh = l * np.cos(z[:,0])
    
    # Convert the list to a 2D array
    xh = np.expand_dims(np.array(xh), axis=1)
    yh = np.expand_dims(np.array(yh), axis=1)
    z_output = np.concatenate((z, xh, yh), axis=1)

    return z_ssT, z_afs, t, z_output, d_step, v_step

def simulator_odeint(x):

    N = OptParams().N

    time = x[0]
    z_ss0 = x[1:5]; z_bfs = x[5:9]
    u_opt = x[10:10+N+1]
    
    params = WalkerParameters()
    params.P = x[9]
    
    t_opt = np.linspace(0, time, N+1)
    z = np.zeros((N+1, 4))
    z[0] = z_ss0
    
    dynamics_args = (params.M,params.m,params.I,params.l,params.c,params.g,params.gam)
    
    for i in range(0, N):
        args = dynamics_args + (t_opt[i],t_opt[i+1],u_opt[i], u_opt[i+1])
        z_temp = odeint(
            power_stance_ode_int, z[i], np.array([t_opt[i], t_opt[i+1]]), 
            args, atol = 1e-13, rtol = 1e-13
        )
        z[i+1] = z_temp[-1]
        
    z_ssT = z[-1]
    z_afs = footstrike( 0, z_bfs, params)
    
    l = params.l
    d_step = 2 * l * np.sin(0.5 * z_ssT[2])
    t_step = time
    v_step = d_step / t_step
    
    xh = l * np.sin(z[0,0]) - l * np.sin(z[:,0])
    yh = l * np.cos(z[:,0])
    
    # Convert the list to a 2D array
    xh = np.expand_dims(np.array(xh), axis=1)
    yh = np.expand_dims(np.array(yh), axis=1)
    z_output = np.concatenate((z, xh, yh), axis=1)

    return z_ssT, z_afs, t_opt, z_output, d_step, v_step

def walker_constraint(x):
    
    time = x[0]
    z_ss0 = x[1:5]
    z_bfs = x[5:9]

    # theta1, omega1, theta2, omega2
    theta1_bfs = z_bfs[0]
    theta2_bfs = z_bfs[2]
    collision_condition = theta2_bfs + 2*theta1_bfs
    
    # z_ssT, z_afs, _, _, d_step, v_step = simulator(x)
    
    # odeint is more Faster than solve_ivp
    z_ssT, z_afs, _, _, d_step, v_step = simulator_odeint(x)

    swing_state_diff = z_ss0 - z_afs
    strike_state_diff = z_bfs - z_ssT
    
    # debugging
    print(f"swing_state_diff: {swing_state_diff}")
    print(f"strike_state_diff: {strike_state_diff}")
    print(f"d_step: {d_step} / v_step: {v_step}")
    opt_funcs = [ *swing_state_diff, *strike_state_diff, collision_condition, (0.5-d_step), (1-v_step) ]
    
    return opt_funcs

# Define a callback function to display step results
def callback(xk):
    print('Step result:', xk)

def torque_plot(opt_result):
    
    plt.figure(1)

    plt.plot(opt_result[9:],'r--')
    plt.ylabel('torque')

    plt.show(block=False)
    plt.pause(3)
    plt.close()

if __name__=="__main__":
    
    opt_params = OptParams()
    
    # control sampling
    N = opt_params.N
    
    time_min, time_max = 0.3, 1.0
    u_min, u_max = -2.0, 2.0
    P_min, P_max = 0.1, 0.4
    
    # theta1, omega1, theta2, omega2
    z_ss_lb = [0.1, -2, -2*0.4, -4]; z_ss_ub = [0.4, -0.1, -2*0.1, 4]
    z_bfs_lb = [-0.4, -2, 2*0.1, -4]; z_bfs_ub = [-0.1, -0.1, 2*0.4, 4]

    #####################################################
    ######## example a. powered walker optimize #########
    #####################################################
    
    # t_bf_strike = (time_min + time_max) / 2
    # z_ini = [0.15, -0.2, -0.3, 0]
    # z_bf_strike = [-0.15, -0.2, 0.3, 0]
    
    # use optimal states for faster solve_ivp optim
    t_bf_strike = (time_min + time_max) / 2
    z_ini = [ 0.18350086, -0.27333605, -0.36700172, 0.03138303]
    z_bf_strike = [ -0.18350086, -0.27333605, 0.36700172, 0.03138303]
    
    P = 0.1
    u_opt = (u_min + (u_max-u_min) * np.random.rand(1, N+1)).flatten()
    
    # example a. powered walker optimize
    u_lb = (u_min * np.ones((1,N+1))).flatten()
    u_ub = (u_max * np.ones((1,N+1))).flatten()
    x0 = [ t_bf_strike, *z_ini, *z_bf_strike, P, *u_opt ]
    x_min = [ time_min, *z_ss_lb, *z_bfs_lb, P_min, *u_lb ]
    x_max = [ time_max, *z_ss_ub, *z_bfs_ub, P_max, *u_ub ]
    
    limits = opt.Bounds(x_min, x_max)
    
    constraint = {
        'type': 'eq',
        'fun': walker_constraint
    }
    
    result = opt.minimize(
        cost, x0, args=(WalkerParameters), method='SLSQP', 
        constraints=[constraint], 
        options={'ftol': 1e-6, 'disp': True, 'maxiter':500},
        bounds=limits
    )
    opt_state = result.x
        
    for i in range(9):
        print(opt_state[i])
    
    print('Copy paste in main_walker.py')
    print(f"params.t_opt = {np.linspace(0, opt_state[0], N+1)}")
    print(f"params.u_opt = {opt_state[10:]}")
    print(f"params.P = {opt_state[9]}")
    print("=== initial state ===")
    print(f"theta1, omega1, theta2, omega2 = {opt_state[1]}, {opt_state[2]}, {opt_state[3]}, {opt_state[4]}")
    print("=== befor strike ===")
    print(f"theta1, omega1, theta2, omega2 = {opt_state[5]}, {opt_state[6]}, {opt_state[7]}, {opt_state[8]}")
    
    # z_ssT, z_afs, t, z_output, d_step, v_step = simulator(opt_state)
    z_ssT, z_afs, t, z_output, d_step, v_step = simulator_odeint(opt_state)
    walker_param = WalkerParameters()
    animate(t, z_output, walker_param)
    torque_plot(opt_state)