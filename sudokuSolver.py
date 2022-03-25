import copy

def PrintSudoku(sudoku):
	for line in sudoku:
		for value in line:
			print(value, end=" ")
		print()

def ReadSudoku(fileName,sudoku):
	f = open(fileName, "r")
	row = 0
	for x in f:
		sudoku[row] = x.rstrip().split(" ")
		# print(sudoku[row])
		row += 1

def CountNUnknownMatrix(matrix):
	nUnknown = 0
	for row in matrix:
		for number in row:
			if not number.isnumeric():
				nUnknown += 1
	return nUnknown

def CountNUnknownVector(vector):
	nUnknown = 0
	for number in vector:
		if not number.isnumeric():
			nUnknown += 1
	return nUnknown

def PrintInfo(sudoku,nIterations):
	print(80*"*")
	print("Iteration",nIterations)
	print(80*"*")
	PrintSudoku(sudoku)

def PrintResult(sudoku):
	print(80*"*")
	print("End")
	print(80*"*")
	PrintSudoku(sudoku)

def GetUnusedVector(vector):
	unUsed = [str(x) for x in range(1,10)]
	for number in vector:
		if number.isnumeric():
			unUsed.remove(number)
	return unUsed

def GetUnusedMatrix(matrix):
	unUsed = [str(x) for x in range(1,10)]
	for line in matrix:
		for number in line:
			if number.isnumeric():
				unUsed.remove(number)
	return unUsed

def GetPossibleColumns(recentRowID,number,sudoku):
	possibleColumns = []
	# print(sudoku[rowID][])
	for columnID in range(9):
		# print(sudoku[rowID][columnID],end=" ")
		if sudoku[recentRowID][columnID].isnumeric():
			continue
		# print(columnID,end=" ")
		hasNumber = False
		for rowID in range(9):
			if sudoku[rowID][columnID] == number:
				hasNumber = True
		if not hasNumber:
			possibleColumns.append(columnID)
	return possibleColumns

def GetPossibleRows(recentColumnID,number,sudoku):
	possibleRows = []
	# print(sudoku[rowID][])
	for rowID in range(9):
		# print(sudoku[rowID][rowID],end=" ")
		if sudoku[rowID][recentColumnID].isnumeric():
			continue
		# print(rowID,end=" ")
		hasNumber = False
		for columnID in range(9):
			if sudoku[rowID][columnID] == number:
				hasNumber = True
				break
		if not hasNumber:
			possibleRows.append(rowID)
	return possibleRows

def GetPossiblePositions(squareID,number,sudoku):
	possiblePossitions = []

	for positionID in range(9):
		# print(sudoku[(positionID//3)+3*(squareID//3)][(positionID%3)+3*(squareID%3)])
		rowPos = (positionID//3)+3*(squareID//3)
		columnPos = (positionID%3)+3*(squareID%3)
		if sudoku[rowPos][columnPos].isnumeric():
			continue
		hasNumber = False;
		for rowID in range(9):
			if sudoku[rowID][columnPos] == number:
				hasNumber = True
				break
		for columnID in range(9):
			if sudoku[rowPos][columnID] == number:
				hasNumber = True
				break
		if not hasNumber:
			possiblePossitions.append(positionID)
	return possiblePossitions

def CheckRows(sudoku):
	solved = 0
	for rowID in range (9):
		if CountNUnknownVector(sudoku[rowID]) != 0:
			unUsedNumbers = GetUnusedVector(sudoku[rowID])
			# print(unUsedNumbers)
			for number in unUsedNumbers:
				# print(number,rowID)
				possibleColumns = GetPossibleColumns(rowID,number,sudoku)
				# print(possibleColumns)
				if len(possibleColumns) == 1:
					sudoku[rowID][possibleColumns[0]] = number
					solved = 1
				if len(possibleColumns) == 0:
					return -1
			# input()
	return solved

def CheckColumns(sudoku):
	solved = 0
	for columnID in range(9):
		if CountNUnknownVector([row[columnID] for row in sudoku]) != 0:
			unUsedNumbers = GetUnusedVector([row[columnID] for row in sudoku])
			# print(unUsedNumbers)
			for number in unUsedNumbers:
				# print(number,rowID)
				possibleRows = GetPossibleRows(columnID,number,sudoku)
				# print(possibleRows)
				if len(possibleRows) == 1:
					sudoku[possibleRows[0]][columnID] = number
					solved = 1
				if len(possibleRows) == 0:
					return -1
			# input()
	return solved

def CheckSquares(sudoku):
	solved = 0
	for squareID in range(9):
		# print([row[3*(squareID%3):3*(squareID%3+1)] for row in sudoku[3*(squareID//3):3*(squareID//3+1)]])
		if CountNUnknownMatrix([row[3*(squareID%3):3*(squareID%3+1)] for row in sudoku[3*(squareID//3):3*(squareID//3+1)]]) != 0:
			unUsedNumbers = GetUnusedMatrix([row[3*(squareID%3):3*(squareID%3+1)] for row in sudoku[3*(squareID//3):3*(squareID//3+1)]])
			# print(unUsedNumbers)
			for number in unUsedNumbers:
				possiblePossitions = GetPossiblePositions(squareID,number,sudoku)
				# print(possiblePossitions)
				if len(possiblePossitions) == 1:
					sudoku[(possiblePossitions[0]//3)+3*(squareID//3)][(possiblePossitions[0]%3)+3*(squareID%3)] = number
					solved = 1
				if len(possiblePossitions) == 0:
					return -1
			# input()
	return solved

def CheckPositions(sudoku,pos):
	smallest = 10
	for x in range(9):
		for y in range(9):
			if sudoku[x][y].isnumeric():
				continue;
			# possibleNumbers = []
			unRow = GetUnusedVector(sudoku[x])
			unColumn = GetUnusedVector(row[y] for row in sudoku)
			squareID = ((x//3)*3)+(y//3)
			unSquare = GetUnusedMatrix([row[3*(squareID%3):3*(squareID%3+1)] for row in sudoku[3*(squareID//3):3*(squareID//3+1)]])
			intersection = set(unRow) & set(unColumn) & set(unSquare)
			if pos == 0:
				if len(intersection) == 1:
					for value in intersection:
						sudoku[x][y] = value
					return 1
				if (len(intersection) < smallest):
					smallest = len(intersection)
			else:
				if len(intersection) == pos:
					for value in intersection:
						# print(sudoku)
						hypotheticalSudoku = copy.deepcopy(sudoku)
						hypotheticalSudoku[x][y] = value
						# print(value)
						# print(sudoku)
						result = SolveSudoku(hypotheticalSudoku,True)
						if (result):
							sudoku[x][y] = value
							# print(sudoku)
							return 1
							# sudoku[x][y] = value
	return smallest



def SolveSudoku(sudoku,hyp = False):
	nIterations = 0
	while(CountNUnknownMatrix(sudoku) != 0):
		if not hyp:
			PrintInfo(sudoku,nIterations)
		# rowsSolved = False
		# columnsSolved = False
		rowsSolved =  CheckRows(sudoku)
		columnsSolved = CheckColumns(sudoku)
		squaresSolved = CheckSquares(sudoku)
		if rowsSolved == -1 or columnsSolved == -1 or squaresSolved == -1:
			print("Error in the solving!!!")
			return False
		# CheckPositions(sudoku)
		if rowsSolved == 0 and columnsSolved == 0 and squaresSolved == 0:
			if hyp:
				print("Unsolvable!!!")
				return False
			print ("No change done! Checking individual positions")
			checkPos = CheckPositions(sudoku,0)
			print(checkPos)
			if checkPos == 1:
				continue
			elif checkPos == 2:
				checkPos = CheckPositions(sudoku,checkPos)
			else:
				print("Unsolvable!!!")
				return False
		nIterations += 1
	return True

if __name__ == "__main__":
	sudoku = [[" "]*9,[" "]*9,[" "]*9,[" "]*9,[" "]*9,[" "]*9,[" "]*9,[" "]*9,[" "]*9]
	fileName = "easy.sud"

	ReadSudoku(fileName,sudoku)
	# PrintSudoku(sudoku)

	solved = SolveSudoku(sudoku)

	if solved:
		PrintResult(sudoku)