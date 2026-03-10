"""import numpy as np
import matplotlib.pyplot as plt

# Parameters
nx = 41          # grid points in x
ny = 41          # grid points in y
lx = 1.0         # cavity length
ly = 1.0
dx = lx / (nx - 1)
dy = ly / (ny - 1)
nt = 500         # number of time steps
dt = 0.001       # time step
Re = 100         # Reynolds number
nu = 1/Re        # kinematic viscosity

# Initialize fields
u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))

# Functions
def build_up_b(b, u, v, dx, dy, dt):
    b[1:-1,1:-1] = (1/dt)*(
        (u[1:-1,2:] - u[1:-1,0:-2])/(2*dx) +
        (v[2:,1:-1] - v[0:-2,1:-1])/(2*dy)
    ) - ((u[1:-1,2:] - u[1:-1,0:-2])/(2*dx))**2 - 2*((u[2:,1:-1]-u[0:-2,1:-1])/(2*dy)*(v[1:-1,2:]-v[1:-1,0:-2])/(2*dx)) - ((v[2:,1:-1]-v[0:-2,1:-1])/(2*dy))**2
    return b

def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p)
    for q in range(50):
        pn[:] = p[:]
        p[1:-1,1:-1] = (((pn[1:-1,2:] + pn[1:-1,0:-2])*dy**2 +
                         (pn[2:,1:-1] + pn[0:-2,1:-1])*dx**2) /
                        (2*(dx**2 + dy**2)) -
                        dx**2*dy**2/(2*(dx**2 + dy**2)) * b[1:-1,1:-1])
        # Boundary conditions
        p[:,-1] = p[:,-2]   # dp/dx = 0 at x = L
        p[:,0] = p[:,1]     # dp/dx = 0 at x = 0
        p[-1,:] = 0         # p = 0 at y = L
        p[0,:] = p[1,:]     # dp/dy = 0 at y = 0
    return p

# Time-stepping
for n in range(nt):
    un = u.copy()
    vn = v.copy()
    
    b = build_up_b(b, u, v, dx, dy, dt)
    p = pressure_poisson(p, dx, dy, b)
    
    u[1:-1,1:-1] = (un[1:-1,1:-1] -
                     un[1:-1,1:-1]*dt/dx*(un[1:-1,1:-1]-un[1:-1,0:-2]) -
                     vn[1:-1,1:-1]*dt/dy*(un[1:-1,1:-1]-un[0:-2,1:-1]) -
                     dt/(2*dx)*(p[1:-1,2:]-p[1:-1,0:-2]) +
                     nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2]) +
                         dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1])))
    
    v[1:-1,1:-1] = (vn[1:-1,1:-1] -
                     un[1:-1,1:-1]*dt/dx*(vn[1:-1,1:-1]-vn[1:-1,0:-2]) -
                     vn[1:-1,1:-1]*dt/dy*(vn[1:-1,1:-1]-vn[0:-2,1:-1]) -
                     dt/(2*dy)*(p[2:,1:-1]-p[0:-2,1:-1]) +
                     nu*(dt/dx**2*(vn[1:-1,2:]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2]) +
                         dt/dy**2*(vn[2:,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1])))
    
    # Lid boundary condition: moving lid at top
    u[-1,:] = 1
    v[-1,:] = 0
    
    # No-slip boundary conditions
    u[0,:] = u[:,0] = u[:,-1] = 0
    v[0,:] = v[:,0] = v[:,-1] = 0

# Plot results
X, Y = np.meshgrid(np.linspace(0, lx, nx), np.linspace(0, ly, ny))
plt.figure(figsize=(8,6))
plt.quiver(X, Y, u, v)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Velocity field in Lid-Driven Cavity')
plt.show(block=True)"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensures VS Code can show plots
import matplotlib.pyplot as plt

# -----------------------
# Parameters
# -----------------------
nx, ny = 41, 41      # grid points
lx, ly = 1.0, 1.0    # cavity dimensions
dx, dy = lx/(nx-1), ly/(ny-1)
nt = 500             # time steps
dt = 0.001           # time step
Re = 100             # Reynolds number
nu = 1/Re            # kinematic viscosity

# -----------------------
# Initialize fields
# -----------------------
u = np.zeros((ny, nx))
v = np.zeros((ny, nx))
p = np.zeros((ny, nx))
b = np.zeros((ny, nx))

# -----------------------
# Functions
# -----------------------
def build_up_b(b, u, v, dx, dy, dt):
    b[1:-1,1:-1] = (1/dt)*(
        (u[1:-1,2:] - u[1:-1,0:-2])/(2*dx) +
        (v[2:,1:-1] - v[0:-2,1:-1])/(2*dy)
    ) - ((u[1:-1,2:] - u[1:-1,0:-2])/(2*dx))**2 - 2*((u[2:,1:-1]-u[0:-2,1:-1])/(2*dy)*(v[1:-1,2:]-v[1:-1,0:-2])/(2*dx)) - ((v[2:,1:-1]-v[0:-2,1:-1])/(2*dy))**2
    return b

def pressure_poisson(p, dx, dy, b):
    pn = np.empty_like(p)
    for _ in range(50):
        pn[:] = p[:]
        p[1:-1,1:-1] = (((pn[1:-1,2:] + pn[1:-1,0:-2])*dy**2 +
                         (pn[2:,1:-1] + pn[0:-2,1:-1])*dx**2) /
                        (2*(dx**2 + dy**2)) -
                        dx**2*dy**2/(2*(dx**2 + dy**2)) * b[1:-1,1:-1])
        # Boundary conditions
        p[:,-1] = p[:,-2]
        p[:,0] = p[:,1]
        p[-1,:] = 0
        p[0,:] = p[1,:]
    return p

# -----------------------
# Time-stepping
# -----------------------
for n in range(nt):
    un = u.copy()
    vn = v.copy()
    
    b = build_up_b(b, u, v, dx, dy, dt)
    p = pressure_poisson(p, dx, dy, b)
    
    u[1:-1,1:-1] = (un[1:-1,1:-1] -
                     un[1:-1,1:-1]*dt/dx*(un[1:-1,1:-1]-un[1:-1,0:-2]) -
                     vn[1:-1,1:-1]*dt/dy*(un[1:-1,1:-1]-un[0:-2,1:-1]) -
                     dt/(2*dx)*(p[1:-1,2:]-p[1:-1,0:-2]) +
                     nu*(dt/dx**2*(un[1:-1,2:]-2*un[1:-1,1:-1]+un[1:-1,0:-2]) +
                         dt/dy**2*(un[2:,1:-1]-2*un[1:-1,1:-1]+un[0:-2,1:-1])))
    
    v[1:-1,1:-1] = (vn[1:-1,1:-1] -
                     un[1:-1,1:-1]*dt/dx*(vn[1:-1,1:-1]-vn[1:-1,0:-2]) -
                     vn[1:-1,1:-1]*dt/dy*(vn[1:-1,1:-1]-vn[0:-2,1:-1]) -
                     dt/(2*dy)*(p[2:,1:-1]-p[0:-2,1:-1]) +
                     nu*(dt/dx**2*(vn[1:-1,2:]-2*vn[1:-1,1:-1]+vn[1:-1,0:-2]) +
                         dt/dy**2*(vn[2:,1:-1]-2*vn[1:-1,1:-1]+vn[0:-2,1:-1])))
    
    # Lid boundary condition: top lid moves right
    u[-1,:] = 1
    v[-1,:] = 0
    
    # No-slip on other walls
    u[0,:] = u[:,0] = u[:,-1] = 0
    v[0,:] = v[:,0] = v[:,-1] = 0

# -----------------------
# Visualization
# -----------------------
X, Y = np.meshgrid(np.linspace(0, lx, nx), np.linspace(0, ly, ny))
speed = np.sqrt(u**2 + v**2)

plt.figure(figsize=(10,4))

# Velocity magnitude heatmap
plt.subplot(1,2,1)
plt.contourf(X, Y, speed, cmap='jet')
plt.colorbar(label='Velocity magnitude')
plt.title('Velocity magnitude')
plt.xlabel('X')
plt.ylabel('Y')

# Velocity vectors (quiver)
plt.subplot(1,2,2)
plt.quiver(X, Y, u, v)
plt.title('Velocity vectors')
plt.xlabel('X')
plt.ylabel('Y')

plt.tight_layout()
plt.show(block=True)