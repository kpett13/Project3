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

#Define lists
_mdot = []
_Vel_Liq = []
_Vel_Gas = []
_e_Rad = []
_P1 = []
_P2 = []
_P3 = []
_P4 = []
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

#Define Fluids
air_1 = ct.Solution('air.cti')
air_2 = ct.Solution('air.cti')

#Knowns
T1_air = 38+273
P1_air = 101325

T2_air = 10+273
P2_air = 101325

air_1.TP = T1_air,P1_air
air_2.TP = T2_air,P2_air

h1_air = air_1.h
h2_air = air_2.h

voldot_air = 650  # m^3/hr
mdot_air = voldot_air*(air_1.density)*1/3600

Ac_Liqline = (math.pi/4)*((0.0254)*5/16)**2  # Cross sectional area of 5/16" ID liquid line
Ac_Gasline = (math.pi/4)*((0.0254)*13/32)**2  # Cross sectional area of 13/32" ID Gas line

#Sets
q_storage = -2500
q_cabin = mdot_air*(air_1.h-air_2.h)
n_pump = 0.95

WF_1 = ct.Hfc134a()
WF_2 = ct.Hfc134a()
WF_3 = ct.Hfc134a()
WF_4 = ct.Hfc134a()


#Changing
P1 = 1*10**4 
pr = 5


for mdot in range(1,100):
    
    mdot_WF = (mdot/100)
    
    # State 1 - Before Storage
    X1 = 1                 # Fluid is a vapor
    WF_1.PX = P1, 1        # Define fluid
    
    T1 = WF_1.T
    s1 = WF_1.s
    h1 = WF_1.h
    
    #State 2 - Before Pump
    P2 = P1                                # Heat rejection is isobaric
    h2 = (q_storage/mdot_WF)+h1   # delta h is defined by q_storage
    WF_2.HP = h2, P2                       # Define fluid
    
    X2 = WF_2.X
    T2 = WF_2.T
    s2 = WF_2.s

    #State 3 - Before Radiator
    P3 = pr*P2
    s3_is = s2
    WF_3.SP = s3_is,P3
    h3_is = WF_2.h
    h3 = h_OutCompressor(n_pump, h3_is, h2)
    WF_3.HP = h3,P3
    
    X3 = WF_3.X
    T3 = WF_3.T
    s3 = WF_3.s
    
    #State 4 - Before Throttle
    P4 = P3
    h4 = (q_cabin/mdot_WF)+h3
    WF_4.HP = h4,P4
    
    X4 = WF_4.X
    T4 = WF_4.T
    s4 = WF_4.s
    
    #Effectiveness of Radiatior
    air_2_perf = ct.Solution('air.cti')
    T2_air_perf = T3
    air_2_perf.TP = T2_air_perf,P2_air
    h2_air_perf = air_2_perf.h
    e_Rad = (h2_air-h1_air)/(h2_air_perf-h1_air)
    
    _mdot.append(mdot_WF)    

    _Vel_Liq.append(mdot_WF/(Ac_Liqline*WF_2.density))
    _Vel_Gas.append(mdot_WF/(Ac_Gasline*WF_1.density))
    _e_Rad.append(e_Rad)
    _P1.append(P1/10**4)
    _P2.append(P2/10**4)
    _P3.append(P3/10**4)
    _P4.append(P4/10**4)
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
    
pyplot.figure('Pressure vs. Mass Flow of WF')
pyplot.plot(_mdot, _P1, label="State 1")
pyplot.plot(_mdot, _P2, label="State 2")
pyplot.plot(_mdot, _P3, label="State 3")
pyplot.plot(_mdot, _P4, label="State 4")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Pressure (atm)')
pyplot.title('Pressure vs. Mass Flow of WF')

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
pyplot.plot(_mdot, _h34, label="Radiator")
pyplot.plot(_mdot, _h41, label="Throttle")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Enthalpy Change (J/kg)')
pyplot.title('Enthalpy Change vs. Mass Flow of WF')

pyplot.figure('Entropy Change vs. Mass Flow of WF')
pyplot.plot(_mdot, _s12, label="Storage")
pyplot.plot(_mdot, _s23, label="Pump")
pyplot.plot(_mdot, _s34, label="Radiator")
pyplot.plot(_mdot, _s41, label="Throttle")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Entropy Change (J/kg-K)')
pyplot.title('Entropy Change vs. Mass Flow of WF')

pyplot.figure('Radiator Effectiveness vs. Mass Flow of WF')
pyplot.plot(_mdot, _e_Rad)
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Effectiveness')
pyplot.title('Effectiveness vs. Mass Flow of WF')

pyplot.figure('WF Velocities vs. Mdot WF')
pyplot.plot(_mdot, _Vel_Liq, label="Liquid")
pyplot.plot(_mdot, _Vel_Gas, label="Gas")
pyplot.legend()
pyplot.xlabel('Mass Flow of Working Fluid (kg/s)')
pyplot.ylabel('Velocity of WF (m/s)')
pyplot.title('WF Velocities vs. Mdot WF')
pyplot.tight_layout()
pyplot.savefig('IILawEff.jpg')
