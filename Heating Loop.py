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
WF_1 = ct.Water()
WF_2 = ct.Water()
WF_3 = ct.Water()
WF_4 = ct.Water()

"Knowns"
T1_air = 0+273.15         # T1 ambient = 0C
P1_air = 1*10**5          # P1 ambient = 1 bar
T2_air = 40+273.15        # T2 into cabin = 40C
P2_air = P1_air           # P2 = 1 bar
air_1.TP = T1_air,P1_air  # Define state
air_2.TP = T2_air,P2_air  # Define state
h1_air = air_1.h          
h2_air = air_2.h   
       
"Set variables"
voldot_air = 500          # Volumetric fow rate of air into cabin (m^3/hr)
D_Gasline = .75             # Inner diameter of gas line (in)
D_Liqline = .75            # Inner diameter of liquid line (in)
q_evaporator = 2500       # Heat rejected from 
n_compressor = 0.7       # Compressor efficiency
P1 = 0.6*10**5            # Low side pressure
pr = 5                    # Pressure ratio
Ac_Storage= 0.05-(500*math.pi*((0.01)**2)/4)      # Cross Sectional Area of Storage 
W_fan = 48

"Calculations from set variables"
mdot_air = voldot_air*(air_1.density)*1/3600       # Mass flow rate of air into cabin
q_cabin = mdot_air*(air_2.h-air_1.h)               # Heat out of condensor
Ac_Liqline = (math.pi/4)*((0.0254)*D_Liqline)**2   # Cross sectional area of 1/2" ID liquid line
Ac_Gasline = (math.pi/4)*((0.0254)*D_Gasline)**2   # Cross sectional area of 2" ID Gas line

for mdot in range(1,5):
 
    mdot_WF = (mdot/380)   # Define actual mdot of working fluid (kg/s)
    
    "State 1 - Outlet Evaporator / Inlet Compressor"
    X1 = 1                 # Assume saturated vapor
    WF_1.PX = P1, X1       # Define state
    h1 = WF_1.h             
    T1 = WF_1.T          
    s1 = WF_1.s           
    rho1 = WF_1.density
    
    "State 2 - Outlet Compressor / Inlet Condensor"
    P2 = pr*P1             # Pressure is increased through compressor
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
    P3 = P2                     # Heat addition is isobaric
    h3 = h2-(q_cabin/mdot_WF)   # Enthalpy drop due to heat rejection to cabin
    WF_3.HP = h3,P3             # Define state
    X3 = WF_3.X
    T3 = WF_3.T         
    s3 = WF_3.s       
    rho3 = WF_3.density
    
    "State 4 - Outlet Throttle / Inlet Evaporator"
    P4 = P1                            # Pressure is set to low side 
    h4 = -(q_evaporator/mdot_WF)+h1    # Heat from the source is q = mdot*(delta:h)
    WF_4.HP = h4,P4                    # Define state  
    T4 = WF_4.T            
    s4 = WF_4.s          
    X4 = WF_4.X             
    rho4 = WF_4.density
    
    "Effectiveness of Radiatior"
    WF_3_perf =  ct.Water()      # Define a state of WF
    T3_perf = T1_air+0.05        # Set outlet state of WF to inlet state of air
    WF_3_perf.TP = T3_perf,P3    
    h3_perf = WF_3_perf.h
    e_Rad = (h3-h2)/(h3_perf-h2) # Calculate required effectiveness
    
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
pyplot.plot(_mdot, _h23, label="Condensor (To cabin)")
pyplot.plot(_mdot, _h34, label="Throttle")
pyplot.plot(_mdot, _h41, label="Evaporator (Storage)")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Enthalpy Change (J/kg)')
pyplot.title('Enthalpy Change vs. Mass Flow of WF')

pyplot.figure('Entropy Change vs. Mass Flow of WF')
pyplot.plot(_mdot, _s12, label="Compressor")
pyplot.plot(_mdot, _s23, label="Condensor (To cabin)")
pyplot.plot(_mdot, _s34, label="Throttle")
pyplot.plot(_mdot, _s41, label="Evaporator (Storage)")
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

