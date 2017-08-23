import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
x1=[]
x2=[]
y1=[]
y2=[]
z1=[]
z2=[]
x3=[]
y3=[]
z3=[]
dt=0.00002
d11 = -10
d12 = 0
d13=0
v11 = -23
v12 = 20
v13=0
d21 = 10
d22 = 0
d23=5
v21 = 14
v22 = 38
v23=0
d31=0
d32=50
d33=45
v31=0
v32=-30
v33=34
g=1000000
for i in range(100000):
    d11+=v11*dt
    d12+=v12*dt
    d21+=v21*dt
    d22+=v22*dt
    d13+=v13*dt
    d23+=v23*dt
    d31+=v31*dt
    d32+=v32*dt
    d33+=v33*dt
    x1.append(d11)
    y1.append(d12)
    z1.append(d13)
    x2.append(d21)
    y2.append(d22)
    z2.append(d23)
    x3.append(d31)
    y3.append(d32)
    z3.append(d33)
    r12=pow(np.sqrt(pow(d11-d21,2)+pow(d12-d22,2)+pow(d13-d23,2)),3)+.1
    r13=pow(np.sqrt(pow(d11-d31,2)+pow(d12-d32,2)+pow(d13-d33,2)),3)+.1
    r23=pow(np.sqrt(pow(d31-d21,2)+pow(d32-d22,2)+pow(d33-d23,2)),3)+.1
    a121=g*(d21-d11)/r12
    a122=g*(d22-d12)/r12
    a123=g*(d23-d13)/r12
    a211=-a121
    a212=-a122
    a213=-a123
    a131=g*(d31-d11)/r13
    a132=g*(d32-d12)/r13
    a133=g*(d33-d13)/r13
    a311=-a131
    a312=-a132
    a313=-a133
    a321=g*(d21-d31)/r23
    a322=g*(d22-d32)/r23
    a323=g*(d23-d33)/r23
    a231=-a321
    a232=-a322
    a233=-a323
    v11=v11+(a121+a131)*dt
    v12=v12+(a122+a132)*dt
    v13=v13+(a123+a133)*dt
    v31=v31+(a321+a311)*dt
    v32=v32+(a322+a312)*dt
    v33=v33+(a323+a313)*dt
    v21=v21+(a211+a231)*dt
    v22=v22+(a212+a232)*dt
    v23=v23+(a213+a233)*dt

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x2, y2, z2)
ax2 = fig.gca(projection='3d')
ax2.plot(x1, y1, z1)
ax3 = fig.gca(projection='3d')
ax3.plot(x3, y3, z3)
#ani = animation.FuncAnimation(fig,  blit=False,interval=0.01, repeat=True)
plt.show()
