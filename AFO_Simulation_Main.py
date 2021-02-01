import AFO0_Simulation
import AFO1_DesignParameter
import os
import AFO2_MBDModel
import AFO3_ParaTestSelect
import numpy as np
import AFO4_ResultsCollection
import AFO5_DoE
#AFO0_Simulation.GaitSimulation('Walk')                                                                                                         # Perform walk gait simulation, including scaling, inverse dynamics, RRA, CMC, forward dynamics
#AFO0_Simulation.GaitSimulation('Gait_AFO')

for i in range (2):
    for j in range (2):
        for m in range (2):
            for n in range (2):
                ResultDirectory='SimulationOutput_DOE_'+str(i)+str(j)+str(m)+str(n)
                AFO5_DoE.DoESimulation(i, j, m, n, 'simulation', ResultDirectory)

"""
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship')
for i in range (5):
    AFO_FLrelationship[0]=AFO_FLrelationship[0]-0.1*(i+1)
    print(AFO_FLrelationship[0])
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship')
for i in range (2):
    AFO_FLrelationship[0]=AFO_FLrelationship[0]-0.1*(i+1)
    print(AFO_FLrelationship[0])
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'model', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For force-length relationship_amplification
AFO_FLrelationship=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'AFO_FLrelationship')
for i in range (10):
    AFO_FLrelationship[1]=AFO_FLrelationship[1]*(i/20+1)
    print(AFO_FLrelationship[1])
    ResultDirectory='SimulationOutput_'+'AFO_FLrelationship'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_FLrelationship', AFO_FLrelationship)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
#--------------------------------------------------------------------------------------------------------------------------------------------
# For number of strips in side
num_side=int(AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'num_side'))
for i in range (5):
    print(num_side)
    ResultDirectory='SimulationOutput_'+'num_side'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'num_side', num_side)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
    num_side=num_side+1
#--------------------------------------------------------------------------------------------------------------------------------------------
# For number of strips in front
num_front=int(AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'num_front'))
for i in range (5):
    print(num_front)
    ResultDirectory='SimulationOutput_'+'num_front'+str(i)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'num_front', num_front)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation', ResultDirectory)
    num_front=num_front+1
Platform_inclination=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
Inclination_increment=[5,0,0]
for i in range (2):
    Platform_inclination=Platform_inclination+Inclination_increment
    print(Platform_inclination)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'Platform_inclination', Platform_inclination)
    AFO0_Simulation.Simulation('AFODroplanding', 'model')
AFO_side_top_iniPosAngle=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
angle_increment=1
for i in range (10):
    AFO_side_top_iniPosAngle=AFO_side_top_iniPosAngle+angle_increment
    print(AFO_side_top_iniPosAngle)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_side_top_iniPosAngle', AFO_side_top_iniPosAngle)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation')
AFO_side_bottom_iniPosAngle=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input.txt', 'Platform_inclination')
angle_increment=1
for i in range (10):
    AFO_side_bottom_iniPosAngle=AFO_side_bottom_iniPosAngle+angle_increment
    print(AFO_side_bottom_iniPosAngle)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO_side_bottom_iniPosAngle', AFO_side_bottom_iniPosAngle)
    AFO0_Simulation.Simulation('AFODroplanding', 'simulation')
"""
"""
output_folder_prefix='num_side'
for i in range (0,5):
    output_folder=output_folder_prefix+str(i)
    #Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
    Results_parameter=['time', '/jointset/ankle_r/ankle_angle_r/value']
    data= AFO4_ResultsCollection.Droplandingresultscollection(output_folder, Results_parameter)
    AFO4_ResultsCollection.DLResultstoExcel('MBD Results', 'DL Results11.xls', output_folder, Results_parameter, data)
"""
