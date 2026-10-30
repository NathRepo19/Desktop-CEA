from rocketcea.cea_obj import CEA_Obj
from solver.data_class_custom import CalcSet,ChoiceSet
from solver.calc_engine import compute_val,mono_prop_compute_val
import numpy as np 
import matplotlib.pyplot as plt
import copy 


def loop_func(data_obj:CalcSet,calc_ch:ChoiceSet,of_low,of_high,of_num):
    
    of_list = np.linspace(of_low,of_high,int(of_num))
    data_list = []
    for of in of_list: 
        current_obj = copy.deepcopy(data_obj)  
        current_obj.of_ratio = of
        current_obj = compute_val(current_obj, calc_ch)
        data_list.append(current_obj)

    return data_list

def loop_func_ch_pressure(data_obj:CalcSet,calc_ch:ChoiceSet,pc_low,pc_high,pc_num):
    ch_pressure_list = np.linspace(pc_low,pc_high,int(pc_num))
    data_list = []  
    for pc in ch_pressure_list: 
        current_obj = copy.deepcopy(data_obj)
        current_obj.chamber_pressure = pc
        if current_obj.of_ratio is not None: 
            current_obj = compute_val(current_obj,calc_ch)
        else:
            current_obj = mono_prop_compute_val(current_obj,calc_ch)
        
        data_list.append(current_obj)
    return data_list 


 
def loop_func_nozzle_ratio(data_obj:CalcSet,calc_ch:ChoiceSet,nz_ratio_low,nz_ratio_high,nz_ratio_num):
    nozzle_list = np.linspace(nz_ratio_low,nz_ratio_high,int(nz_ratio_num))
    data_list = []  
    for nz in nozzle_list: 
        current_obj = copy.deepcopy(data_obj)
        current_obj.area_ratio = nz
        if current_obj.of_ratio is not None: 
            current_obj = compute_val(current_obj,calc_ch)
        else:
            current_obj = mono_prop_compute_val(current_obj,calc_ch)
        
        data_list.append(current_obj)
    return data_list 
 
    

