import sys
from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QMessageBox,QPushButton, QDoubleSpinBox, QRadioButton, QLineEdit,QLabel,QVBoxLayout,QGridLayout,QGroupBox,QHBoxLayout,QDialog
from PySide6.QtCore import Qt
from solver.calc_engine import compute_val,mono_prop_compute_val,new_prop_add,retrieve_card
from solver.propellants_list import OXIDIZERS,FUELS,MONOPROPS
from solver.data_class_custom import CalcSet,ChoiceSet
#from gui.secondary_dialog_boxes import AddExtraOutputs,OutputDisplayTab
from gui.mono_widgets import drop_down_widgets, button_widgets, input_box_widgets, output_box_widgets, radio_widgets,button_widget_set_2,AddPropCombo
from gui.helpers import set_field_visibility,add_output_func,exit_radio_control_function,mono_func_button,create_add_output,func_button,fun_save_csv,sweep_button_function, update_weight_percentage,split_components,count_keyword_occurrences
from gui.helpers import get_weight_percentages

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

    def __init__(self,mono_tab,bi_tab):
        super().__init__()
        self.layout = QFormLayout(self)

        self.mono_tab = mono_tab
        self.bi_tab = bi_tab
        ## Container for add_fuel, add_ox and add_prop buttons
        self.add_prop_container = QWidget()
        self.add_prop_layout = QHBoxLayout(self.add_prop_container)

        ## Container for add_element rows and buttons
        self.add_element_container = QWidget()
        self.add_element_layout = QGridLayout(self.add_element_container)

        ## Container to add blends 
        self.blend_container = QWidget() 
        self.blend_layout = QGridLayout(self.blend_container)

        # Widget to add element letter , like C for carbon
        self.add_element_letter = QLineEdit()
        self.add_element_letter.setMaximumWidth(80)

        # Widget to add number of atoms of an element
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
        # self.add_fuel.setMaximumWidth(80)
        self.add_fuel.clicked.connect(self.construct_string)
        self.add_ox = QPushButton("Add as Oxidizer")
        # self.add_ox.setMaximumWidth(80)
        self.add_ox.clicked.connect(self.construct_string)
        self.add_mono = QPushButton("Add as Monopropellant")
        # self.add_mono.setMaximumWidth(80)
        self.add_mono.clicked.connect(self.construct_string)
        self.add_prop_layout.addWidget(self.add_fuel)
        self.add_prop_layout.addWidget(self.add_ox)
        self.add_prop_layout.addWidget(self.add_mono)
        
        # Input boxes for custom propellant name, chemical formula, formation enthalpy
        self.prop_name = QLineEdit()
        self.prop_formula = QLineEdit()
        self.prop_enthalpy = QDoubleSpinBox()
        self.prop_enthalpy.setDecimals(2)
        self.prop_enthalpy.setRange(-sys.float_info.max,sys.float_info.max)
        self.ref_temp = QDoubleSpinBox()
        self.ref_temp.setDecimals(2)
        self.ref_temp.setRange(0,5000)
        self.ref_temp.setValue(298.15)
        self.ref_temp.setSuffix("K")
        self.prop_rho = QDoubleSpinBox()
        self.prop_rho.setDecimals(2)
        self.prop_rho.setRange(0,20) # Setting the density input limit to 20 g/cc or 20 tons/m3.
        self.prop_rho.setSuffix("g/cc")

        

        # Add everything to main layout, including the two containers
        self.layout.addRow("Enter propellant name",self.prop_name)
        self.layout.addRow("Enter propellant chemical formula",self.prop_formula)
        self.layout.addRow("Enter formation enthalpy in cal/mol",self.prop_enthalpy)
        self.layout.addRow("Enter Reference Temperature in K",self.ref_temp)
        self.layout.addRow("Enter density in g/cc (optional)",self.prop_rho)
        self.layout.addRow(self.add_element_container)
        self.layout.addRow(self.add_prop_container)
        AddPropCombo(self)


        self.element_name_list = [] # List of newly created element symbols
        self.element_num_list = [] # List of newly created numbers of elements
        self.element_name_list.append(self.add_element_letter)
        self.element_num_list.append(self.add_element_num)
        self.element_row_counter = 1 # Tracker for number of elements created

        self.blend_name_list = [] # List of newly created components to add to blend 
        self.blend_percent_list = [] # List of newly created components' wt %
        self.blend_counter = 0 # Tracker for number of components of a blend
    
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
        send_button = self.sender() 
        button_txt = send_button.text()
        if button_txt == "Add as fuel":
            str_lead = "fuel"
            ch = 3
        elif button_txt == "Add as Oxidizer":
            str_lead = "oxid"
            ch = 2
        elif button_txt == "Add as Monopropellant":
            str_lead = "name"
            ch = 1 
        
        
        if self.prop_formula.text():
            str_formula = self.prop_formula.text().strip()
        else:
            QMessageBox.warning(self,"Missing Information","Please enter the chemical formula of your custom propellant")
            return
        
        str_cal = str(self.prop_enthalpy.value())
        str_ref_temp = str(self.ref_temp.value())
        if self.prop_name.text():
            self.custom_prop_name = self.prop_name.text().strip() # I may need to access this later 
        else:
            QMessageBox.warning(self,"Missing Information","Please enter name of your custom propellant")
            return
        
        if self.prop_rho.value() > 0: 
            str_rho = str(self.prop_rho.value())
        else:
            str_rho = ""

        res_temp = ""
        for symbol, num in zip(self.element_name_list,self.element_num_list):
            elem_symb_temp = symbol.text()
            elem_num_temp = str(num.value())
            if elem_symb_temp:
                res_temp = res_temp + " " + elem_symb_temp + " " + elem_num_temp

        if str_rho: 
            str_rho_add = "rho.g/cc=" + str_rho
        else:
            str_rho_add= ""
        
        final_str = str_lead + " " + str_formula + res_temp + " " + "wt%=100.00" + " " + "h,cal=" + str_cal + " " + "t(k)=" + str_ref_temp + " " + str_rho_add
        final_str = final_str.strip()


        current_list_ox = [self.bi_tab.OxBox.itemText(i) for i in range(self.bi_tab.OxBox.count())]
        current_list_fuel = [self.bi_tab.FuBox.itemText(i) for i in range(self.bi_tab.FuBox.count())]
        current_list_mono_prop = [self.mono_tab.mono_prop_box.itemText(i) for i in range(self.mono_tab.mono_prop_box.count())]
        new_prop_add(self.custom_prop_name,final_str,ch)
        
        if ch == 1:
            if self.custom_prop_name not in current_list_mono_prop:
                self.mono_tab.mono_prop_box.addItem(self.custom_prop_name)
        elif ch == 2:
            if self.custom_prop_name not in current_list_ox:
                self.bi_tab.OxBox.addItem(self.custom_prop_name)
        elif ch == 3: 
            if self.custom_prop_name not in current_list_fuel:
                self.bi_tab.FuBox.addItem(self.custom_prop_name)
        
    def  helper_add_blend(self):
        blend_type_string = self.blend_options.currentText() 
        
        #self.blend_counter = self.blend_counter + 1
       
        
        
        if blend_type_string == "Fuel Blend":
            current_list_fu = [self.bi_tab.FuBox.itemText(i) for i in range(self.bi_tab.FuBox.count())]
            self.fuel_dropdown = QComboBox()
            self.fuel_dropdown.addItems(current_list_fu)
            
            self.fuel_percentage = QDoubleSpinBox()
            self.fuel_percentage.setDecimals(2)
            self.fuel_percentage.setRange(0,100)
            self.blend_layout.addWidget(self.fuel_dropdown,self.blend_counter,0,Qt.AlignmentFlag.AlignHCenter)
            self.blend_layout.addWidget(self.fuel_percentage,self.blend_counter,1,Qt.AlignmentFlag.AlignHCenter)
            self.group_layout.addWidget(self.blend_container)
            self.blend_name_list.append(self.fuel_dropdown)
            self.blend_percent_list.append(self.fuel_percentage)
            self.blend_counter = self.blend_counter + 1 

        if blend_type_string == "Oxidizer Blend":
            current_list_ox = [self.bi_tab.OxBox.itemText(i) for i in range(self.bi_tab.OxBox.count())]
            self.ox_dropdown = QComboBox()
            self.ox_dropdown.addItems(current_list_ox)
            self.ox_percentage = QDoubleSpinBox()
            self.ox_percentage.setDecimals(2)
            self.ox_percentage.setRange(0,100)
            self.blend_layout.addWidget(self.ox_dropdown,self.blend_counter,0,Qt.AlignmentFlag.AlignHCenter)
            self.blend_layout.addWidget(self.ox_percentage,self.blend_counter,1,Qt.AlignmentFlag.AlignHCenter)
            self.group_layout.addWidget(self.blend_container)
            self.blend_name_list.append(self.ox_dropdown)
            self.blend_percent_list.append(self.ox_percentage)
            self.blend_counter = self.blend_counter + 1

        if blend_type_string == "Monopropellant Blend":
            current_list_monoprop = [self.mono_tab.mono_prop_box.itemText(i) for i in range(self.mono_tab.mono_prop_box.count())]
            self.mono_dropdown = QComboBox()
            self.mono_dropdown.addItems(current_list_monoprop)
            self.mono_percentage = QDoubleSpinBox() 
            self.mono_percentage.setDecimals(2)
            self.mono_percentage.setRange(0,100)
            self.blend_layout.addWidget(self.mono_dropdown,self.blend_counter,0,Qt.AlignmentFlag.AlignHCenter)
            self.blend_layout.addWidget(self.mono_percentage,self.blend_counter,1,Qt.AlignmentFlag.AlignHCenter)
            self.group_layout.addWidget(self.blend_container)
            self.blend_name_list.append(self.mono_dropdown)
            self.blend_percent_list.append(self.mono_percentage)
            self.blend_counter = self.blend_counter + 1
            
            

    def helper_del_blend(self):
        if self.blend_counter > 0:
            self.blend_counter = self.blend_counter - 1
        else:
            return
        
        deleted_element = self.blend_name_list.pop()
        deleted_element_num = self.blend_percent_list.pop()

        self.blend_layout.removeWidget(deleted_element)
        deleted_element.deleteLater()
        self.blend_layout.removeWidget(deleted_element_num)
        deleted_element_num.deleteLater()

    
    def on_blend_changed(self):
        # Reset counter and widget lists 
        self.blend_counter = 0
        self.blend_percent_list = []
        self.blend_name_list = []
  
        # All the widget objects for storing propellant and weight percentage are deleted 
        while self.blend_layout.count(): 
            item = self.blend_layout.takeAt(0) # Returns the first widget's QLayoutWrapper (the actual widget object sits inside this wrapper)
            widget = item.widget() # Returns the actual widget object
            if widget is not None:
                widget.deleteLater() 
        # self.blend_container = QWidget()
        # self.blend_layout = QGridLayout(self.blend_container)

        
    
    def helper_on_add_blend(self):

        if self.blend_counter < 2: 
            QMessageBox.warning(self,"Insufficient Inputs","You need atleast two components to create a blend")
            return

        percent_list =    [self.blend_percent_list[i].value() for i in range(len(self.blend_percent_list))]
        blend_percent_sum = sum(percent_list)

        if blend_percent_sum != 100: 
            QMessageBox.warning(self,"Check Inputs","The Propellant percentages should add to 100%")
            return
        if self.blend_options.currentText() == "Fuel Blend":
            ch = 3
        elif self.blend_options.currentText() == "Oxidizer Blend":
            ch = 2
        else:
            ch = 1 

        # Update wt. percentage 
        count = 0
        final_card = []
        for item in self.blend_name_list: 
            name_str = item.currentText()
            card = retrieve_card(name_str,ch)
            card = " ".join(card)
            if ch == 1: 
                target = "name"
            elif ch == 2:
                target = "oxid"
            elif ch == 3:
                target = "fuel"
            key_count = count_keyword_occurrences(card,target)
            if key_count > 1: 
                mod_component = []
                component_list = split_components(card,target)
                for component in component_list:
                    wt_perc = get_weight_percentages(component)
                    wt_perc_updated = wt_perc[0]*(1/100) * percent_list[count] 
                    updated_component= update_weight_percentage(component,wt_perc_updated)
                    updated_component = updated_component + " "
                    mod_component.append(updated_component)
                final_card.extend(mod_component)
            else:
                updated_card = update_weight_percentage(card,percent_list[count])
                updated_card = updated_card + " "
                final_card.append(updated_card)



            # updated_card = update_weight_percentage(card,percent_list[count])
            # updated_card = updated_card + " "
            # final_card.append(updated_card)
            count = count + 1
        final_card = "\n".join(final_card)
        #print(final_card)
        custom_blend_name = self.blend_name_input.text().strip()
        current_list_ox = [self.bi_tab.OxBox.itemText(i) for i in range(self.bi_tab.OxBox.count())]
        current_list_fuel = [self.bi_tab.FuBox.itemText(i) for i in range(self.bi_tab.FuBox.count())]
        current_list_mono_prop = [self.mono_tab.mono_prop_box.itemText(i) for i in range(self.mono_tab.mono_prop_box.count())]
        new_prop_add(custom_blend_name,final_card,ch)
        
        if ch == 1:
            if custom_blend_name not in current_list_mono_prop:
                self.mono_tab.mono_prop_box.addItem(custom_blend_name)
        elif ch == 2:
            if custom_blend_name not in current_list_ox:
                self.bi_tab.OxBox.addItem(custom_blend_name)
        elif ch == 3: 
            if custom_blend_name not in current_list_fuel:
                self.bi_tab.FuBox.addItem(custom_blend_name)
        
        