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
        self.fractions_check.setChecked(True)
    
    def get_matrix(self):
        # store the info they just gave
        global row_number
        global column_number
        global want_fractions

        # need to make sure they fully input all of the data before pressing next so the program doesn't crash
        errors = 0
        # start to take in the input
        # don't proceed if they leave a line blank which is optional
        if str(self.row_selection.currentText()) == "Select an option:":          
            self.error_1.setText("Select a valid row number.")
            errors += 1
        else:
            self.error_1.setText('')
            row_number = int(self.row_selection.currentText())

        if str(self.column_selection.currentText()) == "Select an option:": 
            self.error_2.setText("Select a valid column number.")
            errors += 1
        else:
            self.error_2.setText('')
            column_number = int(self.column_selection.currentText())  

        if self.fractions_check.isChecked:
            want_fractions == True
        
        else:
            want_fractions == False

        if errors == 0:
            matrix_screen = Matrix()
            widget.addWidget(matrix_screen)
            widget.setCurrentIndex(widget.currentIndex()+1)    
            

class Matrix(QDialog):
    def __init__(self):
        super(Matrix, self).__init__()
        loadUi("matrix.ui", self)
        self.add_boxes()

    def add_boxes(self):
        if column_number < 6:
            self.box16.resize(0,0)
            self.box26.resize(0,0)
            self.box36.resize(0,0)
            self.box46.resize(0,0)
            self.box56.resize(0,0)
            self.box66.resize(0,0)
        if column_number < 5:
            self.box15.resize(0,0)
            self.box25.resize(0,0)
            self.box35.resize(0,0)
            self.box45.resize(0,0)
            self.box55.resize(0,0)
            self.box65.resize(0,0)            
        if column_number < 4:
            self.box14.resize(0,0)
            self.box24.resize(0,0)
            self.box34.resize(0,0)
            self.box44.resize(0,0)
            self.box54.resize(0,0)
            self.box64.resize(0,0)                    
        if column_number < 3:
            self.box13.resize(0,0)
            self.box23.resize(0,0)
            self.box33.resize(0,0)
            self.box43.resize(0,0)
            self.box53.resize(0,0)
            self.box63.resize(0,0) 
        if column_number < 2: 
            self.box12.resize(0,0)
            self.box22.resize(0,0)
            self.box32.resize(0,0)
            self.box42.resize(0,0)
            self.box52.resize(0,0)
            self.box62.resize(0,0)
        if row_number < 6:
            self.box61.resize(0,0)
            self.box62.resize(0,0)
            self.box63.resize(0,0)
            self.box64.resize(0,0)
            self.box65.resize(0,0)
            self.box66.resize(0,0)
        if row_number < 5:
            self.box51.resize(0,0)
            self.box52.resize(0,0)
            self.box53.resize(0,0)
            self.box54.resize(0,0)
            self.box55.resize(0,0)
            self.box56.resize(0,0)
        if row_number < 4:
            self.box41.resize(0,0)
            self.box42.resize(0,0)
            self.box43.resize(0,0)
            self.box44.resize(0,0)
            self.box45.resize(0,0)
            self.box46.resize(0,0)
        if row_number < 3:
            self.box31.resize(0,0)
            self.box32.resize(0,0)
            self.box33.resize(0,0)
            self.box34.resize(0,0)
            self.box35.resize(0,0)
            self.box36.resize(0,0)
        if row_number < 2:
            self.box21.resize(0,0)
            self.box22.resize(0,0)
            self.box23.resize(0,0)
            self.box24.resize(0,0)
            self.box25.resize(0,0)
            self.box26.resize(0,0) 
            self.box62.resize(0,0) 
         

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