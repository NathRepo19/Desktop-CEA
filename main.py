from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from gui.gui_class import MainWindow

## Initialize the application, window and layout objects

app = QApplication() 

app.setWindowIcon(QIcon(str(Path(__file__).resolve().with_name("icon.png"))))


# Now the MainWindow contains two tabs
window = MainWindow()
window.show() # Shows the window 

app.exec() # Starts the event loop, which waits for things like mouse clicks, keyboard inputs and button presses among others


