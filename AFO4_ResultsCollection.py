# output_folder='SimulationOutput_AFO_FLrelationship0'
# Results_parameter=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
def Droplandingresultscollection(output_folder, Results_parameter):
    import numpy as np
    import math
    import os
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    DL_results_directory=os.path.join(path_simulation, 'Drop landing', output_folder)
    DL_results="default_states_degrees.mot"
    #directory=os.path.join(path, results_directory)
    if not os.path.isdir(DL_results_directory):
        print("No specified directory found, please create one!")
        # os.makedirs(directory)
    results_file_initial=os.path.join(DL_results_directory, DL_results)
    if not os.path.exists(results_file_initial):
        print("No specified file found, please check! ")

    npos=[]
    AFO_POI=[]
    with open (results_file_initial,"r",encoding="utf-8") as f:
        lines=f.readlines()
    with open (os.path.join(DL_results_directory,'Results_file_final.txt'),"w",encoding="utf-8") as f_w:
        for line in lines:
            linestr=line.strip()
            if len(linestr)==0:
                continue
            if linestr.startswith('time'):
                strlist=linestr.split('\t')
                print(strlist)
                for i in range(len(Results_parameter)):
                    npos.append(strlist.index(Results_parameter[i]))
                    f_w.writelines([strlist[npos[i]],"  "])
                f_w.writelines("\n")
            elif linestr[0].isdigit():
                strlist=linestr.split('\t')
                for j in range(len(npos)):
                    f_w.writelines(strlist[npos[j]])
                    AFO_POI.append(float(strlist[npos[j]]))
                f_w.writelines("\n")
    AFO_POI=np.array(AFO_POI).reshape(-1,len(Results_parameter))
    return AFO_POI


#------------------------------------------------------------------------------------------------------------------------------------------
# Export the MBD simulation results into excel file
# Input: # File_folder: The folder for the MBD results that include the excel file, default='MBD Results'
              # File_excel: the name of the results excel, default='MBD Results'
              # output_folder: the name of the sheet, e.g. output_folder='SimulationOutput_AFO_FLrelationship0'
              # Results_parameter: the results of interest that will be stored to the excel file, defualt=['time', '/jointset/subtalar_r/subtalar_angle_r/value', '/jointset/subtalar_r/subtalar_angle_r/speed']
              # data: the matrix of data that will be stored into the excel file
def DLResultstoExcel(File_folder, File_excel, output_folder, Results_parameter, data):
    import os
    import numpy as np
    import xlwt, xlrd
    from xlutils.copy import copy as xl_copy
    # The folder path of pthon script
    path_script = os.path.realpath(__file__)                                                                                              # The full path for the python scrip folder: python script
    path_simulation=os.path.dirname(os.path.dirname(path_script))                                                       # The path of the folder including the python script: python simulation
    # The joining of the folders python simulation, drop landing (DL) and output folders
    DL_results_directory=os.path.join(path_simulation, 'Drop landing', File_folder)
    if not os.path.isdir(DL_results_directory):
        print("No specified directory found, please create one!")
        os.makedirs(DL_results_directory)
    DL_results_file=os.path.join(DL_results_directory, File_excel)

    if not os.path.exists(DL_results_file):
        f=xlwt.Workbook()
        sheet_output_folder=f.add_sheet('%s' %(output_folder), cell_overwrite_ok=True)
    else:
        rb=xlrd.open_workbook(DL_results_file, formatting_info=True)
        f=xl_copy(rb)
        sheet_output_folder=f.add_sheet('%s' %(output_folder))

    [h, l]=data.shape
    for i in range(h+1):
        if i==0:
            for j in range(len(Results_parameter)):
                sheet_output_folder.write(i,j,Results_parameter[j])
        else:
            for j in range (l):
                sheet_output_folder.write(i,j,data[i-1,j])
    f.save(DL_results_file)
