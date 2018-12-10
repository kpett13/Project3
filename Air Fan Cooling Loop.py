# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 18:33:10 2018

@author: kpett
"""

import cantera as ct 
from matplotlib import pyplot


"Define Fluids"
air_1 = ct.Solution('air.cti')
air_2 = ct.Solution('air.cti')

"Knowns"
T1_air = 38+273.15        # T1 ambient = 38C
P1_air = 1*10**5          # P1 ambient = 1 bar
T2_air = 10+273.15        # T2 into cabin = 10C
P2_air = P1_air           # P2 = 1 bar
air_1.TP = T1_air,P1_air  # Define state
air_2.TP = T2_air,P2_air  # Define state
h1_air = air_1.h          
h2_air = air_2.h 

Q = []
W = []
vel = []
COP = []
W_max = 48
vol_dot_max = 595  
m_dot_out = vol_dot_max*air_1.density*1/3600
q_cabin = m_dot_out*(air_1.h-air_2.h)
Ac = 0.00064516*9.5

for v in range (0,60):
    vel.append(v)
    v_mhr = 1609.34*v
    m_dot_in = Ac*v_mhr*air_1.density*1/3600
    delta_m_dot = m_dot_out-m_dot_in    
    W_fan = delta_m_dot*(W_max/m_dot_out)
    COP.append(q_cabin/W_fan)
    W.append (W_fan)
    Q.append(q_cabin)
    
pyplot.figure('COP vs. Vehicle Speed')
pyplot.plot(vel, COP)
pyplot.xlabel('Velocity (mph)')
pyplot.ylabel('COP')
pyplot.title('COP vs. Vehicle Speed')
    
pyplot.figure('Heat vs. Vehicle Speed')
pyplot.plot(vel, Q)
pyplot.xlabel('Velocity (mph)')
pyplot.ylabel('Heat (W)')
pyplot.title('Heat vs. Vehicle Speed')
    
pyplot.figure('Fan Power vs. Vehicle Speed')
pyplot.plot(vel, W)
pyplot.xlabel('Velocity (mph)')
pyplot.ylabel('Fan Power (W)')
pyplot.title('Fan Power vs. Vehicle Speed')
    
    