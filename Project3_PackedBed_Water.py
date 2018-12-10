import numpy
import cantera

H2O = cantera.Water()
Xi = 0.62345
Pi = 0.6E5
H2O.PX = Pi, Xi
Ti = H2O.T

Ts = 473 #Surface temperature of Al spheres [K]
Ti = 273 #[K]

V = 0.3735 #Fluid Velocity [m/s]
D = 0.01 #Al sphere Diamemter [m]
L = 0.1 #Length of Bed [m]
W = 0.75 #Width of Bed
H = 0.5 #Height of Bed
N = round(W/D,0)*round(L/D,0)*round(H/D,0) #Number of spheres
N = round(N - N*0.05,0) #Reduction in 5% of spheres due to packing

v_d = numpy.interp(Ti, temperature, Viscosity_dyn) #Dynamic Viscosity of Fluid [m²/s]
v_g = numpy.interp(Ti, temperature, vg) #Density of fluid
Pr = numpy.interp(Ti, temperature, Pr) #Prandtl Number of Fluid
Kf = numpy.interp(Ti, temperature, conductivity) #Conductivity of Fluid
rho = 1/v_g

v_ds = numpy.interp(Ts, temperature, Viscosity_dyn) #Dynamic viscosity of air at surface temperature
vg_s = numpy.interp(Ts, temperature, vg) #Desnity of air at surface temperature
rho_s = 1/vg_s

v_k = rho*v_d #Kinematic viscosity at ambient temperature
v_ks = rho_s*v_ds #Kinematic viscosity at surface temperature

Re = V*D/v_d
Nu = 2 + (0.4*Re**(1/2) + 0.06*Re**(2/3))*Pr**0.4*(v_k/v_ks)**(1/4)
h = Nu/Kf*L

A_pt = N*numpy.pi*D**2 #Surface area of spheres
A_cb = W*H #Cross-Sectional Area of Channel

Cp = 950 #Specific heat of Al [J/kg*K]
rho_sphere = 2700 #Density of Al [kg/m³]
Vol_sphere = 4/3*numpy.pi*(D/2)**3

To = Ts - (Ts-Ti)*numpy.exp(-h*A_pt/(rho*V*A_cb*Cp)) - 273 #Outlet temperature [°C]
#t = rho*V*Cp/(h*A_cb)*numpy.log((Ts-Ti)/(Ti-To))
W = N*rho_sphere*Vol_sphere #Weight [kg]