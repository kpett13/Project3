# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:39:12 2018

@author: kpett
"""

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
_Qin = []
_Qout = []
_mdot = []
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
#WF_1 = ct.Hfc134a()
#WF_2 = ct.Hfc134a()
#WF_3 = ct.Hfc134a()
#WF_4 = ct.Hfc134a()

WF_1 = ct.Water()
WF_2 = ct.Water()
WF_3 = ct.Water()
WF_4 = ct.Water()

"Knowns"
T1_air = 0+273            # T1 ambient = 0C
P1_air = 1*10**5          # P1 ambient = 1 bar
T2_air = 40+273           # T2 into cabin = 40C
P2_air = P1_air           # P2 = 1 bar
air_1.TP = T1_air,P1_air  # Define state
air_2.TP = T2_air,P2_air  # Define state
h1_air = air_1.h          ###
h2_air = air_2.h          ###

"Set variables"
voldot_air = 500          # Volumetric fow rate of air into cabin (m^3/hr)
D_Gasline = 2             # Inner diameter of gas line (in)
D_Liqline = .5            # Inner diameter of liquid line (in)
q_evaporator = 2500       # Heat rejected from 
n_pump = 0.95             # Pump efficiency
P1 = 0.6*10**4            # Low side pressure
pr = 20                   # Pressure ratio

"Calculations from set variables"
mdot_air = voldot_air*(air_1.density)*1/3600       # Mass flow rate of air into cabin
q_cabin = mdot_air*(air_1.h-air_2.h)               # Heat out of condensor (-)
Ac_Liqline = (math.pi/4)*((0.0254)*D_Liqline)**2   # Cross sectional area of 1/2" ID liquid line
Ac_Gasline = (math.pi/4)*((0.0254)*D_Gasline)**2   # Cross sectional area of 2" ID Gas line


for mdot in range(1,10):
 
    mdot_WF = (mdot/272)   # Define actual mdot of working fluid (kg/s)
    
    "State 2 - Outlet Evaporator / Inlet Pump"
    P2 = P1                # Heat addition is assumed to be isobaric
    X2 = 1                 # Assume saturated vapor
    WF_2.PX = P2, X2       # Define state
    h2 = WF_2.h            ### Get rest of paramaters    
    T2 = WF_2.T            ### 
    s2 = WF_2.s            ###

    "State 3 - Outlet Pump / Inlet Condensor"
    P3 = pr*P2             # Pressure is increased by chosen pressure ratio to P1
    s3_is = s2             # First, assume pump to be isentropic 
    WF_3.SP = s3_is,P3     # Define isentropic outlet state
    h3_is = h2             # Define isentropic outlet enthalpy
    h3 = h_OutCompressor(n_pump, h3_is, h2)    # Define actual outlet enthalpy using pump efficiency
    WF_3.HP = h3,P3                            # Define state
    X3 = WF_3.X            ###
    T3 = WF_3.T            ### Get rest of paramaters
    s3 = WF_3.s            ###
    
    "State 4 - Outlet Condensor / Inlet Throttle"
    P4 = P3                     # Heat addition is isobaric
    h4 = (q_cabin/mdot_WF)+h3   # Change in enthalpy due to heat rejection to cabin
    WF_4.HP = h4,P4             # Define state
    X4 = WF_4.X            ###
    T4 = WF_4.T            ### Get rest of paramaters
    s4 = WF_4.s            ###
    
    "State 1 - Outlet Throttle / Inlet Evaporator"
    h1 = -(q_evaporator/mdot_WF)+h2    # Heat from the source is q = mdot*(delta:h)
    WF_1.HP = h1,P1                    # Define state [P1 is chosen out of loop.] 
    T1 = WF_1.T            ###
    s1 = WF_1.s            ### Get rest of paramaters
    X1 = WF_1.X            ###    

    #Effectiveness of Radiatior
    WF_4_perf =  ct.Water()
    T4_perf = T1_air+1        #effectiveness is rough bc water cannot be solid
    WF_4_perf.TP = T4_perf,P4
    h4_perf = WF_4_perf.h
    e_Rad = (h4-h3)/(h4_perf-h3)
    rho4 = WF_4.density
    rho2 = WF_2.density
    
    _mdot.append(mdot_WF)    
    _Vel_Liq.append(mdot_WF/(Ac_Liqline*rho4))  
    _Vel_Gas.append(mdot_WF/(Ac_Gasline*rho2))
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
    _Qin.append((h4-h3)*mdot_WF)
    _Qout.append((h2-h1)*mdot_WF)
    
pyplot.figure('Q vs. Mass Flow of WF')
pyplot.plot(_mdot, _Qin, label="Q into Cabin")
pyplot.plot(_mdot, _Qout, label="Q from Storage")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Heat (W)')
pyplot.title('Q vs. Mass Flow of WF')    

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
pyplot.plot(_mdot, _h12, label="Storage")
pyplot.plot(_mdot, _h23, label="Pump")
pyplot.plot(_mdot, _h34, label="Condenser")
pyplot.plot(_mdot, _h41, label="Throttle")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Enthalpy Change (J/kg)')
pyplot.title('Enthalpy Change vs. Mass Flow of WF')

pyplot.figure('Entropy Change vs. Mass Flow of WF')
pyplot.plot(_mdot, _s12, label="Storage")
pyplot.plot(_mdot, _s23, label="Pump")
pyplot.plot(_mdot, _s34, label="Condensor")
pyplot.plot(_mdot, _s41, label="Throttle")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Entropy Change (J/kg-K)')
pyplot.title('Entropy Change vs. Mass Flow of WF')

pyplot.figure('Radiator Effectiveness vs. Mass Flow of WF')
pyplot.plot(_mdot, _e_Rad)
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Effectiveness')
pyplot.title('Radiator Effectiveness vs. Mass Flow of WF')

pyplot.figure('WF Velocities vs. Mdot WF')
pyplot.plot(_mdot, _Vel_Liq, label="Liquid")
pyplot.plot(_mdot, _Vel_Gas, label="Gas")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Velocity of WF (m/s)')
pyplot.title('WF Velocities vs. Mdot WF')
pyplot.tight_layout()

