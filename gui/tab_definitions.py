from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QPushButton, QDoubleSpinBox, QRadioButton, QTextEdit,QLabel,QVBoxLayout,QGridLayout,QGroupBox,QHBoxLayout,QDialog
from PySide6.QtCore import Qt
from solver.calc_engine import compute_val,mono_prop_compute_val
from solver.propellants_list import OXIDIZERS,FUELS,MONOPROPS
from solver.data_class_custom import CalcSet,ChoiceSet
#from gui.secondary_dialog_boxes import AddExtraOutputs,OutputDisplayTab
from gui.mono_widgets import drop_down_widgets, button_widgets, input_box_widgets, output_box_widgets, radio_widgets,button_widget_set_2
from gui.helpers import set_field_visibility,add_output_func,exit_radio_control_function,mono_func_button,create_add_output,func_button,fun_save_csv,sweep_button_function


class BiPropTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

        self.calc_instance = CalcSet(chamber_pressure=0,cstar = 0, chamber_temp= 0 ,vac_isp=0)
        self.calc_choice_instance = ChoiceSet()

        BiPropTab.create_add_output = create_add_output     # Equivalent to def create_add_output(self,...other arguments)
        BiPropTab.exit_condition_func = exit_radio_control_function # Equivalent to def exit_condition_func(self..). Descriptor binding. "self" automatically injected as first argument
        BiPropTab.func_button = func_button
        BiPropTab.add_output_func = add_output_func
        BiPropTab.set_field_visibility = set_field_visibility
        BiPropTab.fun_save_csv = fun_save_csv
        BiPropTab.sweep_button_function = sweep_button_function

        # Call your widget helper functions. Each of these functions creates the widget objects and adds them to the layout object
        drop_down_widgets(self,2)
        input_box_widgets(self,2)
        radio_widgets(self)
        button_widgets(self,2)
        output_box_widgets(self)
        button_widget_set_2(self)

        self.exit_condition_func()# Function that executes each time you toggle the radio button of the exit condition group
        
    
  




        

class MonoPropTab(QWidget):
    def __init__(self):

        super().__init__()
        self.layout = QFormLayout(self)



        self.calc_instance = CalcSet(chamber_pressure=0,cstar = 0, chamber_temp= 0 ,vac_isp=0)
        self.calc_choice_instance = ChoiceSet()

        MonoPropTab.calc_func = mono_func_button
        MonoPropTab.pop_up = add_output_func
        MonoPropTab.set_field_visibility = set_field_visibility
        MonoPropTab.exit_condition_func = exit_radio_control_function
        MonoPropTab.create_add_output =  create_add_output
        MonoPropTab.fun_save_csv = fun_save_csv
        MonoPropTab.sweep_button_function = sweep_button_function

        drop_down_widgets(self,1)

        input_box_widgets(self)
        radio_widgets(self)
        button_widgets(self)
        output_box_widgets(self)
        button_widget_set_2(self)
 
        self.exit_condition_func() # This function connects to the radio toggle for exit conditionl. Run it once at startup 

        
        
 