from PySide6.QtWidgets import QMainWindow,QTabWidget,QDialog
from PySide6.QtCore import Qt
from solver.calc_engine import compute_val
from solver.propellants_list import OXIDIZERS,FUELS




from gui.tab_definitions import MonoPropTab,BiPropTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desktop CEA")
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = MonoPropTab()
        self.tab2 = BiPropTab()

        # if self.tab1.calc_choice_instance.user_extra_outputs == 1:
        #     self.tabs.setTabEnabled(1,False)
        # elif self.tab2.calc_choice_instance.user_extra_outputs == 1: 
        #     self.tabs.setTabEnabled(0,False)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        # # Add the instantiated views into the tab layout
        self.tabs.addTab(self.tab1, "Monopropellant")
        self.tabs.addTab(self.tab2, "Bipropellant")

    # Function that activates once user tries to change tabs. It checks if the user has the output dialog popup open to decide whether to let user change tabs
    def on_tab_changed(self):
        if self.tab1.calc_choice_instance.user_extra_outputs == 1: 
            self.tabs.setTabEnabled(1,False)
            self.tab1.dialog_2.finished.connect(self.pop_close_open_biprop)

        if self.tab1 is True: 
            self.tab1.input_of = None


        if self.tab2.calc_choice_instance.user_extra_outputs == 1: 
            self.tabs.setTabEnabled(0,False)
            self.tab2.dialog_2.finished.connect(self.pop_close_open_mono)

    # Function to renable bi_prop tab once user closes the mono_prop output dialog
    def pop_close_open_biprop(self):
        self.tabs.setTabEnabled(1,True)

    # Function to renable...once user closes bi_prop output dialog
    def pop_close_open_mono(self):
        self.tabs.setTabEnabled(0,True)


