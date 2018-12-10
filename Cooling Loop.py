# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 20:23:48 2018

@author: kpett
"""
import cantera as ct 
from matplotlib import pyplot
import math

def h_OutCompressor(n_compressor, h_OutIs, h_In):
    h_OutAct = ((h_OutIs - h_In)/n_compressor)+h_In
    return h_OutAct

"Define lists for plotting"
_W_compressor = []
_COP = []
_Qin = []
_Qout = []
_mdot = []
_Vel_Storage = []
_Vel_Liq = []
_Vel_Gas = []
_e_Rad = []
_T1 = []
_T2 = []
_T3 = []
_T4 = []
_X1 = []
_X2 = []
_X3 = []
_X4 = []
_h12 = []
_h23 = []
_h34 = []
_h41 = []
_s12 = []
_s23 = []
_s34 = []
_s41 = []

"Define Fluids"
air_1 = ct.Solution('air.cti')
air_2 = ct.Solution('air.cti')
WF_1 = ct.Hfc134a()
WF_2 = ct.Hfc134a()
WF_3 = ct.Hfc134a()
WF_4 = ct.Hfc134a()

"Knowns"
T1_air = 38+273.15        # T1 ambient = 38C
P1_air = 1*10**5          # P1 ambient = 1 bar
T2_air = 10+273.15        # T2 into cabin = 10C
P2_air = P1_air           # P2 = 1 bar
air_1.TP = T1_air,P1_air  # Define state
air_2.TP = T2_air,P2_air  # Define state
h1_air = air_1.h          
h2_air = air_2.h          

"Set variables"
voldot_air = 500          # Volumetric fow rate of air into cabin (m^3/hr)
D_gasline = .75           # Inner diameter of gas line (in)
D_liqline = .75             # Inner diameter of liquid line (in)
q_condenser = 2500       # Heat rejected from 
n_compressor = 0.85       # compressor efficiency
P1 = 0.6*10**5            # Low side pressure
pr = 5                   # Pressure ratio wrt. P1
Ac_Storage= 0.05-(500*math.pi*((0.01)**2)/4)      # Cross-sectional area of packed bed storage gaps 
W_fan = 48                # Work into blower fan (W)

"Calculations from set variables"
mdot_air = voldot_air*(air_1.density)*1/3600       # Mass flow rate of air into cabin
q_cabin = mdot_air*(air_1.h-air_2.h)               # Heat into evaporator 
Ac_Liqline = (math.pi/4)*((0.0254)*D_liqline)**2   # Cross sectional area of liquid line
Ac_Gasline = (math.pi/4)*((0.0254)*D_gasline)**2   # Cross sectional area of Gas line

for mdot in range(1,10):
    
    mdot_WF = (mdot/69)   # Define actual mdot of working fluid (kg/s)

    "State 1 - Outlet Evaporator / Inlet Compressor"
    X1 = 1                 # Working fluid is assumed to be saturated vapor 
    WF_1.PX = P1,X1        # Define state 
    h1 = WF_1.h                   
    s1 = WF_1.s           
    T1 = WF_1.T            
    rho1 = WF_1.density
    
    "State 2 - Outlet Compressor / Inlet Condensor"
    P2 = P1*pr                # Pressure is set to high side
    s2_is = s1             # First, assume compressor to be isentropic 
    WF_2.SP = s2_is,P2     # Define isentropic outlet state
    h2_is = WF_2.h         # Define isentropic outlet enthalpy
    h2 = h_OutCompressor(n_compressor, h2_is, h1)    # Define actual outlet enthalpy using compressor efficiency
    WF_2.HP = h2,P2        # Define state
    X2 = WF_2.X           
    T2 = WF_2.T           
    s2 = WF_2.s           
    rho2 = WF_2.density
    
    "State 3 - Outlet Condensor / Inlet Throttle"
    P3 = P2                         # Heat addition is isobaric
    h3 = h2-(q_condenser/mdot_WF)   # Change in enthalpy due to heat from ambient
    WF_3.HP = h3,P3                 # Define state
    X3 = WF_3.X           
    T3 = WF_3.T           
    s3 = WF_3.s       
    rho3 = WF_3.density
    
    "State 4 - Outlet Throttle / Inlet Evaporator"
    P4 = P1                     # Heat addition is isobaric
    h4 = h1-(q_cabin/mdot_WF)  # Change in enthalpy due to heat from ambient
    WF_4.HP = h4,P4             # Define state
    X4 = WF_4.X          
    T4 = WF_4.T            
    s4 = WF_4.s 
    rho4 = WF_4.density    
    
    "Effectiveness of Cabin Radiatior"
    WF_1_perf =  ct.Hfc134a()
    T1_perf = T1_air
    WF_1_perf.TP = T1_perf,P1
    h1_perf = WF_1_perf.h
    e_Rad = (h1-h4)/(h1_perf-h4)
    
    W_compressor = (h2-h1)*mdot_WF    
    
    _W_compressor.append(W_compressor)
    _mdot.append(mdot_WF)    
    _e_Rad.append(e_Rad)
    _T1.append(T1)
    _T2.append(T2)
    _T3.append(T3)
    _T4.append(T4)
    _X1.append(X1)
    _X2.append(X2)
    _X3.append(X3)
    _X4.append(X4)
    _s12.append(s2-s1)
    _s23.append(s3-s2)
    _s34.append(s4-s3)
    _s41.append(s1-s4)
    _h12.append(h2-h1)
    _h23.append(h3-h2)
    _h34.append(h4-h3)
    _h41.append(h1-h4)
    
    _Vel_Storage.append(mdot_WF/(Ac_Storage*(rho4+rho1)/2))
    _Vel_Liq.append(mdot_WF/(Ac_Liqline*rho3))  
    _Vel_Gas.append(mdot_WF/(Ac_Gasline*rho1))
    
    _COP.append(q_cabin/(W_compressor+W_fan))
    
pyplot.figure('Work into Compressor vs. Mass Flow of WF')
pyplot.plot(_mdot, _W_compressor)
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Work (W)')
pyplot.title('Work vs. Mass Flow of WF')   

pyplot.figure('Temperature vs. Mass Flow of WF')
pyplot.plot(_mdot, _T1, label="State 1")
pyplot.plot(_mdot, _T2, label="State 2")
pyplot.plot(_mdot, _T3, label="State 3")
pyplot.plot(_mdot, _T4, label="State 4")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Temperature (K)')
pyplot.title('Temperature vs. Mass Flow of WF')

pyplot.figure('Quality vs. Mass Flow of WF')
pyplot.plot(_mdot, _X1, label="State 1")
pyplot.plot(_mdot, _X2, label="State 2")
pyplot.plot(_mdot, _X3, label="State 3")
pyplot.plot(_mdot, _X4, label="State 4")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Quality')
pyplot.title('Quality vs. Mass Flow of WF')

pyplot.figure('Enthalpy Change vs. Mass Flow of WF')
pyplot.plot(_mdot, _h12, label="Compressor")
pyplot.plot(_mdot, _h23, label="Condensor (Storage)")
pyplot.plot(_mdot, _h34, label="Throttle")
pyplot.plot(_mdot, _h41, label="Evaporator (To cabin)")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Enthalpy Change (J/kg)')
pyplot.title('Enthalpy Change vs. Mass Flow of WF')

pyplot.figure('Entropy Change vs. Mass Flow of WF')
pyplot.plot(_mdot, _s12, label="Compressor")
pyplot.plot(_mdot, _s23, label="Condensor (Storage)")
pyplot.plot(_mdot, _s34, label="Throttle")
pyplot.plot(_mdot, _s41, label="Evaporator (To cabin)")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Entropy Change (J/kg-K)')
pyplot.title('Entropy Change vs. Mass Flow of WF')

pyplot.figure('Radiator Effectiveness vs. Mass Flow of WF')
pyplot.plot(_mdot, _e_Rad)
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Effectiveness')
pyplot.title('Radiator Effectiveness vs. Mass Flow of WF')

pyplot.figure('COP vs. Mass Flow of WF')
pyplot.plot(_mdot, _COP)
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('COP')
pyplot.title('COP vs. Mass Flow of WF')

pyplot.figure('WF Velocities vs. Mdot WF')
pyplot.plot(_mdot, _Vel_Liq, label="Liquid")
pyplot.plot(_mdot, _Vel_Gas, label="Gas")
pyplot.plot(_mdot, _Vel_Storage, label="Storage")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Velocity of WF (m/s)')
pyplot.title('WF Velocities vs. Mdot WF')
pyplot.tight_layout()

n_arrays = 4
N_per_array = 65  
t_fin = 0.05*0.0254
space_fin = ((6.5*0.0254)-(N_per_array*t_fin))/(N_per_array-1)
t_rad = 12*0.0254
h_fin = (6/4)*0.0254
A_base = space_fin*0.0254*t_rad
Ac_air = space_fin*(N_per_array-1)*n_arrays*h_fin
v_air = voldot_air*(1/3600)*(1/Ac_air)
A_fin = 2*t_rad*h_fin
A_tot = 2*n_arrays*(N_per_array-1)*A_base+(N_per_array-1)*2*t_rad*h_fin

avg_dynvis = (air_1.viscosity+air_2.viscosity)/2
avg_rho = (air_1.density+air_2.density)/2
avg_cp = (air_1.cp+air_2.cp)/2
avg_k = (air_1.thermal_conductivity+air_2.thermal_conductivity)/2
avg_Pr = (avg_cp*avg_dynvis)/avg_k
Re = avg_rho*v_air*t_rad/(avg_dynvis)

if (Re < 5*10**5):
    Nu = 0.664*Re**.5*avg_Pr**(1/3) 
else:
    Nu = ((0.037*Re**(4/5))-871)*avg_Pr**(1/3)
h = avg_k*Nu/t_rad
k_al = 205
k_copper = 385
perimeter_fin = 2*t_rad+2*h_fin
Ac_fin = t_rad*t_fin

m = math.sqrt((h*perimeter_fin)/(k_al*Ac_fin))
eta_fin = math.tanh(m*t_rad)/(m*t_rad)

UA_needed = q_cabin/(T1_air-176) 
UA_actual = h*A_tot-h*A_fin*(1-eta_fin)

space_fin_in = space_fin/0.0254
