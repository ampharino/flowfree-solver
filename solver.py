
import copy
import time
domain = []
sources = []
remaining_values = {}

def printResult(assignment):
	output = ''
	for line in assignment:
		output+= "".join(line)
		output+='\n'
	print(output)


def getPuzzle(file):
	with open(file) as file:
		lines = [list(line.strip()) for line in file]
	return lines

#Finds source cells	
def getSource(assignment):
	for row,line in enumerate(assignment):
			for column,square in enumerate(line):
				if square != '_':
					sources.append((row, column))
def getDomain(assignment):
	for row,line in enumerate(assignment):
			for column,square in enumerate(line):
				if square != '_' and square != '\n':
					if square not in domain:
						domain.append(square)

#Get each variable's remaining values for forward checking
def getRemainingValues(assignment):
	for y,line in enumerate(assignment):
			for x,square in enumerate(line):
				if square == '_':
					neighbor_value = []
					empty_neighbors = 0
					if y < len(assignment)-1:
						if assignment[y+1][x] != '_':
							neighbor_value.append(assignment[y+1][x])
						else:
							empty_neighbors+=1
		
					if y > 0:
						if assignment[y-1][x] != '_':
							neighbor_value.append(assignment[y-1][x])
						else:
							empty_neighbors+=1

					if x < len(assignment[0])-1:
						if assignment[y][x+1] != '_':
							neighbor_value.append(assignment[y][x+1])
						else:
							empty_neighbors+=1

					
					if x > 0:
						if assignment[y][x-1] != '_':
							neighbor_value.append(assignment[y][x-1])
						else:
							empty_neighbors+=1

					if len(neighbor_value) == 0:
						remaining_values[(y,x)] = domain.copy()
					else:
						temp = domain.copy()
						for value in domain:
							count = neighbor_value.count(value)
							if count > 2:
								temp.remove(value)
							if count < 2 and (count+empty_neighbors < 2):
								temp.remove(value)
						remaining_values[(y,x)] = temp.copy()
				else:
					if (y,x) in remaining_values:
						del remaining_values[(y,x)]

#Not used
def getMostConstrained():
	temp = sorted(remaining_values, key=lambda k: len(remaining_values[k]))
	return temp[0]

	


def checkConstraints(assignment, row, column, value):
	temp = copy.deepcopy(assignment)
	temp[row][column] = value
	for y,line in enumerate(temp):
			for x,square in enumerate(line):
				if square == '_':
					continue
				same_neighbors = 0
				empty_neighbors = 0
				different_neighbors = 0
				if y < len(temp)-1:
					if temp[y+1][x] == temp[y][x]:
						same_neighbors+=1
					elif temp[y+1][x] == '_':
						empty_neighbors+=1
					else:
						different_neighbors+=1
				if y > 0:
					if temp[y-1][x] == temp[y][x]:
						same_neighbors+=1
					elif temp[y-1][x] == '_':
						empty_neighbors+=1
					else:
						different_neighbors+=1
				if x < len(temp[0])-1:
					if temp[y][x+1] == temp[y][x]:
						same_neighbors+=1
					elif temp[y][x+1] == '_':
						empty_neighbors+=1
					else:
						different_neighbors+=1
				if x > 0:
					if temp[y][x-1] == temp[y][x]:
						same_neighbors+=1
					elif temp[y][x-1] == '_':
						empty_neighbors+=1
					else:
						different_neighbors+=1
				if (y,x) in sources:
					if same_neighbors > 1:
						#print("{} is not valid. row:{} column:{} Failed condition 1".format(value, y, x))
						return False
					if same_neighbors == 0 and empty_neighbors < 1:
						#print("{} is not valid. row:{} column:{} Failed condition 2".format(value, y, x))
						return False
				else:
					if same_neighbors > 2:
						#print("{} is not valid. row:{} column:{} Failed condition 3".format(value, y, x))
						return False
					if same_neighbors < 2 and (empty_neighbors + same_neighbors < 2):
						#print("{} is not valid. row:{} column:{} Failed condition 4".format(value, y, x))
						return False
						
	#print("{} is valid".format(value))					
	return True


def smartSolver(assignment):
	if any('_' in line for line in assignment):
		temp = copy.deepcopy(assignment)
		for row,line in enumerate(assignment):
			for column,square in enumerate(line):
				if square != '_':
					continue
				for value in remaining_values[(row,column)]:
					if checkConstraints(assignment, row, column, value) == True:
						#print("Assigning value")
						assignment[row][column] = value
						getRemainingValues(assignment)
						violation = any(len(value) == 0 for value in remaining_values.values())
						if not violation:
							smartSolver.counter+=1
							#printResult(assignment)
							result = smartSolver(assignment)
							if result != None:
								return result
						#print("resetting assignment")
						assignment = copy.deepcopy(temp)
						#printResult(assignment)
				return None		
	else:
		return assignment


smartSolver.counter = 0
file = input("Enter a puzzle name\n")
assignment = getPuzzle(file)
getSource(assignment)
getDomain(assignment)
getRemainingValues(assignment)
#print(remaining_values)
start = time.time()
assignment1 = smartSolver(assignment)
end = time.time()
print("Final Result:\n")
printResult(assignment1)
print("Total assignments:{}".format(smartSolver.counter))
print("Total time:{}".format(end-start))