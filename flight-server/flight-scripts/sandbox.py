#!/usr/bin/python

drop_spacing = 5
total_rows = 4
total_columns = 4

# def target_location():

for column in range(1, total_columns+1):

		for row in range(1, total_rows+1): # runs until the second to last row (loops go to 1 before second argument)

			print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
			print('Dropping seeds..')

			if column % 2 != 0 and row != total_rows: # if column is odd
				print('Moving north to:')
				print( drop_spacing * (row), drop_spacing * (column - 1) )
			elif column % 2 == 0  and row != total_rows: # if column is even
				print('Moving south to')
				print( drop_spacing * (total_rows - 1) - drop_spacing * (row), drop_spacing * (column - 1) )
	
		# print('Dropping seeds..')

		if column == total_columns: # runs when the last row and column have been reached
			print('Column: %d, Row: %d' % (column, row)) # print what column and row currently at
			print('Returning Home')
		else: # this runs when the drone has reached the last row of column but not last column
			if column % 2 != 0: # if column is odd and last row in column
				print('Moving east to new column:')
				print(drop_spacing * (total_rows - 1), drop_spacing * (column))
			elif column % 2 == 0: # if column is even and last row in column
				print('Moving east to new column:')
				print( 0, drop_spacing * (column))