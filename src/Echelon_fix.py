from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QInputDialog, QLineEdit, QPushButton
from fractions import Fraction
import copy
import ctypes
import sys
import time
from pathlib import Path

# this sets the icon as your taskbar icon
myappid = 'Echelon'
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
want_fractions = False
row_number = 0
column_number = 0
original_matrix = []
emtpy_matrix = []
exit = []
row1 = []
row2 = []
row3 = []
row4 = []
row5 = []
row6 = []
current_step = 0
output_box = []
speed = 1

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

        if self.fractions_check.isChecked():
            want_fractions = True
            
        elif self.decimals_check.isChecked():
            want_fractions = False

        if errors == 0:
            matrix_screen = Matrix()
            widget.addWidget(matrix_screen)
            widget.setCurrentIndex(widget.currentIndex()+1)    


class Matrix(QDialog):
    def __init__(self):
        super(Matrix, self).__init__()
        loadUi("matrix.ui", self)
        self.add_boxes()
        self.run_button.clicked.connect(self.start_program)
        self.exit_button.clicked.connect(self.close_program)
        self.start_over_button.clicked.connect(self.start_over)

    def start_over(self):
        start_screen = Input()
        widget.addWidget(start_screen)
        widget.setCurrentIndex(widget.currentIndex()+1) 

    def close_program(self):
        QApplication.exit()

    def start_program(self):
        global emtpy_matrix
        global speed
        global matrix_steps
        matrix_steps = []

        # make sure they didn't leave any matrix boxes blank
        error = 0
    
        if str(self.speed_selection.currentText()) == "Select a speed:":          
            self.error_2.setText("Select a valid speed.")
            error += 1
        else:
            self.error_2.setText('')
            temp = str(self.speed_selection.currentText())
            if temp == "Slow":
                speed = 6
            elif temp == "Normal":
                speed = 2
            elif temp == "Fast":
                speed = .5
        
        for i in range(0, row_number):
            for j in range(0, column_number):
                if len(empty_matrix[i][j].toPlainText()) == 0:
                    self.error_1.setText("Please finish the matrix to continue.")
                    error += 1
                else:
                    self.error_1.setText("")

        
        if error == 0:
            cur_row = []
            # get the matrix from the user
            for i in range(0, row_number):
                for j in range(0, column_number):
                    cur_row.append(int(empty_matrix[i][j].toPlainText()))
                input_matrix.append(cur_row)
                cur_row = []
            # turn it into row reduced echelon form
            matrix_steps.append(copy.deepcopy(input_matrix))
            rref(input_matrix, row_number, column_number)

            print_matrix(matrix_steps, row_number, column_number)
            exit[0].resize(100, 71)


    def add_boxes(self):
        self.exit_button.resize(0,0)
        exit.append(self.exit_button)
        global empty_matrix
        global row1 
        global row2 
        global row3 
        global row4 
        global row5 
        global row6
        global output_box
        output_box = []
        output_box.append(self.output)
        empty_matrix = []

        row1 = [self.box11, self.box12, self.box13, self.box14, self.box15, self.box16]
        empty_matrix.append(row1)
        row2 = [self.box21, self.box22, self.box23, self.box24, self.box25, self.box26]
        empty_matrix.append(row2)
        row3 = [self.box31, self.box32, self.box33, self.box34, self.box35, self.box36]
        empty_matrix.append(row3)
        row4 = [self.box41, self.box42, self.box43, self.box44, self.box45, self.box46]
        empty_matrix.append(row4)
        row5 = [self.box51, self.box52, self.box53, self.box54, self.box55, self.box56]
        empty_matrix.append(row5)
        row6 = [self.box61, self.box62, self.box63, self.box64, self.box65, self.box66]
        empty_matrix.append(row6)

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
            

def swap_rows(matrix, a, b, cols):
    for i in range(0, cols):
        temp = matrix[a][i]
        matrix[a][i] = matrix[b][i]
        matrix[b][i] = temp
    
def order_matrix(matrix, rows, cols):
    global matrix_steps
    # go one by one and bubble sort it
    leading_zero_list = []
    count = 0
    for i in range(0, rows):
        leading_zero_list.append(0)
        for j in range(0, cols):
            if matrix[i][j] == 0:
                leading_zero_list[i] += 1
            else:
                break
    for i in range(rows - 1, 0, -1):
        num_swaps = 0
        for j in range(rows - 1, rows - i, -1):
            if leading_zero_list[j] < leading_zero_list[j - 1]:
                temp = leading_zero_list[j]
                leading_zero_list[j] = leading_zero_list[j - 1]
                leading_zero_list[j - 1] = temp
                num_swaps += 1
        if num_swaps > 0:
            swap_rows(matrix, j, j - num_swaps, cols)
            matrix_steps.append("Swap rows {} and {}".format(j + 1, j + num_swaps + 1))
            matrix_steps.append(copy.deepcopy(matrix))

def rref(matrix, rows, cols):
    # first make sure it is as stair-case as possible
    order_matrix(matrix, rows, cols)

    # variable to keep track of any offsets in the matrix
    row_offset = 0

    # go column to column
    for current_col in range(0, cols):
        order_matrix(matrix, rows, cols)
        # if the matrix is not a square then we need to make sure we don't go out of bounds
        if current_col > rows - 1:
            break;

        # go down the column
        # if the pivot point that we are looking at is a 0 it means all the values under it are
        # also 0 so we move on to the next column and add increase the offset by 1
        if matrix[current_col - row_offset][current_col] == 0:
            order_matrix(matrix, rows, cols)
            if matrix[current_col - row_offset][current_col] == 0:
                row_offset = row_offset + 1
                continue

        for current_row in range(current_col - row_offset, rows):
            # find if there are any entries that already have a 1 in that column and swap (convenience)
            if matrix[current_row][current_col] == 1 and current_row != current_col - row_offset:
                swap_rows(matrix, current_row, current_col, cols)
                matrix_steps.append("Swap rows {} and {}".format(current_row + 1, current_col + 1))
                matrix_steps.append(copy.deepcopy(matrix))
        # convert the pivot point of the current column to a 1
        if matrix[current_col - row_offset][current_col] != 1:
            value = matrix[current_col - row_offset][current_col]
            for col in range(current_col, cols):
                matrix[current_col - row_offset][col] = matrix[current_col - row_offset][col] / value
            matrix_steps.append("turn the pivot value of column {} into a 1".format(current_col + 1))
            matrix_steps.append(copy.deepcopy(matrix))

        # convert the values under the current pivot to a 0
        for current_row in range(current_col - row_offset + 1, rows):
            # if the value is already 0 we can skip it
            if matrix[current_row][current_col] == 0:
                continue
            # find the value we need to multiply the current row's leading value by to get this
            # value to 0
            value = (-1 * matrix[current_row][current_col]) / matrix[current_col - row_offset][current_col] 
            # add the multiplied value of each member of the row to the one we want to change the
            # leading value of to 0
            for col in range(current_col, cols):
                matrix[current_row][col] = matrix[current_row][col] + (matrix[current_col - row_offset][col] * value)
            # add this to the matrix steps
            if want_fractions == 1:
                matrix_steps.append("Multiply row {} by {} and add it to row {}".format(current_col - row_offset + 1, str(Fraction(value).limit_denominator()), current_row + 1))
            else:
                matrix_steps.append("Multiply row {} by {:4.1f} and add it to row {}".format(current_col - row_offset + 1, value, current_row + 1))
            matrix_steps.append(copy.deepcopy(matrix)) 
    
    # start from the bottom row and work your way up
    for i in range(0, rows):
        # since we are working backwards I need to change the index
        current_row = rows - i - 1
        # find the first non-zero entry (should be a 1)
        pivot_column = -1
        for j in range(0, cols):
            if matrix[current_row][j] == 1:
                pivot_column = j
                break
        # if pivot is -1, then this row has no pivot so continue up
        if pivot_column == -1:
            continue

        # now that we have the column that the pivot is on, we can make all values above this 0
        for j in range(0, current_row):
            temp_row = current_row - j - 1
            if matrix[temp_row][pivot_column] == 0:
                continue
            # get the value we need to multiply the pivot row by
            value = (-1 * matrix[temp_row][pivot_column]) / matrix[current_row][pivot_column]
            # multiply the value we got by each member of the pivot number's row and add it to the
            # row we want to change
            for k in range(pivot_column, cols):
                matrix[temp_row][k] = matrix[temp_row][k] + (matrix[current_row][k] * value)
            # add this to the matrix steps
            if want_fractions == 1:
                matrix_steps.append("Multiply row {} by {} and add it to row {}".format(current_row + 1, str(Fraction(value).limit_denominator()), temp_row + 1))
            else:
                matrix_steps.append("Multiply row {} by {:4.1f} and add it to row {}".format(current_row + 1, value, temp_row + 1))
            matrix_steps.append(copy.deepcopy(matrix))  

def print_matrix(matrix_steps, rows, cols):
    global empty_matrix
    downloads_path = str(Path.home() / "Downloads")
    downloads_path = downloads_path + "/steps.txt"
    file = open(downloads_path, "a")

    # first file.write some lines to separate the matrix
    file.write("-----------------------------------------------------")
    # first thing on it is the matrix, so file.write that
    file.write("\n\noriginal matrix\n\n")
    for i in range(0, rows):
        file.write("[")
        for j in range(0, cols):
            file.write("   {:13s}   ".format(str(Fraction(matrix_steps[0][i][j]).limit_denominator())) + "   ")
        file.write(" ]\n")
    file.write("-----------------------------------------------------")
    file.write("")

    global current_step
    
    # now begins the loop where we file.write (change the matrix)
    for i in range(1, len(matrix_steps)):
        if i % 2 != 0:            
            # file.write the string
            file.write("\n" + str(matrix_steps[i]) + "\n")
            file.write("-----------------------------------------------------\n")
            output_box[0].clear()
            output_box[0].setText(str(matrix_steps[i]))
            # this is what would go into the text box
        else:
            # file.write the matrix
            for j in range(0, rows):
                file.write("[    ")
                for k in range(0, cols):
                    if want_fractions == 1:
                        file.write("   {:13s}   ".format(str(Fraction(matrix_steps[i][j][k]).limit_denominator())))
                        empty_matrix[j][k].clear()
                        empty_matrix[j][k].setText("{:7s}".format(str(Fraction(matrix_steps[i][j][k]).limit_denominator())))
                    else:
                        file.write("   {:8.2f}   ".format(matrix_steps[i][j][k]))
                        empty_matrix[j][k].clear()
                        empty_matrix[j][k].setText("{:8.2f}".format(matrix_steps[i][j][k]))
                file.write("]\n")
           
            
            file.write("-----------------------------------------------------")
            file.write("")

        QApplication.processEvents()
        time.sleep(speed)

        


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