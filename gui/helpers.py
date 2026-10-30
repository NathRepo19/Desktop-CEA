
from gui.secondary_dialog_boxes import AddExtraOutputs, OutputDisplayTab, SweepDisplayTab
from PySide6.QtWidgets import QDialog,QTextEdit,QFormLayout,QInputDialog
from solver.calc_engine import compute_val,mono_prop_compute_val
from PySide6.QtCore import Qt
from solver.data_class_custom import CalcSet
from gui.output_options import var_mapping
from dataclasses import asdict, dataclass
from pathlib import Path
import csv

# NOTE: Helper functions that are added as functions to buttons and radio widgets etc. 
## NOTE 2: If a function definition has a mono_ pre-fix, it means that the helper function is different for monoprop and biprop implementation 

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

def sweep_button_function(self):
    def enable_back():
        if self.input_of is not None: 
            self.input_of.setEnabled(True)
        self.input_pc.setEnabled(True)
        self.nozzle_rat.setEnabled(True)
        self.nozzle_radio.setEnabled(True)
        self.exit_p_radio.setEnabled(True)

    sweep_dialog = SweepDisplayTab(self)
    sweep_dialog.show()
    # Once your sweep tab's function is done, any main gui widgets you disabled will be brought back online to be reused
    sweep_dialog.finished.connect(enable_back)

# Connects to 2nd button to add extra outputs 
def add_output_func(self):
    dialog = AddExtraOutputs(self)
    self.res = 5
    selected = []

    if dialog.exec() == QDialog.Accepted: # Code executes onnly if user presses "OK". dialog.exec() stores 1 QDialog.Accepted also store 1     
        dialog.get_selected_options(self)


    if self.calc_choice_instance.user_extra_outputs == 1:
        self.dialog_2 = OutputDisplayTab(self)
        self.dialog_2.show()
        self.Calc_button_2.setEnabled(False) # While the output secondary dialog box is open, the user cannot click button_2
        self.res = self.dialog_2.exec()
        if self.res == QDialog.Accepted or self.res == QDialog.Rejected:
            self.calc_choice_instance.user_extra_outputs = 0 # Once the user clicks ok in the secondary dialog box field, button_2 is available again
            self.dialog_2.reset_to_default(self)
            self.Calc_button_2.setEnabled(True) 



def exit_radio_control_function(self):

    is_nozzle = self.nozzle_radio.isChecked()
    self.nozzle_rat.setVisible(is_nozzle)
    self.exit_p.setVisible(not is_nozzle)
    self.output_text_box_5.setVisible(not is_nozzle)
    self.output_text_box_6.setVisible(is_nozzle)


    if hasattr(self, 'layout'):
        self.layout.labelForField(self.nozzle_rat).setVisible(is_nozzle)
        self.layout.labelForField(self.exit_p).setVisible(not is_nozzle)
        self.layout.labelForField(self.output_text_box_5).setVisible(not is_nozzle)
        self.layout.labelForField(self.output_text_box_6).setVisible(is_nozzle)


# To connect to the Calculate button in bipropellant tab
def func_button(self): 
    # Read the user input values
    self.calc_instance_2 = CalcSet(chamber_pressure=0,cstar = 0, chamber_temp= 0 ,vac_isp=0)
    self.calc_instance = self.calc_instance_2
    # pc = self.input_pc.value() *14.504 # Converts the input pressure to psia 
    # self.calc_instance.chamber_pressure = pc
    self.calc_instance.chamber_pressure = self.input_pc.value() # user inputs the pressure in bar 


    self.calc_instance.ox = self.OxBox.currentText()
    self.calc_instance.of_ratio = self.input_of.value()
    self.calc_instance.fuel = self.FuBox.currentText()
    self.calc_instance.amb_pressure = self.input_p_amb.value()

    if self.nozzle_radio.isChecked(): 
        self.calc_instance.area_ratio = self.nozzle_rat.value() 
        self.calc_choice_instance.nzzl_ch = 1
        self.calc_choice_instance.exit_ch = 0
    else:
        self.calc_instance.exit_pressure = self.exit_p.value() # Convert from Pa user input units to psi
        self.calc_choice_instance.exit_ch = 1
        self.calc_choice_instance.nzzl_ch  = 0
    
    # Check what the user selected in the radio selection menu 
    
    if self.eq_button.isChecked():
        self.calc_instance.flg1 = 0
        self.calc_instance.flg2 = 0
        self.calc_instance.solver_setting = "Equilibrium throughout"

    if self.frz_ch.isChecked():
        self.calc_instance.flg1 = 1
        self.calc_instance.flg2 = 0
        self.calc_instance.solver_setting = "Flow frozen after combustion chamber"

    if self.frz_throat.isChecked(): 
        self.calc_instance.flg1 = 1
        self.calc_instance.flg2 = 1
        self.calc_instance.solver_setting = "Flow frozen after nozzle throat"

   

    self.calc_instance_2 = compute_val(self.calc_instance,self.calc_choice_instance)
    self.output_text_box.setPlainText(str(self.calc_instance_2.cstar))
    self.output_text_box_2.setPlainText(str(self.calc_instance_2.vac_isp))
    self.output_text_box_4.setPlainText(str(self.calc_instance_2.isp_amb))
    self.output_text_box_3.setPlainText(str(self.calc_instance_2.chamber_temp))
    if self.nozzle_radio.isChecked():
        self.output_text_box_6.setPlainText(str(self.calc_instance_2.exit_pressure))
        self.output_text_box_5.setPlainText("Not computed")
    else:
        self.output_text_box_5.setPlainText(str(self.calc_instance_2.area_ratio))
        self.output_text_box_6.setPlainText("Not computed")

    if self.calc_choice_instance.user_extra_outputs == 1: 
        self.dialog_2.disp_values(self)
        # self.dialog_2.accept()
    if self.calc_instance_2.cstar is not None: 
        self.Calc_button_3.setEnabled(True)


# To connect calculate button in mono_prop_tab
def mono_func_button(self): 
    # Read the user input values
    self.calc_instance_2 = CalcSet(chamber_pressure=0,cstar = 0, chamber_temp= 0 ,vac_isp=0)
    self.calc_instance = self.calc_instance_2
    
    # pc = self.input_pc.value() *14.504 # Converts the input pressure to psia 
    # self.calc_instance.chamber_pressure = pc 
    self.calc_instance.chamber_pressure = self.input_pc.value() # user inputs the pressure in bar   


    #self.calc_instance.ox = self.OxBox.currentText()
    #self.calc_instance.of_ratio = self.input_of.value()

    self.calc_instance.mono_prop_name = self.mono_prop_box.currentText()
    #self.calc_instance.fuel = self.FuBox.currentText()
    self.calc_instance.amb_pressure = self.input_p_amb.value() 

    if self.nozzle_radio.isChecked(): 
        self.calc_instance.area_ratio = self.nozzle_rat.value() 
        self.calc_choice_instance.nzzl_ch = 1
        self.calc_choice_instance.exit_ch = 0
    else:
        self.calc_instance.exit_pressure = self.exit_p.value() # Convert from Pa user input units to psi
        self.calc_choice_instance.exit_ch = 1
        self.calc_choice_instance.nzzl_ch  = 0
    
    # Check what the user selected in the radio selection menu 
    
    if self.eq_button.isChecked():
        self.calc_instance.flg1 = 0
        self.calc_instance.flg2 = 0
        self.calc_instance.solver_setting = "Equilibrium throughout"

    if self.frz_ch.isChecked():
        self.calc_instance.flg1 = 1
        self.calc_instance.flg2 = 0
        self.calc_instance.solver_setting = "Flow frozen after combustion chamber"

    if self.frz_throat.isChecked(): 
        self.calc_instance.flg1 = 1
        self.calc_instance.flg2 = 1
        self.calc_instance.solver_setting = "Flow frozen after nozzle throat"

    # self.calc_instance_2 = CalcSet(chamber_pressure=0,cstar = 0, chamber_temp= 0 ,vac_isp=0)
    self.calc_instance_2 = mono_prop_compute_val(self.calc_instance,self.calc_choice_instance)
    self.output_text_box.setPlainText(str(self.calc_instance_2.cstar))
    self.output_text_box_2.setPlainText(str(self.calc_instance_2.vac_isp))
    self.output_text_box_4.setPlainText(str(self.calc_instance_2.isp_amb))
    self.output_text_box_3.setPlainText(str(self.calc_instance_2.chamber_temp))
    if self.nozzle_radio.isChecked():
        self.output_text_box_6.setPlainText(str(self.calc_instance_2.exit_pressure))
        self.output_text_box_5.setPlainText("Not computed")
    else:
        self.output_text_box_5.setPlainText(str(self.calc_instance_2.area_ratio))
        self.output_text_box_6.setPlainText("Not computed")


    if self.calc_choice_instance.user_extra_outputs == 1: 
        self.dialog_2.disp_values(self)
        #self.dialog_2.accept()
    
    if self.calc_instance_2.cstar is not None: 
        self.Calc_button_3.setEnabled(True)


def fun_save_csv(self):
    if self.calc_instance_2.mono_prop_name is None:
        string_1 = self.calc_instance_2.fuel
        string_2 = self.calc_instance_2.ox
    else: 
        string_1 = self.calc_instance_2.mono_prop_name
        string_2 = "Monopropellant"
    string_3 = ".csv"
    # file_string = string_1 + "_" + string_2 + string_3
    
    data_dict = asdict(self.calc_instance_2) #THis one makes the dataclass into a dictionary. Key is the field name and the value is the corresponding attribute value.
    
    strng_not_write_1 = "flg1"
    strng_not_write_2 = "flg2"
    text,ok = QInputDialog.getText(self,"Enter Filename","Please enter your preferred filename")
    if not ok or not text.strip():
        return

    if ok and text:
        current_dir = Path.cwd()
        results_dir = current_dir/"Results (Desktop_CEA)"
        results_dir.mkdir(parents = True,exist_ok=True)
        text = text + string_3
        save_path = results_dir/text

        # self.sc.fig.savefig(save_path, bbox_inches='tight', dpi=300)


    with open(save_path,mode = "w" ,newline="",encoding="utf-8") as file: 
        writer = csv.writer(file)

        for field_name,value in data_dict.items(): 
            row_label  = var_mapping.get(field_name,field_name) # Writing field_name twice ensures that if key = field_name does not have a corresponding string in dictionary, it just returns field_name as row_label instead of none
            if row_label != strng_not_write_1 and row_label != strng_not_write_2: #Basically don't write the flg1 and flg2 data values in the final csv results file 
                if value is not None:
                    writer.writerow([row_label,value])

    self.Calc_button_3.setEnabled(False)


