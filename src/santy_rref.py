from fractions import Fraction
import copy

matrix_steps = []
want_fractions = 0

def print_matrix(matrix, rows):
    for i in range(0, rows):
        print(matrix[i])
    print("-------------------------")

def swap_rows(matrix, a, b, cols):
    for i in range(0, cols):
        temp = matrix[a][i]
        matrix[a][i] = matrix[b][i]
        matrix[b][i] = temp
    
def order_matrix(matrix, rows, cols):
    global matrix_steps
    # order the matrix to be as staircase as possible off the bat
    for k in range(0, rows):
        current_row = rows - 1 - k
        bottom_row = current_row
        max_leading_zeros = 0
        for i in range(0, current_row + 1):
            leading_zeros = 0
            for j in range(0, cols):
                if matrix[i][j] == 0:
                    leading_zeros = leading_zeros + 1
                else:
                    break
            if leading_zeros > max_leading_zeros:
                max_leading_zeros = leading_zeros
                bottom_row = i
        # swap the bottom row with the new bottom row if they're different
        if bottom_row != current_row:
            swap_rows(matrix, current_row, bottom_row, cols)
            matrix_steps.append("Swap rows {} and {}".format(current_row + 1, bottom_row + 1))
            matrix_steps.append(copy.deepcopy(matrix))    

def rref(matrix, rows, cols):
    # first make sure it is as stair-case as possible
    order_matrix(matrix, rows, cols)

    # variable to keep track of any offsets in the matrix
    row_offset = 0

    # go column to column
    for current_col in range(0, cols):
        # if the matrix is not a square then we need to make sure we don't go out of bounds
        if current_col > rows - 1:
            break;
        # go down the column
        # if the pivot point that we are looking at is a 0 it means all the values under it are
        # also 0 so we move on to the next column and add increase the offset by 1
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
    # first print some lines to separate the matrix
    for i in range(0, cols):
        print("-----", end = "")
    # first thing on it is the matrix, so print that
    print("\noriginal matrix\n")
    for i in range(0, rows):
        print("[", end = " ")
        for j in range(0, cols):
            print(matrix_steps[0][i][j], end = "   ")
        print(" ]")
    for i in range(0, cols):
        print("-----", end = "")
    print("")
    
    # now begins the loop where we print (change then matrix)
    for i in range(1, len(matrix_steps)):
        if i % 2 != 0:            
            # print the string
            print(matrix_steps[i], "\n")
        else:
            # print the matrix
            for j in range(0, rows):
                print("[", end = "    ")
                for k in range(0, cols):
                    if want_fractions == 1:
                        print("{:13s}".format(str(Fraction(matrix_steps[i][j][k]).limit_denominator())), end = "  ")
                    else:
                        print("{:8.2f}".format(matrix_steps[i][j][k]), end = "  ")
                print("]")
            for i in range(0, cols):
                print("---------------", end = "")
            print("")
        


            
    
# main
input_matrix = []

row_number = int(input("how many rows?:\n"))
column_number = int(input("how many columns?:\n"))
want_fractions = int(input("Do you want your values in 1) fractions or 2) decimals?\n"))
cur_row = []
# get the matrix from the user
for i in range(0, row_number):
    for j in range(0, column_number):
        cur_row.append(int(input("Row {}, Col {}: ".format(i + 1, j + 1))))
    input_matrix.append(cur_row)
    cur_row = []
# turn it into row reduced echelon form
matrix_steps.append(copy.deepcopy(input_matrix))
rref(input_matrix, row_number, column_number)

print_matrix(matrix_steps, row_number, column_number)





