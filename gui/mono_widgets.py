
from PySide6.QtWidgets import QWidget, QComboBox, QPushButton, QDoubleSpinBox, QRadioButton,QLabel,QVBoxLayout,QGroupBox,QHBoxLayout,QGridLayout

from solver.propellants_list import MONOPROPS,OXIDIZERS,FUELS

# Widget defintions
def drop_down_widgets(self,ch = 1):
    #Initialize an inner container to arrange the oxidizer and fuel drop-down lists and labels in a grid pattern
    self.inner_container = QWidget()
    if ch == 1:
        self.inner_layout  = QVBoxLayout(self.inner_container)
        
        self.Prop_Label = QLabel("Select Monopropellant")
        self.mono_prop_box = QComboBox()
        self.mono_prop_box.addItems(MONOPROPS)


        self.inner_layout.addWidget(self.Prop_Label)
        self.inner_layout.addWidget(self.mono_prop_box)

        # Add the inner container to the overall layout object
        self.layout.addRow(self.inner_container)

    else:
        
        self.inner_layout = QGridLayout(self.inner_container)

        # Drop-down menu to input oxidizer species
        self.ox_label = QLabel("Choose Oxidizer")
        self.OxBox = QComboBox()
        self.OxBox.addItems(OXIDIZERS)

        # Drop-down menu to input fuel species 
        self.fu_label = QLabel("Choose Fuel")
        self.FuBox = QComboBox()
        self.FuBox.addItems(FUELS)

        # Add the widgets to the grid-type inner-layout object 
        self.inner_layout.addWidget(self.OxBox,1,0)
        self.inner_layout.addWidget(self.FuBox,1,1)
        self.inner_layout.addWidget(self.ox_label,0,0)
        self.inner_layout.addWidget(self.fu_label,0,1)

        # Add the inner container to the overall layout object
        self.layout.addRow(self.inner_container)


def button_widgets(self,ch = 1):
    #Add the main calculation button 
    self.Calc_Button = QPushButton("Calculate")
    self.Calc_Button.setToolTip("Click this button to calculate outputs based on inputs and currently selected conditions")
    
    if ch == 1: 
        self.Calc_Button.clicked.connect(self.calc_func)
    else: 
        self.Calc_Button.clicked.connect(self.func_button)
    

    # Add the button that lets users choose more output parameters
    self.Calc_button_2 = QPushButton("Select Additional Outputs")
    self.Calc_button_2.setToolTip("Click this button to select additional outputs you want to be calculated")

    self.Calc_button_3 = QPushButton("Export Results to CSV")
    self.Calc_button_3.setToolTip("Click to export current calculation data to a csv file")
    self.Calc_button_3.setEnabled(False)
    self.Calc_button_3.clicked.connect(self.fun_save_csv)
    

    if ch == 1: 
        self.Calc_button_2.clicked.connect(self.pop_up)
    else: 
        self.Calc_button_2.clicked.connect(self.add_output_func)

    
    # Add buttons to layout
    self.layout.addRow(self.Calc_button_2)
    self.layout.addRow(self.Calc_Button)
    self.layout.addRow(self.Calc_button_3)
    
def button_widget_set_2(self):
    
    
    self.sweep_button = QPushButton("Perform Parameter Sweep")
    self.sweep_button.setToolTip("Calculate parameters for a range of O/F, chamber pressure or nozzle area ratio")
    self.sweep_button.clicked.connect(self.sweep_button_function)
    self.layout.addRow(self.sweep_button)

def input_box_widgets(self,ch = 1):
    self.input_of = None
    if ch == 2:
        self.input_of = QDoubleSpinBox()
        self.input_of.setRange(0.1,100) # Acceptable input range 
        self.input_of.setDecimals(2) # Accuracy upto two digits after decimal 
        self.input_of.setSingleStep(0.1)
        self.input_of.setValue(2.5) # Default O/F ratio 

        


    # Input box to input chamber pressure 
    self.input_pc = QDoubleSpinBox()
    self.input_pc.setRange(0.1,500) # Acceptable range of chamber pressures in bar 
    self.input_pc.setDecimals(2)
    self.input_pc.setSingleStep(0.5)
    self.input_pc.setValue(20) # Default chamber pressure 
    self.input_pc.setSuffix("bar")

    # Input box to input ambient pressure 
    self.input_p_amb = QDoubleSpinBox()
    self.lim_p_amb = self.input_pc.value() * 0.5 
    self.input_p_amb.setRange(0.0,self.lim_p_amb) # User cannot enter ambient pressure that exceeds choking threshold of ~ half of chamber pressure
    self.input_p_amb.setDecimals(2)
    self.input_p_amb.setSingleStep(0.5)
    self.input_p_amb.setValue(1) # Default set to 1 bar which is ~ atmospheric
    self.input_p_amb.setSuffix("bar")

    # Input box for nozzle area ratio 

    self.nozzle_rat = QDoubleSpinBox()
    self.nozzle_rat.setRange(1.2,1000)
    self.nozzle_rat.setDecimals(2)
    self.nozzle_rat.setSingleStep(1)
    self.nozzle_rat.setValue(40)

    # Input box for exit pressure
    
    self.exit_p = QDoubleSpinBox()
    self.exit_p.setRange(10,200000) # User can enter exit pressure inputs fromm 10 Pa to 200,000 Pa or 2 bar 
    self.exit_p.setDecimals(2)
    # self.exit_p.setSingleStep(0.1)
    self.exit_p.setValue(50000)
    self.exit_p.setSuffix("Pa")


    #self.layout.addRow("O/F Ratio: ",self.input_of)
    if ch == 2: 
        self.layout.addRow("O/F Ratio: ", self.input_of)
    self.layout.addRow("Chamber Pressure: ",self.input_pc)
    self.layout.addRow("Ambient Pressure: ",self.input_p_amb)
    self.layout.addRow("Nozzle Area Ratio: ",self.nozzle_rat)
    self.layout.addRow("Exit Pressure", self.exit_p)


def radio_widgets(self):

    # Group 1: Choose whether eps or exit pressure specification
    self.grp_1_radio = QGroupBox("Exit Condition Specifier")
    self.grp_1_layout = QHBoxLayout(self.grp_1_radio)

    self.nozzle_radio = QRadioButton("Specify Nozzle Area Ratio")
    self.exit_p_radio = QRadioButton("Specify Exit Pressure In Pa")
    self.nozzle_radio.setChecked(True) # Default selection 

    self.nozzle_radio.toggled.connect(self.exit_condition_func)
    

    self.grp_1_layout.addWidget(self.nozzle_radio)
    self.grp_1_layout.addWidget(self.exit_p_radio)




    # Add widget to let the user choose between frozen solve and equiilibrium 
    self.grp_2_radio = QGroupBox("Solver Settings")
    self.grp_2_layout = QVBoxLayout(self.grp_2_radio)

    self.eq_button = QRadioButton("Equilibrium upto exit")
    self.frz_ch = QRadioButton("Frozen at Chamber")
    self.frz_throat = QRadioButton("Frozen at Throat")
    self.eq_button.setChecked(True) # The default solver choice is equilibrium 

    self.grp_2_layout.addWidget(self.eq_button)
    self.grp_2_layout.addWidget(self.frz_throat)
    self.grp_2_layout.addWidget(self.frz_ch)

    self.layout.addRow(self.grp_1_radio)
    self.layout.addRow(self.grp_2_radio)


def output_box_widgets(self):

    ## Add results boxes to display computation results 

    # The following output boxes will be displayed by default, regardless of user choice
    self.output_text_box = self.create_add_output(self.layout,"Characteristic Velocity (m/s)")
    self.output_text_box_2 = self.create_add_output(self.layout,"Vacuum Specific Impulse (s)")
    self.output_text_box_4 = self.create_add_output(self.layout,"Ambient Specific Impulse (s)")
    self.output_text_box_3 = self.create_add_output(self.layout,"Adiabatic Flame Temperature (K)")
    self.output_text_box_5 = self.create_add_output(self.layout,"Nozzle Area Ratio")
    self.output_text_box_6 = self.create_add_output(self.layout,"Exit Pressure (Pa)")







