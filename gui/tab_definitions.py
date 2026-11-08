import sys
from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QPushButton, QDoubleSpinBox, QRadioButton, QLineEdit,QLabel,QVBoxLayout,QGridLayout,QGroupBox,QHBoxLayout,QDialog
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

        
        


class AddNewProp(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

        ## Container for add_fuel, add_ox and add_prop buttons
        self.add_prop_container = QWidget()
        self.add_prop_layout = QHBoxLayout(self.add_prop_container)

        ## Container for add_element rows and buttons
        self.add_element_container = QWidget()
        self.add_element_layout = QGridLayout(self.add_element_container)

        # Widget to add element letter , like C for carbon
        self.add_element_letter = QLineEdit()
        self.add_element_letter.setMaximumWidth(80)

        # Widget to add number of elements
        self.add_element_num = QDoubleSpinBox() 
        self.add_element_num.setDecimals(1)
        self.add_element_num.setMaximumWidth(80)

        # Button to add more rows which creates additional input boxes for adding element symbol and number of elements
        self.add_more_elements = QPushButton("ADD")
        self.add_more_elements.setMaximumWidth(60)
        self.add_more_elements.clicked.connect(self.add_element_func)

        # Button to delete rows (deletes from the last added widget onwards)
        self.delete_elements = QPushButton("DEL")
        self.delete_elements.setMaximumWidth(60)
        self.delete_elements.clicked.connect(self.del_element_func)

        # ELement row labels
        self.element_lbl_1 = QLabel("Element Symbol")
        self.element_lbl_1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.element_lbl_2 = QLabel("Number of atoms")
        self.element_lbl_2.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add to layout widget for container to add_element_container
        self.add_element_layout.addWidget(self.element_lbl_1,0,0,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(self.add_element_letter,1,0,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(self.element_lbl_2,0,1,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(self.add_element_num,1,1,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(self.add_more_elements,1,2,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(self.delete_elements,1,3,Qt.AlignmentFlag.AlignHCenter)

        # Add three buttons to add_prop_container      
        self.add_fuel = QPushButton("Add as fuel")
        self.add_fuel.clicked.connect(self.construct_string)
        self.add_ox = QPushButton("Add as Oxidizer")
        self.add_mono = QPushButton("Add as Monopropellant")
        self.add_prop_layout.addWidget(self.add_fuel)
        self.add_prop_layout.addWidget(self.add_ox)
        self.add_prop_layout.addWidget(self.add_mono)
        
        # Input boxes for custom propellant name, chemical formula, formation enthalpy
        self.prop_name = QLineEdit()
        self.prop_formula = QLineEdit()
        self.prop_enthalpy = QDoubleSpinBox()
        self.prop_enthalpy.setDecimals(2)
        self.prop_enthalpy.setRange(-sys.float_info.max,sys.float_info.max)


        # Add everything to main layout, including the two containers
        self.layout.addRow("Enter propellant name",self.prop_name)
        self.layout.addRow("Enter propellant chemical formula",self.prop_formula)
        self.layout.addRow("Enter formation enthalpy in cal/mol",self.prop_enthalpy)
        self.layout.addRow(self.add_element_container)
        self.layout.addRow(self.add_prop_container)


        self.element_name_list = [] # List of newly created element symbols
        self.element_num_list = [] # List of newly created numbers of elements
        self.element_name_list.append(self.add_element_letter)
        self.element_num_list.append(self.add_element_num)
        self.element_row_counter = 1 # Tracker for number of elements created
    
    def add_element_func(self):
        self.element_row_counter = self.element_row_counter + 1 
        element_holder = QLineEdit() 
        element_holder.setMaximumWidth(80)
        
        element_num_holder = QDoubleSpinBox() 
        element_num_holder.setDecimals(1)
        element_num_holder.setMaximumWidth(80)

        self.add_element_layout.addWidget(element_holder,self.element_row_counter,0,Qt.AlignmentFlag.AlignHCenter)
        self.add_element_layout.addWidget(element_num_holder,self.element_row_counter,1,Qt.AlignmentFlag.AlignHCenter)
        
        self.element_name_list.append(element_holder)
        self.element_num_list.append(element_num_holder)
        

    def del_element_func(self):
        if self.element_row_counter > 1:
            self.element_row_counter = self.element_row_counter - 1
        
        deleted_element = self.element_name_list.pop()
        deleted_element_num = self.element_num_list.pop()

        self.add_element_layout.removeWidget(deleted_element)
        deleted_element.deleteLater()
        self.add_element_layout.removeWidget(deleted_element_num)
        deleted_element_num.deleteLater()
    
    def construct_string(self):
        res_temp = ""
        for symbol, num in zip(self.element_name_list,self.element_num_list):
            elem_symb_temp = symbol.text()
            elem_num_temp = str(num.value())
            res_temp = res_temp + " " + elem_symb_temp + " " + elem_num_temp

        print(res_temp)
