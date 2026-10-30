from PySide6.QtWidgets import (QVBoxLayout,QSizePolicy,QInputDialog,QHBoxLayout,QComboBox,QDialog,QCheckBox,QDialogButtonBox,QFormLayout,QTextEdit,QWidget,QDoubleSpinBox,QRadioButton,QAbstractSpinBox,QLabel,QButtonGroup,QPushButton)
from dataclasses import fields,asdict
from gui.output_options import output_list,choice_list,data_variable_list,var_mapping
#from gui.helpers import create_add_output,set_field_visibility,add_output_func
from PySide6.QtCore import Qt
from solver.calc_loop import loop_func,loop_func_ch_pressure,loop_func_nozzle_ratio
from gui.gui_plotter_class import PlotCanvas,find_the_max
from pathlib import Path 
import csv
#from gui.helpers import find_the_max


class AddExtraOutputs(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setWindowTitle("Select Additional Output Options")
        layout = QVBoxLayout(self)

        self.look_up_string = dict(zip(output_list,choice_list))

        # Only set those attributes to 0 whose keys are in the options list. Other attributes cannot be touched.
        for str in output_list:
            var_name = self.look_up_string.get(str)
            setattr(parent.calc_choice_instance,var_name,0)
        setattr(parent.calc_choice_instance,'user_extra_outputs',0) 

        self.checkbox_list = [] 

        

        for options in output_list:
            cb = QCheckBox(options)
            layout.addWidget(cb)
            self.checkbox_list.append(cb)

        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok| QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_options(self,parent): 
        return_list = []
        ctr = 0
        for x in self.checkbox_list: 
            if x.isChecked():
                ctr = ctr + 1
                chkbox_text = x.text()
                variable_name = self.look_up_string.get(chkbox_text)
                # parent.calc_choice_instance.chamber_sp_heat_ch = 1
                setattr(parent.calc_choice_instance,variable_name,1)
                
        if ctr > 0: 
            setattr(parent.calc_choice_instance,'user_extra_outputs',1)
        else: 
            setattr(parent.calc_choice_instance,'user_extra_outputs',0)
        # return return_list


class OutputDisplayTab(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setWindowTitle("Displaying Additional Outputs")
        self.layout = QFormLayout(self)

        #  # The following output boxes (and the corresponding output) will only be displayed if the user selects those outputs

        # Chamber gas properties
        self.output_text_chamber_enthalpy = self.create_add_output(self.layout,"Chamber Enthalpy (KJ/Kg)")
        self.set_field_visibility(self.output_text_chamber_enthalpy,False)    

        self.output_text_chamber_gas_rho = self.create_add_output(self.layout,"Chamber Gas Density (Kg/m3)")
        self.set_field_visibility(self.output_text_chamber_gas_rho,False)

        self.output_text_mol_wt = self.create_add_output(self.layout,"Chamber Gas Molecular Wt. (g/mol)")
        self.set_field_visibility(self.output_text_mol_wt,False)

        self.output_text_chamber_gamma = self.create_add_output(self.layout,"Chamber specific heat ratio (<i>&gamma;<sub>ch</sub></i>)")
        self.set_field_visibility(self.output_text_chamber_gamma,False)

        self.output_text_chamber_cp = self.create_add_output(self.layout,"Chamber Specific Heat (KJ/Kg-K)")
        self.set_field_visibility(self.output_text_chamber_cp,False)

        # Thraot gas properties
        self.output_text_throat_enthalpy = self.create_add_output(self.layout, "Throat Enthalpy (KJ/Kg)")
        self.set_field_visibility(self.output_text_throat_enthalpy, False)

        self.output_text_throat_temp = self.create_add_output(self.layout,"Throat Gas Temperature (K)")
        self.set_field_visibility(self.output_text_throat_temp,False)

        self.output_text_throat_rho = self.create_add_output(self.layout, "Throat Gas Density (Kg/m3)")
        self.set_field_visibility(self.output_text_throat_rho, False)

        self.output_text_throat_sp_heat = self.create_add_output(self.layout,"Throat Gas Specific Heat (KJ/Kg-K)")
        self.set_field_visibility(self.output_text_throat_sp_heat,False)

        self.output_text_throat_mol_wt = self.create_add_output(self.layout,"Throat Gas Molecular Wt. (g/mol)")
        self.set_field_visibility(self.output_text_throat_mol_wt,False)

        self.output_text_throat_gamma = self.create_add_output(self.layout, "Throat specific heat ratio (<i>&gamma;<sub>throat</sub></i>)")
        self.set_field_visibility(self.output_text_throat_gamma,False)

        # Nozzle exit properties 
        self.output_text_exit_rho = self.create_add_output(self.layout, "Nozzle Exit Gas Density (kg/m3)")
        self.set_field_visibility(self.output_text_exit_rho, False)

        self.output_text_exit_temp = self.create_add_output(self.layout,"Nozzle Exit Temperature (K)")
        self.set_field_visibility(self.output_text_exit_temp,False)

        self.output_text_exit_sp_heat = self.create_add_output(self.layout,"Nozzle Exit Gas Specific Heat (KJ/Kg-K)")
        self.set_field_visibility(self.output_text_exit_sp_heat,False)

        self.output_text_exit_mol_wt = self.create_add_output(self.layout,"Nozzle Exit Gas Molecular Wt. (g/mol)")
        self.set_field_visibility(self.output_text_exit_mol_wt,False)

        self.output_text_exit_gamma = self.create_add_output(self.layout, "Nozzle Exit specific heat ratio (<i>&gamma;<sub>exit</sub></i>)")
        self.set_field_visibility(self.output_text_exit_gamma,False)

        self.output_text_exit_enthalpy = self.create_add_output(self.layout, "Nozzle Exit Enthalpy (KJ/Kg)")
        self.set_field_visibility(self.output_text_exit_enthalpy,False)

        self.output_exit_mach = self.create_add_output(self.layout,"Nozzle Exit Mach number")
        self.set_field_visibility(self.output_exit_mach,False)

        # Chamber gas conditional output box
        if parent.calc_choice_instance.chamber_enth_ch == 1:
            self.set_field_visibility(self.output_text_chamber_enthalpy,True)
        else:
            self.set_field_visibility(self.output_text_chamber_enthalpy,False)

        if parent.calc_choice_instance.gamma_ch == 1:
            self.set_field_visibility(self.output_text_chamber_gamma,True)
        else: 
            self.set_field_visibility(self.output_text_chamber_gamma,False)

        if parent.calc_choice_instance.chamber_rho_ch == 1: 
            self.set_field_visibility(self.output_text_chamber_gas_rho,True)
        else:
            self.set_field_visibility(self.output_text_chamber_gas_rho,False)

        if parent.calc_choice_instance.mol_wt_ch == 1: 
            self.set_field_visibility(self.output_text_mol_wt,True)
        else: 
            self.set_field_visibility(self.output_text_mol_wt,False)

        if parent.calc_choice_instance.chamber_sp_heat_ch == 1:
            self.set_field_visibility(self.output_text_chamber_cp,True)
        else:
            self.set_field_visibility(self.output_text_chamber_cp,False)

        # THroat gas conditional output box
        if parent.calc_choice_instance.throat_rho_ch == 1: 
            self.set_field_visibility(self.output_text_throat_rho, True)
        else: 
            self.set_field_visibility(self.output_text_throat_rho, False)

        if parent.calc_choice_instance.T_throat == 1: 
            self.set_field_visibility(self.output_text_throat_temp,True)
        else: 
            self.set_field_visibility(self.output_text_throat_temp,False)

        if parent.calc_choice_instance.throat_sp_heat_ch == 1:
            self.set_field_visibility(self.output_text_throat_sp_heat, True)
        else:
            self.set_field_visibility(self.output_text_throat_sp_heat,False)

        if parent.calc_choice_instance.throat_enth_ch == 1: 
            self.set_field_visibility(self.output_text_throat_enthalpy,True)
        else:
            self.set_field_visibility(self.output_text_throat_enthalpy,False)

        if parent.calc_choice_instance.mol_wt_throat == 1: 
            self.set_field_visibility(self.output_text_throat_mol_wt,True)
        else: 
            self.set_field_visibility(self.output_text_throat_mol_wt,False)

        if parent.calc_choice_instance.gamma_throat == 1: 
            self.set_field_visibility(self.output_text_throat_gamma,True)
        else: 
            self.set_field_visibility(self.output_text_throat_gamma,False)

        # Nozzle ecit plane conditional output box 
        if parent.calc_choice_instance.exit_rho_ch == 1: 
            self.set_field_visibility(self.output_text_exit_rho,True)
        else: 
            self.set_field_visibility(self.output_text_exit_rho,False)

        if parent.calc_choice_instance.T_exit == 1: 
            self.set_field_visibility(self.output_text_exit_temp,True)
        else: 
            self.set_field_visibility(self.output_text_exit_temp,False)

        if parent.calc_choice_instance.exit_sp_heat_ch == 1: 
            self.set_field_visibility(self.output_text_exit_sp_heat,True)
        else:
            self.set_field_visibility(self.output_text_exit_sp_heat,False)

        if parent.calc_choice_instance.exit_enth_ch == 1: 
            self.set_field_visibility(self.output_text_exit_enthalpy,True)
        else: 
            self.set_field_visibility(self.output_text_exit_enthalpy,False)

        if parent.calc_choice_instance.mol_wt_exit == 1: 
            self.set_field_visibility(self.output_text_exit_mol_wt,True)
        else: 
            self.set_field_visibility(self.output_text_exit_mol_wt,False)

        if parent.calc_choice_instance.gamma_exit == 1: 
            self.set_field_visibility(self.output_text_exit_gamma,True)
        else:
            self.set_field_visibility(self.output_text_exit_gamma,False)

        if parent.calc_choice_instance.mach_num_exit == 1: 
            self.set_field_visibility(self.output_exit_mach,True)
        else: 
            self.set_field_visibility(self.output_exit_mach,False)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)  # Closes dialog and returns 1
        self.layout.addRow(buttons)
        # buttons.rejected.connect(self.reject)  # Closes dialog and returns 0
    def disp_values(self,parent = None):
        # Print chamber properties
        if parent.calc_instance_2.H_ch is not None:
            self.output_text_chamber_enthalpy.setPlainText(str(round(parent.calc_instance_2.H_ch,2))) # Factor multiplied to convert output frfom btu/lbm to kj/kg

        if parent.calc_instance_2.rho_ch is not None: 
            self.output_text_chamber_gas_rho.setPlainText(str(round(parent.calc_instance_2.rho_ch,2))) # Factor multiplied to convert output from lb/cu_ft to Kg/m3

        if parent.calc_instance_2.cp_ch is not None: 
            self.output_text_chamber_cp.setPlainText(str(round(parent.calc_instance_2.cp_ch,2))) # Factor multipled to convert from BTU/lb-degR to KJ/Kg-K 

        if parent.calc_instance_2.gamma_ch  is not None: 
            self.output_text_chamber_gamma.setPlainText(str(round(parent.calc_instance_2.gamma_ch,2))) 

        if parent.calc_instance_2.mol_wt is not None:
            self.output_text_mol_wt.setPlainText(str(round(parent.calc_instance_2.mol_wt,2)))

        # Print throat properties 
        if parent.calc_instance_2.rho_throat is not None:
            self.output_text_throat_rho.setPlainText(str(round(parent.calc_instance_2.rho_throat,2)))

        if parent.calc_instance_2.gamma_throat is not None: 
            self.output_text_throat_gamma.setPlainText(str(round(parent.calc_instance_2.gamma_throat,2)))

        if parent.calc_instance_2.mol_wt_throat is not None: 
            self.output_text_throat_mol_wt.setPlainText(str(round(parent.calc_instance_2.mol_wt_throat,2)))

        if parent.calc_instance_2.H_throat is not None: 
            self.output_text_throat_enthalpy.setPlainText(str(round(parent.calc_instance_2.H_throat,2)))

        if parent.calc_instance_2.cp_throat is not None: 
            self.output_text_throat_sp_heat.setPlainText(str(round(parent.calc_instance_2.cp_throat,2)))

        if parent.calc_instance_2.T_Throat is not None: 
            self.output_text_throat_temp.setPlainText(str(round(parent.calc_instance_2.T_Throat,2)))

        # Print exit properties 
        if parent.calc_instance_2.exit_rho is not None: 
            self.output_text_exit_rho.setPlainText(str(round(parent.calc_instance_2.exit_rho,2)))

        if parent.calc_instance_2.exit_cp is not None: 
            self.output_text_exit_sp_heat.setPlainText(str(round(parent.calc_instance_2.exit_cp,2)))

        if parent.calc_instance_2.exit_gamma is not None: 
            self.output_text_exit_gamma.setPlainText(str(round(parent.calc_instance_2.exit_gamma,2)))

        if parent.calc_instance_2.exit_mol_wt is not None: 
            self.output_text_exit_mol_wt.setPlainText(str(round(parent.calc_instance_2.exit_mol_wt,2)))

        if parent.calc_instance_2.exit_H is not None: 
            self.output_text_exit_enthalpy.setPlainText(str(round(parent.calc_instance_2.exit_H,2)))

        if parent.calc_instance_2.exit_mach is not None: 
            self.output_exit_mach.setPlainText(str(round(parent.calc_instance_2.exit_mach,2)))

        if parent.calc_instance_2.T_Exit is not None: 
            self.output_text_exit_temp.setPlainText(str(round(parent.calc_instance_2.T_Exit,2)))


    

    
    # Had to make these new functions here again because I could not import it from helpers.py due to cross-referenxer issue        
    def create_add_output(self,layout: QFormLayout, field_name: str, default_text: str = ""):
        widget_object = QTextEdit()
        widget_object.setFixedSize(100,20)
        widget_object.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addRow(field_name,widget_object)
        return widget_object
        # set_field_visibility(widget_object,False)
    def set_field_visibility(self, field_obj, is_visible):
    # Toggles the visibility of a form field and its associated label.
        field_obj.setVisible(is_visible)
        self.layout.setRowVisible(field_obj,is_visible)
        
        # Retrieves the label linked to the field in the QFormLayout
        label = self.layout.labelForField(field_obj)
        if label is not None:
            label.setVisible(is_visible)
            self.layout.setRowVisible(field_obj,is_visible)

    # Execute this function when the user closes the secondary deisplay output tab so that the chocie variable set resets. 
    def reset_to_default(self,parent):
        self.look_up_string = dict(zip(output_list,choice_list))

        # Only set those attributes to 0 whose keys are in the options list. Other attributes cannot be touched.
        for str in output_list:
            var_name = self.look_up_string.get(str)
            setattr(parent.calc_choice_instance,var_name,0)
        setattr(parent.calc_choice_instance,'user_extra_outputs',0) 


class SweepDisplayTab(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Perform Parameter Sweep Calculation")
        self.DaddyLayout = QHBoxLayout(self)

        self.mega_container = QWidget()
        self.layout = QVBoxLayout(self.mega_container)

        self.calc_instance = parent.calc_instance
        self.calc_choice_instance = parent.calc_choice_instance

        parent.nozzle_radio.setEnabled(False)
        parent.exit_p_radio.setEnabled(False)

        
    
        self.radio_button_group = QButtonGroup(self)
        self.radio_button_group.setExclusive(True)

        self.of_radio = QRadioButton("O/F Sweep")
        self.pressure_radio = QRadioButton("Chamber Pressure Sweep")
        self.nozzle_radio = QRadioButton("Nozzle Area Ratio Sweep")

        
        self.radio_button_group.addButton(self.of_radio)
        self.radio_button_group.addButton(self.pressure_radio)
        self.radio_button_group.addButton(self.nozzle_radio)
        
        
        self.inner_container_1 = QWidget()
        self.inner_layout_1 = QFormLayout(self.inner_container_1)

        self.inner_container_2 = QWidget()
        self.inner_layout_2 = QFormLayout(self.inner_container_2)

        self.iinner_container_3 = QWidget()
        self.inner_layout_3 = QFormLayout(self.iinner_container_3)

        self.drop_down_container = QWidget()
        self.drop_down_layout = QFormLayout(self.drop_down_container)


        # Create widgets and add them to layout
        if parent.input_of is not None: 
            self.make_widgets_of()
        self.make_widget_ch_pressure()
        self.make_widget_nozzle()
        self.create_switch_checkbox()
        self.make_widget_buttons()
        
        self.make_drop_down_widget()
        self.DaddyLayout.addWidget(self.mega_container)
        self.create_additional_outputs_widget()
        self.create_plot_widget()
        

        # Connect compute button to function 
        self.compute_button.clicked.connect(lambda checked = False: self.loop_wrap_func(parent))

        # Connect radio toggles to functions which activate when radios toggled
        if parent.input_of is not None:
            self.of_radio.toggled.connect(lambda checked = False: self.of_toggle_func(parent))
        self.pressure_radio.toggled.connect(lambda checked = False: self.pressure_toggle_func(parent))
        self.nozzle_radio.toggled.connect(lambda checked = False: self.nozzle_toggle_func(parent))

        # Running the functions once during start-up
        if parent.input_of is not None: 
            self.of_toggle_func(parent)
        self.pressure_toggle_func(parent)
        self.nozzle_toggle_func(parent)
        
    
    def make_widgets_of(self):
      
        # self.inner_layout_1.addRow(self.of_radio)
        self.layout.addWidget(self.of_radio)
        self.of_radio.setChecked(True)
        # self.of_radio.toggled.connect(self.of_sweep_func)
        self.of_lower = self.input_box_creator(self.inner_layout_1,"Lower Limit",200,0.2,2,2,None)
        self.of_upper = self.input_box_creator(self.inner_layout_1,"Upper Limit",200,0.2,2,10,None)
        self.num_points = self.input_box_creator(self.inner_layout_1,"Number of Points",1000,2,0,50,None)
        self.layout.addWidget(self.inner_container_1)

    def make_widget_ch_pressure(self):

        self.layout.addWidget(self.pressure_radio)
        # self.inner_layout_2.addRow(self.pressure_radio)
        self.pressure_lower = self.input_box_creator(self.inner_layout_2,"Lower Limit",100,2,2,10,"bar")
        self.pressure_upper = self.input_box_creator(self.inner_layout_2,"Upper Limit",100,2,2,30,"bar")
        self.pressure_num_points = self.input_box_creator(self.inner_layout_2,"Number of Points",1000,2,0,50,None)
        self.layout.addWidget(self.inner_container_2)

    def make_widget_nozzle(self):
        self.layout.addWidget(self.nozzle_radio)
        self.nozzle_lower = self.input_box_creator(self.inner_layout_3,"Lower Limit",1000,1.2,2,10,None)
        self.nozzle_upper = self.input_box_creator(self.inner_layout_3,"Upper Limit",1000,1.2,2,50,None)
        self.nozzle_num_points = self.input_box_creator(self.inner_layout_3,"Number of Points",1000,2,0,50,None)
        self.layout.addWidget(self.iinner_container_3)

    def make_widget_buttons(self):
        self.compute_button = QPushButton("Compute")
        self.plot_button = QPushButton("Plot")
        self.save_csv_button = QPushButton("Save to csv")
        
 
        self.plot_button.clicked.connect(self.make_the_plot)
        self.save_csv_button.clicked.connect(self.fun_save_sweep_csv)

        self.layout.addWidget(self.compute_button)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.save_csv_button)

    def make_drop_down_widget(self):
        self.x_axis = QComboBox()
        self.y_axis = QComboBox()
        self.drop_down_layout.addRow("X-Axis",self.x_axis)
        self.drop_down_layout.addRow("Y-Axis",self.y_axis)
        self.basic_output_list = ["Characteristic Velocity (m/s)","Vaccum Isp (s)","Ambient Isp (s)", "Chamber Temperature (K)", "Exit Pressure (Pa)"]
        
        self.layout.addWidget(self.drop_down_container)
        # self.layout.addWidget(self.x_axis)

    def create_plot_widget(self):
        plt_ht = 3
        self.sc = PlotCanvas(self,width= plt_ht*2, height= plt_ht, dpi = 100)
        self.plot_container = QWidget()
        self.plot_layout = QVBoxLayout(self.plot_container)

        self.plot_button_container = QWidget()
        self.plot_button_layout = QHBoxLayout(self.plot_button_container)
        self.plot_button_container.setSizePolicy(
        QSizePolicy.Policy.Expanding,  # Allow horizontal growth
        QSizePolicy.Policy.Fixed      # Keep height fitted to buttons
        )
        self.plot_button_layout.setContentsMargins(0, 0, 0, 0)

       

        self.find_max_button = QPushButton("Find Maxima")
        self.plot_button_layout.addWidget(self.find_max_button)
        self.find_max_button.clicked.connect(self.find_max_wrap)

        self.save_plot = QPushButton("Save this Graph")
        self.plot_button_layout.addWidget(self.save_plot)
        self.save_plot.clicked.connect(self.save_this_plot)

        


        
        self.plot_layout.addWidget(self.sc)
        self.plot_layout.addWidget(self.plot_button_container)
        self.DaddyLayout.addWidget(self.plot_container)
        
        # self.sc.axis.set_visible(False)
        # self.show()


    def create_switch_checkbox(self): # Making this so that once user selects this option, the extra output options appear 
        self.check_box_to_select_add_outputs = QCheckBox("Select Additional Outputs")
        self.layout.addWidget(self.check_box_to_select_add_outputs)
        # self.check_box_to_select_add_outputs.toggled.connect(self.so_many_fucking_funcs)
        

    def create_additional_outputs_widget(self):
        self.heading_label = QLabel("Select Additional Outputs for Sweep Calculations")
        self.checkbox_list = []
        self.add_output_containers = QWidget()
        self.add_output_layout = QVBoxLayout(self.add_output_containers)
        # self.add_output_layout.addWidget(self.heading_label) # Perhaps I don't need to add this widget
        for options in output_list:
            self.cb = QCheckBox(options)
            self.add_output_layout.addWidget(self.cb)
            self.checkbox_list.append(self.cb)

        self.DaddyLayout.addWidget(self.add_output_containers)
        self.add_output_containers.setVisible(self.check_box_to_select_add_outputs.isChecked()) # On startup, the dialog box will be set based on this command
        self.check_box_to_select_add_outputs.toggled.connect(self.add_output_containers.setVisible) 
        # Note: .setVisible is a function. When it is passed as a connect function argument, ....
        # ...what happens is that if the box is clicked, a boolean true is sent out which makes the .setVisible method call .setVisible(True)


    # Helper functions for this class 

    def input_box_creator(self,layout: QFormLayout,name_str:str,upper_range,lower_range,decimal_places,default_value,units:str):
        widget_object = QDoubleSpinBox()
        widget_object.setButtonSymbols(QAbstractSpinBox.NoButtons)
        widget_object.setRange(lower_range,upper_range)
        widget_object.setDecimals(decimal_places)
        widget_object.setValue(default_value)
        widget_object.setSuffix(units)
        layout.addRow(name_str,widget_object)
        return widget_object

    def make_the_plot(self):
       
        self.sc.axis.clear()

        if self.of_radio.isChecked():
            self.x_list_num = self.of_ratios
            self.sc.axis.set_xlabel("O/F Ratio")
        if self.pressure_radio.isChecked(): 
            self.x_list_num = self.pressure_list
            self.sc.axis.set_xlabel("Chamber Pressure (bar)")
        if self.nozzle_radio.isChecked(): 
            self.x_list_num = self.nozzle_list
            self.sc.axis.set_xlabel("Nozzle Area Ratio")
        
        
        if self.y_axis.currentText() == self.basic_output_list[1]:
            self.sc.axis.plot(self.x_list_num,self.vac_isps,'k--')
            self.sc.axis.set_ylabel("Vacuum Isp (s)")
        if self.y_axis.currentText() == self.basic_output_list[0]:
            self.sc.axis.plot(self.x_list_num,self.c_star_val,'k--')
            self.sc.axis.set_ylabel("Characteristic Velocity (m/s)")
        if self.y_axis.currentText() == self.basic_output_list[2]:
            self.sc.axis.plot(self.x_list_num,self.amb_isps,'k--')
            self.sc.axis.set_ylabel("Ambient Isp (s)")
        if self.y_axis.currentText() == self.basic_output_list[3]:
            self.sc.axis.plot(self.x_list_num,self.T_ad,'k--')
            self.sc.axis.set_ylabel("Adiabatic Flame Temperature (K)")
        if self.y_axis.currentText() == self.basic_output_list[4]:
            self.sc.axis.plot(self.x_list_num,self.exit_pressures,'k--')
            self.sc.axis.set_ylabel("Nozzle Exit Pressure (Pa)")
        if self.y_axis.currentText() in self.add_output:
            output_str_name = self.look_for_variable[self.y_axis.currentText()]
            y_array = self.output_dict[output_str_name]
            self.sc.axis.plot(self.x_list_num,y_array)
            self.sc.axis.set_ylabel(self.y_axis.currentText())
        self.sc.draw_idle()

    def save_this_plot(self):
        text,ok = QInputDialog.getText(self,"Enter Filename","Please enter your preferred filename")
        if ok and text: 
            current_dir = Path.cwd()
            results_dir = current_dir/"Results (Desktop_CEA)"
            results_dir.mkdir(parents = True,exist_ok=True)

            save_path = results_dir/text

            self.sc.fig.savefig(save_path, bbox_inches='tight', dpi=300)


    def of_toggle_func(self,parent):
        if self.of_radio.isChecked(): 
            self.of_lower.setEnabled(True)
            self.of_upper.setEnabled(True)
            self.num_points.setEnabled(True)
            parent.input_of.setEnabled(False)
            self.x_axis.clear()
            self.x_axis.addItems({"O/F"})
        else: 
            self.of_lower.setEnabled(False)
            self.of_upper.setEnabled(False)
            self.num_points.setEnabled(False)
            parent.input_of.setEnabled(True)

    def pressure_toggle_func(self,parent):
        if self.pressure_radio.isChecked(): 
            self.pressure_lower.setEnabled(True)
            self.pressure_upper.setEnabled(True)
            self.pressure_num_points.setEnabled(True)
            parent.input_pc.setEnabled(False)
            self.x_axis.clear()
            self.x_axis.addItems({"Chamber Pressure"})
        else: 
            self.pressure_lower.setEnabled(False)
            self.pressure_upper.setEnabled(False)
            self.pressure_num_points.setEnabled(False)
            parent.input_pc.setEnabled(True)

    def nozzle_toggle_func(self,parent):
        if self.nozzle_radio.isChecked(): 
            self.nozzle_lower.setEnabled(True)
            self.nozzle_upper.setEnabled(True)
            self.nozzle_num_points.setEnabled(True)
            parent.nozzle_rat.setEnabled(False)
            self.x_axis.clear()
            self.x_axis.addItems({"Nozzle Area Ratio"})
        else: 
            self.nozzle_lower.setEnabled(False)
            self.nozzle_upper.setEnabled(False)
            self.nozzle_num_points.setEnabled(False)
            parent.nozzle_rat.setEnabled(True)

    def loop_wrap_func(self,parent):

        self.basic_output_list = self.basic_output_list[:5] # Ensures that once the function is called, only the first 5 (default) outputs are included in the list and appended to y_axis drop-box

        lookup_dict = dict(zip(output_list,choice_list)) # Key: Strings showing UI options. Variables: Corresponding names of variables in calculation choice set dataclass
        look_for_variable = dict(zip(output_list,data_variable_list)) # Key: String showing ui options. Variables: Corresponding names of variables in Calc_Set dataclass
        #lookup_dict_list = dict(zip(output_list,list(range(18))))
        self.look_for_variable = look_for_variable
        self.lookup_dict = lookup_dict

        if self.check_box_to_select_add_outputs.isChecked():
            ctr = 0
            add_output = []
            for options in output_list: 
                if self.checkbox_list[ctr].isChecked():
                    attr_str = lookup_dict[options]
                    setattr(self.calc_choice_instance,attr_str,1)
                    if options not in add_output:
                        add_output.append(options)
                ctr = ctr + 1
        else:
            add_output = []
            for options in output_list: 
                attr_str = lookup_dict[options]
                setattr(self.calc_choice_instance,attr_str,0)
        
        #print(self.calc_choice_instance)
        self.calc_instance.chamber_pressure = parent.input_pc.value() # user inputs the pressure in bar 
        self.calc_instance.amb_pressure = parent.input_p_amb.value()
        self.calc_instance.area_ratio = parent.nozzle_rat.value() 
        if parent.input_of is not None:
            self.calc_instance.of_ratio = parent.input_of.value()

        if parent.eq_button.isChecked():
            self.calc_instance.flg1 = 0
            self.calc_instance.flg2 = 0
            self.calc_instance.solver_setting = "Equilibrium throughout"

        if parent.frz_ch.isChecked():
            self.calc_instance.flg1 = 1
            self.calc_instance.flg2 = 0
            self.calc_instance.solver_setting = "Flow frozen after combustion chamber"

        if parent.frz_throat.isChecked(): 
            self.calc_instance.flg1 = 1
            self.calc_instance.flg2 = 1
            self.calc_instance.solver_setting = "Flow frozen after nozzle throat"

        if parent.input_of is not None:        
            self.calc_instance.fuel = parent.FuBox.currentText()
            self.calc_instance.ox = parent.OxBox.currentText()
        else: 
            self.calc_instance.mono_prop_name = parent.mono_prop_box.currentText()
        # print(self.calc_instance.of_ratio)

        self.calc_choice_instance.nzzl_ch  = 1
        if parent.input_of is not None:
            if  self.of_radio.isChecked():
                of_low_val = self.of_lower.value()
                of_high_val = self.of_upper.value()
                of_num_val = self.num_points.value()
                self.list_obj = loop_func(self.calc_instance,self.calc_choice_instance,of_low_val,of_high_val,of_num_val)
                self.of_ratios = [obj.of_ratio for obj in self.list_obj]

        if self.pressure_radio.isChecked(): 
            pressure_low_val = self.pressure_lower.value()
            pressure_high_val = self.pressure_upper.value() 
            pressure_num = self.pressure_num_points.value()
            self.list_obj = loop_func_ch_pressure(self.calc_instance,self.calc_choice_instance,pressure_low_val,pressure_high_val,pressure_num)
            self.pressure_list = [obj.chamber_pressure for obj in self.list_obj]
            # print(self.calc_instance.of_ratio)

        if self.nozzle_radio.isChecked(): 
            nozzle_low_val = self.nozzle_lower.value()
            nozzle_high_val = self.nozzle_upper.value() 
            nozzle_num = self.nozzle_num_points.value() 
            self.list_obj = loop_func_nozzle_ratio(self.calc_instance,self.calc_choice_instance,nozzle_low_val,nozzle_high_val,nozzle_num)
            self.nozzle_list = [obj.area_ratio for obj in self.list_obj]
        # pc = self.input_pc.value() *14.504 # Converts the input pressure to psia 

        
        self.vac_isps = [obj.vac_isp for obj in self.list_obj] 
        self.exit_pressures = [obj.exit_pressure for obj in self.list_obj]
        self.T_ad = [obj.chamber_temp for obj in self.list_obj]
        self.c_star_val = [obj.cstar for obj in self.list_obj]
        self.amb_isps = [obj.isp_amb for obj in self.list_obj]

       
        
        self.output_dict = {} # Stores all the additional output results in a dictionary. Key is same as string of calc_set attr. Data is actual data array
        self.y_axis.clear()

        for stuff in add_output:
            output_str = look_for_variable[stuff]
            self.output_dict[output_str] = [getattr(obj,look_for_variable[stuff]) for obj in self.list_obj]


        self.add_output = add_output
        self.basic_output_list.extend(add_output)
   
        self.y_axis.addItems(self.basic_output_list)
        
    def find_max_wrap(self):
        y_val_str = self.y_axis.currentText()
        if y_val_str == self.basic_output_list[0]:
            y_array = self.c_star_val
        if y_val_str == self.basic_output_list[1]:
            y_array = self.vac_isps
        if y_val_str == self.basic_output_list[2]:
            y_array = self.amb_isps
        if y_val_str == self.basic_output_list[3]:
            y_array = self.T_ad
        if y_val_str == self.basic_output_list[4]:
            y_array = self.exit_pressures
        if y_val_str in self.add_output:
            output_str_name = self.look_for_variable[self.y_axis.currentText()]
            y_array = self.output_dict[output_str_name]

        
        output = find_the_max(self.x_list_num,y_array)
        if not isinstance(output,str):
            self.sc.axis.plot(output[0],output[1],marker='x', markersize=8, color='red')
            self.sc.axis.axvline(x = output[0],color = 'red',linestyle = '--')
            self.sc.axis.axhline(y = output[1],color = 'red',linestyle = '--')
            self.sc.axis.annotate(
            text = f'x = {output[0]}\ny = {output[1]}',
            xy = (output[0],output[1]),
            xytext = (15,15),
            textcoords='offset points',
            bbox = dict(
                boxstyle = 'round,pad = 0.5',
                facecolor = 'none'

            ),
            fontsize = 10,
            fontweight = 'bold'


            )
            self.sc.draw_idle()
        else:
            self.sc.axis.annotate(
            'Maxima not found', 
            xy=(0.5, 0.9),             # Places it at 50% width, 90% height of the plot
            xycoords='axes fraction',   # Uses relative axes layout (0 to 1) instead of data points
            ha='center',               # Horizontally centers the text on the xy coordinate
            va='center',               # Vertically centers the text on the xy coordinate
            fontsize=12,               # Text size
            color='black',               # Font color
            bbox=dict(boxstyle='round,pad=0.3', fc='none', alpha=1) 
        )
            self.sc.draw_idle()

    
    def fun_save_sweep_csv(self):
        results = getattr(self, "list_obj", None)
        if not results:
            return

        text,ok = QInputDialog.getText(self,"Enter Filename","Please enter your preferred filename")
        if not ok or not text.strip():
            return

        rows = [asdict(result) for result in results]
        # Keep a column if at least one sweep result has a value for it.
        keys = [
            key for key in rows[0]
            if key not in {"flg1", "flg2"}
            and any(row[key] is not None for row in rows)
        ]

        results_dir = Path.cwd() / "Results (Desktop_CEA)"
        results_dir.mkdir(parents=True, exist_ok=True)
        filename = text.strip()
        if not filename.lower().endswith(".csv"):
            filename += ".csv"
        save_path = results_dir / filename

        with open(save_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([var_mapping.get(key, key) for key in keys])
            for row in rows:
                writer.writerow([row[key] for key in keys])






