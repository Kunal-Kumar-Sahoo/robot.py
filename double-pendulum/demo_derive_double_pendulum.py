import sympy as sy

#define symbolic quantities
theta1,theta2  = sy.symbols('', real=True)
omega1,omega2  = sy.symbols('', real=True)
alpha1,alpha2  = sy.symbols('', real=True)
m1,m2,I1,I2,g  = sy.symbols('', real=True)
c1,c2,l        = sy.symbols('', real=True)

#1a) position vectors
mpi = sy.pi
cos1 = sy.cos()
sin1 = sy.sin()
H01 = sy.Matrix([])

cos2 = sy.cos()
sin2 = sy.sin()
H12 = sy.Matrix([])

H02 = 

C1 = sy.Matrix([c1, 0, 1])
G1 = H01*C1
C2 = sy.Matrix([c2, 0, 1])
G2 = H02*C2

x_G1 = sy.Matrix([])
y_G1 = sy.Matrix([])
x_G2 = sy.Matrix([])
y_G2 = sy.Matrix([])

#1b) velocity vectors
q = sy.Matrix([theta1, theta2])
qdot = sy.Matrix([omega1, omega2])
v_G1_x = x_G1.jacobian(q)*qdot 
v_G1_y = y_G1.jacobian(q)*qdot
v_G2_x = x_G2.jacobian(q)*qdot
v_G2_y = y_G2.jacobian(q)*qdot
v_G1 = sy.Matrix([v_G1_x,v_G1_y])
v_G2 = sy.Matrix([v_G2_x,v_G2_y])

#2) Lagrangian
T = 

V = 
L = T-V


#3) Derive equations
