from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QInputDialog, QLineEdit, QPushButton
from fractions import Fraction
import copy
import ctypes
import sys

# this sets the icon as your taskbar icon
myappid = 'Row Reducer'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# The code below makes it so that the widget doesn't get messed up if you scale windows text by 125% or more
# Query DPI Awareness (Windows 10 and 8)
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(0)
# the argument is the awareness level, which can be 0, 1 or 2:
# for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)
# Set DPI Awareness  (Windows 7 and Vista)
success = ctypes.windll.user32.SetProcessDPIAware()
# behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems
# to work with effects identical to SetProcessDpiAwareness(1)

# global variables
input_matrix = []
want_fractions = True
row_number = 0
column_number = 0

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui", self)
        self.start_button.clicked.connect(self.start_program)
    # launch the month selector widget when the start button is pressed
    def start_program(self):
        get_input = Input()
        widget.addWidget(get_input)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Input(QDialog):
    def __init__(self):
        super(Input, self).__init__()
        loadUi("input.ui", self)
        self.next_button.clicked.connect(self.get_matrix)
        self.fractions_check.stateChanged.connect(self.check_fractions)
        self.decimals_check.stateChanged.connect(self.check_decimals)
    
    def check_fractions(self):
        global want_fractions
        want_fractions = True
    def check_decimals(self):
        global want_fractions
        want_fractions = False
    
    def get_matrix(self):
        # store the info they just gave
        global row_number
        global column_number
        global want_fractions

        # need to make sure they fully input all of the data before pressing next so the program doesn't crash
        errors = 0
        # start to take in the input
        # don't proceed if they leave a line blank which is optional
        if len(self.input_row.text()) == 0 or str(self.input_row.text()) == '0':
            self.error_1.setText("Enter a valid row number.")
            errors += 1
        else:
            self.error_1.setText('')
            row_number = int(self.input_row.text())

        if len(self.input_column.text()) == 0 or str(self.input_row.text()) == '0':
            self.error_2.setText("Enter a valid column number.")
            errors += 1
        else:
            self.error_2.setText('')
            column_number = int(self.input_column.text())    

        #if errors == 0:
         #   matrix_screen = Matrix()
          #  widget.addWidget(matrix_screen)
           # widget.setCurrentIndex(widget.currentIndex()+1)    
        
        

# main code
app = QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('logo.ico')) # sets the logo
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(921)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("exiting")