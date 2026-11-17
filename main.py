from pathlib import Path
import time

from PySide6.QtWidgets import QApplication,QSplashScreen
from PySide6.QtGui import QIcon,QPixmap
from PySide6.QtCore import Qt,QSize

## Initialize the application, window and layout objects

app = QApplication() 

# Resolve bundled resources relative to this module, not the launch folder.
icon_path = Path(__file__).resolve().with_name("icon.png")
pixmap = QPixmap(str(icon_path))

#Scale the icon
pixmap = pixmap.scaled(
    QSize(250, 250), 
    Qt.KeepAspectRatio, 
    Qt.SmoothTransformation
)

# Make the flashscreen object so that the icon is shown right after the program is started
splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
splash.show()
app.processEvents()

    

app.setWindowIcon(QIcon(str(icon_path)))

# Load the application after painting the splash so it covers these imports.
from gui.gui_class import MainWindow

# Now the MainWindow contains two tabs
window = MainWindow()

time.sleep(1.75) #Wait for 1.75 seconds before opeining the GUI

window.show() # Shows the window 
splash.finish(window)
app.exec() # Starts the event loop, which waits for things like mouse clicks, keyboard inputs and button presses among others


