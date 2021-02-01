#------------------------------------------------------------------------------------------------------------------------------------------
# Input:    Input_directory: the folder that include the AFO input design DesignParameters
             #  Input_file: the text file including the design parameters of AFO: AFO input.txt
# Output:     AFO_representation: the local coordinates of the two endpoints for the AFO strips
                # AFO_material: the force magnitude and force-length relationship for the AFO strips in side and front
                # Platform_inclination: the inclination of the platform
def AFODesignParameter(Input_directory, Input_file):
    import os
    import math
    import numpy as np
    # Get the full path of the directory and .txt file for the input parameters
    path_script = os.path.realpath(__file__)                                                                                              # The full document path of the python scrip
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder for the python script: python simulation
    File_AFOinput=os.path.join(path_simulation, Input_directory, Input_file)                                       # The text file including the AFO design parameters: AFO input.txt
    # Collect the design parameters from the .txt file and assign to them to the matrix (DesignParameters), using the module (AFOParameterInput)
    DesignParameters=AFOParameterInput(File_AFOinput)                                                                  # The AFO design parameters collected from the parameters file: AFO input.txt
    # DesignParameters = [wrapCylinder_location, wrapCylinder_radius, wrapEllipsoid_location, wrapEllipsoid_dim, wrapEllipsoid_Orinentation,
    #                                     AFO_side_top_iniPosAngle, AFO_side_top_rangeAngle, AFO_side_bottom_iniPosAngle, AFO_side_bottom_rangeAngle,
    #                                     AFO_front_top_iniPosAngle, AFO_front_top_rangeAngle, AFO_front_bottom_iniPosAngle, AFO_front_bottom_rangeAngle,
    #                                     AFO_height, num_side, num_front, AFO_FLrelationship_side, AFO_FLrelationship_front, Platform_inclination, AFO_material_strength, AFO_strip_dia]
    AFO_Fmagnitude=DesignParameters[19]*(math.pi*((DesignParameters[20]/2)**2))                     # The force magnitude for the material properties in the MBD model, calculated by material strength and size
    # Get the local coordinate values of endpoints and the lengths of the AFO strips, using the module (AFORepresentation)
    # AFO_representation=[AFO_top_local, AFO_bottom_local, AFO_length]
    AFO_representation=AFORepresentation(DesignParameters)
    # AFO_material=[AFO_Fmagnitude_side, DesignParameters_side, AFO_Fmagnitude_front, DesignParameters_front]
    AFO_material=[AFO_Fmagnitude, DesignParameters[16], AFO_Fmagnitude, DesignParameters[17]]
    Platform_inclination=DesignParameters[18]
    return AFO_representation, AFO_material, Platform_inclination

#------------------------------------------------------------------------------------------------------------------------------------------
# Collect AFO design parameters from the file File_AFO input.txt
# File_AFOinput: a text file containing the design parameters for AFO
def AFOParameterInput(File_AFOinput):
    import re
    import numpy as np
    with open(File_AFOinput) as f:
        lines=f.readlines()
    dataset=[]
    for line in lines:
        line=" ".join(line.strip().split('\t'))
        dataset.append(line)
    # Line 0: the location of top wrap cylinder
    wrapCylinder_location=re.compile('-?\d+\.*\d*').findall(dataset[0])
    wrapCylinder_location=np.array(wrapCylinder_location, dtype=np.float)
    # Line 1: the radius of top wrap cylinder
    wrapCylinder_radius=float(re.findall(r"\d+\.?\d*",dataset[1])[0])
    # Line 2: the location of bottom ellipsoid
    wrapEllipsoid_location=re.compile('-?\d+\.*\d*').findall(dataset[2])
    wrapEllipsoid_location=np.array(wrapEllipsoid_location, dtype=np.float)
    # Line 3: the dimensions of the bottom wrap ellipsoid
    wrapEllipsoid_dim=re.compile('-?\d+\.*\d*').findall(dataset[3])
    wrapEllipsoid_dim=np.array(wrapEllipsoid_dim, dtype=np.float)
    # Line 4: the orientation of the bottom wrap ellipsoid
    wrapEllipsoid_Orinentation=re.compile('-?\d+\.*\d*').findall(dataset[4])
    wrapEllipsoid_Orinentation=np.array(wrapEllipsoid_Orinentation, dtype=np.float)
    # Line 5: the initial position of the first end points of AFO in top, defined using angles in a circular reference system
    AFO_side_top_iniPosAngle=int(re.findall(r"\d+\.?\d*",dataset[5])[0])
    # Line 6: the widths of the AFO strips in side, defined using range of the angles in a circular reference system
    AFO_side_top_rangeAngle=int(re.findall(r"\d+\.?\d*",dataset[6])[0])
    # Line 7: the initial position of the first end points of AFO on bottom, defined using angles in a ellipsoid reference system
    AFO_side_bottom_iniPosAngle=int(re.findall(r"\d+\.?\d*",dataset[7])[0])
    # Line 8: the widths of the AFO strips in side, defined using range of the angles in a ellipsoid reference system
    AFO_side_bottom_rangeAngle=int(re.findall(r"\d+\.?\d*",dataset[8])[0])
    # Line 9: the initial position of the first end points of AFO in front of top, defined using angles in a circular reference system
    AFO_front_top_iniPosAngle=int(re.findall(r"\d+\.?\d*",dataset[9])[0])
    # Line 10: the widths of the AFO strips in front, defined using range of the angles in a circular reference system
    AFO_front_top_rangeAngle=int(re.findall(r"\d+\.?\d*",dataset[10])[0])
    # Line 11: the initial position of the first end points of AFO on front bottom, defined using angles in a ellipsoid reference system
    AFO_front_bottom_iniPosAngle=int(re.findall(r"\d+\.?\d*",dataset[11])[0])
    # Line 12: the widths of the AFO strips on front bottom, defined using range of the angles in a ellipsoid reference system
    AFO_front_bottom_rangeAngle=int(re.findall(r"\d+\.?\d*",dataset[12])[0])
    # Line 13: the height of the AFO
    AFO_height=float(re.findall(r"\d+\.?\d*",dataset[13])[0])
    # Line 14: the number of the AFO strips in side
    num_side=int(re.findall(r"\d+\.?\d*",dataset[14])[0])
    # Line 15: the number of the AFO strips in front
    num_front=int(re.findall(r"\d+\.?\d*",dataset[15])[0])
    # Line 16: the force-length relationship for the AFO material in AFO side
    AFO_FLrelationship_side=re.compile('-?\d+\.*\d*').findall(dataset[16])
    AFO_FLrelationship_side=np.array(AFO_FLrelationship_side,dtype=np.float).reshape(2,-1)
    # Line 17: the force-length relationship for the AFO material in AFO front
    AFO_FLrelationship_front=re.compile('-?\d+\.*\d*').findall(dataset[17])
    AFO_FLrelationship_front=np.array(AFO_FLrelationship_front,dtype=np.float).reshape(2,-1)
    # Line 18: the inclination of the platform
    Platform_inclination=re.compile('-?\d+\.*\d*').findall(dataset[18])
    Platform_inclination=np.array(Platform_inclination,dtype=np.float)
    # Line 19: strength of the AFO material
    AFO_material_strength=float(re.findall(r"\d+\.?\d*",dataset[19])[0])
    # Line 20: the radius of AFO strips
    AFO_strip_dia=float(re.findall(r"\d+\.?\d*",dataset[20])[0])
    return wrapCylinder_location, wrapCylinder_radius, wrapEllipsoid_location, wrapEllipsoid_dim, wrapEllipsoid_Orinentation, AFO_side_top_iniPosAngle, AFO_side_top_rangeAngle, AFO_side_bottom_iniPosAngle, AFO_side_bottom_rangeAngle, AFO_front_top_iniPosAngle, AFO_front_top_rangeAngle, AFO_front_bottom_iniPosAngle, AFO_front_bottom_rangeAngle, AFO_height, num_side, num_front, AFO_FLrelationship_side, AFO_FLrelationship_front, Platform_inclination, AFO_material_strength, AFO_strip_dia

#------------------------------------------------------------------------------------------------------------------------------------------
# Create the end points of the AFO strips in global and local coordinate system
# Input: design parameters collected from the AFO input.txt file
# Output: The coordinates values of endpoints of AFO strips in global and local coordinate systems
                # AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
                # AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
                # AFO_length=[AFO_length_side, AFO_length_front]
def AFORepresentation(DesignParameter):
    import math
    import numpy as np
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The design parameters for AFO in the MBD model, collected from the AFO input.txt file
    wrapCylinder_location=DesignParameter[0]
    wrapCylinder_radius=DesignParameter[1]
    wrapEllipsoid_location=DesignParameter[2]
    wrapEllipsoid_dim=DesignParameter[3]
    wrapEllipsoid_Orinentation=DesignParameter[4]
    AFO_side_top_iniPosAngle=DesignParameter[5]                                  # The initial position of the AFO strip in two sides of the foot, the position can be determined using ellipse angle
    AFO_side_top_rangeAngle=DesignParameter[6]
    AFO_side_bottom_iniPosAngle=DesignParameter[7]
    AFO_side_bottom_rangeAngle=DesignParameter[8]                                                       # The width of the AFO strip in two sides of the foot, is determined using ellipse angle
    AFO_front_top_iniPosAngle=DesignParameter[9]                                              # The initial position of the AFO strip in front sides of the foot, the position can be determined using ellipse angle
    AFO_front_top_rangeAngle=DesignParameter[10]
    AFO_front_bottom_iniPosAngle=DesignParameter[11]
    AFO_front_bottom_rangeAngle=DesignParameter[12]                                                      # The width of the AFO strip in front sides of the foot, is determined using ellipse angle
    AFO_height=DesignParameter[13]
    num_side=DesignParameter[14]                                                                               # The number of AFO strips in two sides of the foot
    num_front=DesignParameter[15]                                                                              # The number of AFO strips in front side of the foot
    # Transfer the AFO design parameters definition from angle to the radians
    [AFO_side_top_iniPosAngle, AFO_side_top_rangeAngle]=[AFO_side_top_iniPosAngle/180*math.pi, AFO_side_top_rangeAngle/180*math.pi]
    [AFO_side_bottom_iniPosAngle, AFO_side_bottom_rangeAngle]=[AFO_side_bottom_iniPosAngle/180*math.pi, AFO_side_bottom_rangeAngle/180*math.pi]
    [AFO_front_top_iniPosAngle, AFO_front_top_rangeAngle]=[AFO_front_top_iniPosAngle/180*math.pi, AFO_front_top_rangeAngle/180*math.pi]
    [AFO_front_bottom_iniPosAngle, AFO_front_bottom_rangeAngle]=[AFO_front_bottom_iniPosAngle/180*math.pi, AFO_front_bottom_rangeAngle/180*math.pi]

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The ellipsoid wrap surface in the calcn, the AFO at the bottom (ground coordinate system)
    # The AFO on the left and right sides of the foot_bottom
    theta_wrapEllipsoid=wrapEllipsoid_Orinentation                                                     # The rotation of the ellipsoid wrap surface about calcn coordinate system
    location_wrapEllipsoid=wrapEllipsoid_location                                                       # The location of the origin of the ellipsoid wrap surface on the ground coordinate system
    dim_wrapEllipsoid=wrapEllipsoid_dim                                                                   # The dimensions of the ellipsoid wrap surface
    AFO_bottomside_left=AFO_bottomside_right=[]
    for i in range (int(num_side)):
        # AFO strips in the left side of the foot_bottom
        x_left=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos(AFO_side_bottom_iniPosAngle+AFO_side_bottom_rangeAngle/num_side*i)
        y_left=location_wrapEllipsoid[1]
        z_left=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin(AFO_side_bottom_iniPosAngle+AFO_side_bottom_rangeAngle/num_side*i)
        AFO_bottomside_left=np.append(AFO_bottomside_left, np.array([x_left,y_left,z_left]))
        #AFO strips in the right side of the foot_bottom
        #x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((2*math.pi-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        y_right=location_wrapEllipsoid[1]
        #z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((2*math.pi-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((-AFO_side_bottom_iniPosAngle)-AFO_side_bottom_rangeAngle/num_side*i)
        AFO_bottomside_right=np.append(AFO_bottomside_right, np.array([x_right,y_right,z_right]))
    AFO_bottomside_left=AFO_bottomside_left.reshape(-1,3)
    AFO_bottomside_right=AFO_bottomside_right.reshape(-1,3)

    # The AFO on the front sides of the foot_bottom
    AFO_bottomfront_left=AFO_bottomfront_right=[]
    for i in range (num_front):
        # AFO strips in the left front of the foot_bottom
        x_left=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos(AFO_front_bottom_iniPosAngle+AFO_front_bottom_rangeAngle/num_front*i)
        y_left=location_wrapEllipsoid[1]
        z_left=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin(AFO_front_bottom_iniPosAngle+AFO_front_bottom_rangeAngle/num_front*i)
        AFO_bottomfront_left=np.append(AFO_bottomfront_left, np.array([x_left,y_left,z_left]))
        #AFO strips in the right front of the foot_bottom
        x_right=location_wrapEllipsoid[0]+dim_wrapEllipsoid[0]*math.cos((2*math.pi-AFO_front_bottom_iniPosAngle)-AFO_front_bottom_rangeAngle/num_front*i)
        y_right=location_wrapEllipsoid[1]
        z_right=location_wrapEllipsoid[2]+dim_wrapEllipsoid[2]*math.sin((2*math.pi-AFO_front_bottom_iniPosAngle)-AFO_front_bottom_rangeAngle/num_front*i)
        AFO_bottomfront_right=np.append(AFO_bottomfront_right, np.array([x_right,y_right,z_right]))
    AFO_bottomfront_left=AFO_bottomfront_left.reshape(-1,3)
    AFO_bottomfront_right=AFO_bottomfront_right.reshape(-1,3)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The cylinder wrap surface in the tibia, the AFO at the top (ground coordinate system)
    #location_wrapCylinder=np.array([-0.0084,-0.4657,0.0067])                            # The center of the circle at the bottom of the wrap Cylinder (tibia coordinate system)
    location_wrapCylinder=wrapCylinder_location                                                  # The center of teh circle at the bottome in ground coordinate system
    radius=wrapCylinder_radius                                                                                # The radius of the circle for the wrap Cylinder
    AFO_height=AFO_height                                                                                     # The length of the AFO length
    # The AFO on the left and right sides of the foot_top
    AFO_topside_left=AFO_topside_right=[]
    for i in range (num_side):
        # AFO strips in the left side of the foot_top
        x_left=location_wrapCylinder[0]+radius*math.cos(AFO_side_top_iniPosAngle+AFO_side_top_rangeAngle/num_side*i)
        y_left=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_left=location_wrapCylinder[2]+radius*math.sin(AFO_side_top_iniPosAngle+AFO_side_top_rangeAngle/num_side*i)
        AFO_topside_left=np.append(AFO_topside_left, np.array([x_left,y_left,z_left]))
        # AFO strips in the right side of the foot_top
        x_right=location_wrapCylinder[0]+radius*math.cos((2*math.pi-AFO_side_top_iniPosAngle)-AFO_side_top_rangeAngle/num_side*i)
        y_right=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_right=location_wrapCylinder[2]+radius*math.sin((2*math.pi-AFO_side_top_iniPosAngle)-AFO_side_top_rangeAngle/num_side*i)
        AFO_topside_right=np.append(AFO_topside_right, np.array([x_right,y_right,z_right]))
    AFO_topside_left=AFO_topside_left.reshape(-1,3)
    AFO_topside_right=AFO_topside_right.reshape(-1,3)

    # The AFO on the front sides of the foot_top
    AFO_topfront_left=AFO_topfront_right=[]
    for i in range (num_front):
        # AFO strips in the left side of the foot_top
        x_left=location_wrapCylinder[0]+radius*math.cos(AFO_front_top_iniPosAngle+AFO_front_top_rangeAngle/num_front*i)
        y_right=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_left=location_wrapCylinder[2]+radius*math.sin(AFO_front_top_iniPosAngle+AFO_front_top_rangeAngle/num_front*i)
        AFO_topfront_left=np.append(AFO_topfront_left, np.array([x_left,y_left,z_left]))
        # AFO strips in the right side of the foot_top
        x_right=location_wrapCylinder[0]+radius*math.cos((2*math.pi-AFO_front_top_iniPosAngle)-AFO_front_top_rangeAngle/num_front*i)
        y_left=location_wrapEllipsoid[1]+AFO_height                                             # The y coordinate of the AFO of top surface eaqual to bottom surface + AFO height
        z_right=location_wrapCylinder[2]+radius*math.sin((2*math.pi-AFO_front_top_iniPosAngle)-AFO_front_top_rangeAngle/num_front*i)
        AFO_topfront_right=np.append(AFO_topfront_right, np.array([x_right,y_right,z_right]))
    AFO_topfront_left=AFO_topfront_left.reshape(-1,3)
    AFO_topfront_right=AFO_topfront_right.reshape(-1,3)

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # The length of the AFO strips in right, left and front sides
    # Top surface: AFO_topside_left, AFO_topside_right, AFO_topfront_left, AFO_topfront_right
    # Bottom surface: AFO_bottomside_left, AFO_bottomside_right, AFO_bottomfront_left, AFO_bottomfront_right
    # The length of strips in AFO sides
    AFO_side_left_length=AFO_side_right_length=[]
    for i in range (num_side):
        AFO_side_left_length_T=np.sqrt(np.sum(np.square(AFO_topside_left[i]-AFO_bottomside_left[i])))
        AFO_side_left_length=np.append(AFO_side_left_length, AFO_side_left_length_T)
        AFO_side_right_length_T=np.sqrt(np.sum(np.square(AFO_topside_right[i]-AFO_bottomside_right[i])))
        AFO_side_right_length=np.append(AFO_side_right_length,AFO_side_right_length_T)
    # The length of strips in AFO front
    AFO_front_left_length=AFO_front_right_length=[]
    for i in range (num_front):
        AFO_front_left_length_T=np.sqrt(np.sum(np.square(AFO_topfront_left[i]-AFO_bottomfront_right[i])))                      # The length of AFO strip in front, top left to bottom right (top left-bottom right)
        AFO_front_left_length=np.append(AFO_front_left_length, AFO_front_left_length_T)
        AFO_front_right_length_T=np.sqrt(np.sum(np.square(AFO_topfront_right[i]-AFO_bottomfront_left[i])))                    # The length of AFO strip in front, top right to bottom left (top right-bottom left)
        AFO_front_right_length=np.append(AFO_front_right_length, AFO_front_right_length_T)

    AFO_top_global_side=np.vstack((AFO_topside_left, AFO_topside_right))
    AFO_top_global_front=np.vstack((AFO_topfront_left, AFO_topfront_right))
    AFO_bottom_global_side=np.vstack((AFO_bottomside_left, AFO_bottomside_right))
    AFO_bottom_global_front=np.vstack((AFO_bottomfront_right, AFO_bottomfront_left))
    AFO_strip_length_side=np.append(AFO_side_left_length, AFO_side_right_length)
    AFO_strip_length_front= np.append(AFO_front_left_length, AFO_front_right_length)
    AFO_strip_length_side=AFO_strip_length_side
    AFO_strip_length_front=AFO_strip_length_front

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Transfer the endpoints of AFO strips from global coordinate system to local coordinate systems
    tibial_center = np.array([-0.0752, -0.4619, 0.0835])                                                                                              # tibial center coordinates in MBD model in global coordinate system
    calcn_center = np.array([-0.1240, -0.9339, 0.0914])                                                                                             # calcn center coordinates in MBD model in global coordinate system
    # The AFO strip in the AFO side
    [AFO_top_local_side, AFO_bottom_local_side, AFO_length_side]=MBDGlobalToLocal(AFO_top_global_side, AFO_bottom_global_side, AFO_strip_length_side, tibial_center, calcn_center)
    # The AFO strip in the AFO front
    [AFO_top_local_front, AFO_bottom_local_front, AFO_length_front]=MBDGlobalToLocal(AFO_top_global_front, AFO_bottom_global_front, AFO_strip_length_front, tibial_center, calcn_center)
    # Put the AFO strips in AFO side and front together
    AFO_top_local=[AFO_top_local_side, AFO_top_local_front]
    AFO_bottom_local=[AFO_bottom_local_side, AFO_bottom_local_front]
    AFO_length=[AFO_length_side, AFO_length_front]
    return AFO_top_local, AFO_bottom_local, AFO_length

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
def MBDGlobalToLocal(AFO_top, AFO_bottom, AFO_length, tibial_center, calcn_center):
    import numpy as np
    # AFO_top_tibia: The matrix representing coordinate values of the points on the top of the AFO strips in tibial local coordinate system
    # AFO_bottom_calcn: The matrix representing coordinate values of the points at the bottom of the AFO strips in the calcn local coordinate system
    # The tibial local coordinate systems
    # tibial_center=np.array([-0.0752, -0.46192,0.0835])
    tibial_x=np.array([1,0,0])
    tibial_y=np.array([0,1,0])
    tibial_z=np.array([0,0,1])
    tibial_vector=np.array([tibial_x,tibial_y,tibial_z])

    # The calcn local coordinate systems
    # calcn_center=np.array([-0.12397,-0.93387,0.09142])
    calcn_x=np.array([1,0,0])
    calcn_y=np.array([0,1,0])
    calcn_z=np.array([0,0,1])
    calcn_vector=np.array([calcn_x,calcn_y,calcn_z])

    # The transformation from global coordinate system to the local coordiante systems
    AFO_top_tibial=np.array(transformation(AFO_top,tibial_center,tibial_vector))
    AFO_bottom_calcn=np.array(transformation(AFO_bottom,calcn_center,calcn_vector))
    return AFO_top_tibial, AFO_bottom_calcn, AFO_length

#--------------------------------------------------------------------------------------------------------------------------
# Matrix operations: Dot，Cross and Normalization
# input arguments for Dot and Cross: two matrix, i.e. M1=[1.0,2.0,3.0],M2=[2.0,4.0,7.0]
# input argument for Normalization: one matrix, i.e. M=[1,2,3]
class MatrixOperation:
    def Dot(M1,M2):
        return M1[0]*M2[0]+M1[1]*M2[1]+M1[2]*M2[2]
    def Cross(M1,M2):
        return [M1[1]*M2[2]-M1[2]*M2[1],-(M1[0]*M2[2]-M1[2]*M2[0]),M1[0]*M2[1]-M1[1]*M2[0]]
    def Norm(M):
        sqrt=pow((pow(M[0],2)+pow(M[1],2)+pow(M[2],2)),0.5)
        return sqrt
    def Sub(M1,M2):
        M=[]
        T=[]
        for i in range(len(M1)):
            for j in range(len(M1[0])):
                T.append(M1[i][j]-M2[i][j])
            M.append(T)
            T=[]
        return M

#--------------------------------------------------------------------------------------------------------------------------
# Matrix transformation between two coordinate systems
# input arguments: two matrix: M1(n*4 matrix): the original matrix,
                         # M2(1*3 matrix): the origin of the new (local) coordinate system
                         # M3(3*3 matrix): the x,y,z vectors of the new (local) coordinate system
def transformation(M_origin,Coord_local_origin,Coord_local_vector):
        x_global=[1,0,0]
        y_global=[0,1,0]
        z_global=[0,0,1]
        x_local=Coord_local_vector[0]
        y_local=Coord_local_vector[1]
        z_local=Coord_local_vector[2]
        MO=MatrixOperation
        cos_x_local_x_global=MO.Dot(x_local,x_global)/(MO.Norm(x_local)*MO.Norm(x_global))
        cos_x_local_y_global=MO.Dot(x_local,y_global)/(MO.Norm(x_local)*MO.Norm(y_global))
        cos_x_local_z_global=MO.Dot(x_local,z_global)/(MO.Norm(x_local)*MO.Norm(z_global))

        cos_y_local_x_global=MO.Dot(y_local,x_global)/(MO.Norm(y_local)*MO.Norm(x_global))
        cos_y_local_y_global=MO.Dot(y_local,y_global)/(MO.Norm(y_local)*MO.Norm(y_global))
        cos_y_local_z_global=MO.Dot(y_local,z_global)/(MO.Norm(y_local)*MO.Norm(z_global))

        cos_z_local_x_global=MO.Dot(z_local,x_global)/(MO.Norm(z_local)*MO.Norm(x_global))
        cos_z_local_y_global=MO.Dot(z_local,y_global)/(MO.Norm(z_local)*MO.Norm(y_global))
        cos_z_local_z_global=MO.Dot(z_local,z_global)/(MO.Norm(z_local)*MO.Norm(z_global))
        M_new=[]
        T=[]
        M1=M_origin
        M2=Coord_local_origin
        for i in range(len(M1)):
            T=[(M1[i][0]-M2[0])*cos_x_local_x_global+(M1[i][1]-M2[1])*cos_x_local_y_global+(M1[i][2]-M2[2])*cos_x_local_z_global,
                (M1[i][0]-M2[0])*cos_y_local_x_global+(M1[i][1]-M2[1])*cos_y_local_y_global+(M1[i][2]-M2[2])*cos_y_local_z_global,
                (M1[i][0]-M2[0])*cos_z_local_x_global+(M1[i][1]-M2[1])*cos_z_local_y_global+(M1[i][2]-M2[2])*cos_z_local_z_global
                ]
            M_new.append(T)
            T=[]
        return M_new
