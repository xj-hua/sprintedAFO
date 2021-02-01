
def DoESimulation (Level_A, Level_B, Level_C, Level_D, Operation, ResultDirectory):
    import AFO0_Simulation
    DoEFactorLevel (Level_A, Level_B, Level_C, Level_D)
    AFO0_Simulation.Simulation('AFODroplanding', Operation, ResultDirectory)

#---------------------------------------------------------------------------------------------------------------------------------------------
# Perform Design of Experiments and Simulation
# Input:  Level_A: the level for the force-length relationship for AFO in side (amplification): Level_A==1: high level, Level_A==-1: low
            # Level_B: the level for the force-length relationship for AFO in side (shift)
            # Level_C: the level for the force-length relationship for AFO in front (amplification)
            # Level_D: the level for the force-length relationship for AFO in side (shift)
def DoEFactorLevel(Level_A, Level_B, Level_C, Level_D):
    import AFO3_ParaTestSelect
    # The level for the force-length relationship for AFO in side (amplification) (low: level=-1, high: level=1)
    AFO_FLrelationship_side=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship_side')
    AFO_FLrelationship_front=AFO3_ParaTestSelect.ParaTestValue('AFO Design', 'AFO input_default.txt', 'AFO_FLrelationship_front')
    if Level_A==0:                                                       # low level
        AFO_FLrelationship_side[1]=AFO_FLrelationship_side[1]
    elif Level_A==1:                                                      # high level
        AFO_FLrelationship_side[1]=AFO_FLrelationship_side[1]*5

    # The level for the force-length relationship for AFO in side (shift) (low: level=-1, high: level=1)
    if Level_B==0:                                                       # low level
        AFO_FLrelationship_side[0]=AFO_FLrelationship_side[0]
    elif Level_B==1:                                                      # high level
        AFO_FLrelationship_side[0]=AFO_FLrelationship_side[0]-0.2

    # The level for the force-length relationship for AFO in side (amplification) (low: level=-1, high: level=1)
    if Level_C==0:
        AFO_FLrelationship_front[1]=AFO_FLrelationship_front[1]
    elif Level_C==1:
        AFO_FLrelationship_front[1]=AFO_FLrelationship_front[1]*5

    # The level for the force-length relationship for AFO in front (shift) (low: level=-1, high: level=1)
    if Level_D==0:                                                       # low level
        AFO_FLrelationship_front[0]=AFO_FLrelationship_front[0]
    elif Level_D==1:                                                      # high level
        AFO_FLrelationship_front[0]=AFO_FLrelationship_front[0]-0.2

    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input_default.txt', 'AFO input.txt', 'AFO_FLrelationship_side', AFO_FLrelationship_side)
    AFO3_ParaTestSelect.ParaValeModification('AFO Design', 'AFO input.txt', 'AFO input.txt', 'AFO_FLrelationship_front', AFO_FLrelationship_front)
