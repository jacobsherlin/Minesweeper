# Name: Jacob Sherlin
# Text-based minesweeper game.
import random

#display board
def displayBoard(board):
	print('\n       0     1     2     3     4')
	print() #two newlines
	i=0
	rows = 0 # count rows
	while i < len(board):
		if i % 5 == 0 and i == 0:
			print(rows, '  |', end='')
			rows +=1
		elif i % 5 == 0 and i != 0:
			print('\n    -------------------------------') #newline
			print(rows, '  |', end='')
			rows +=1
		print('', board[i], '  |', end='' )
		i+=1
	print('\n\n') #two newlines

#output board into text file
def outputBoard(board, moves):	
    with open('output.txt', 'w') as outfile:
        outfile.write('     0    1    2    3    4\n\n')
        i = 0
        rows = 0  # count rows
        while i < len(board):
            if i % 5 == 0 and i == 0:
                outfile.write(f"{rows}  |")
                rows += 1
            elif i % 5 == 0 and i != 0:
                outfile.write('\n   --------------------------\n')
                outfile.write(f"{rows}  |")
                rows += 1
            outfile.write(f" {board[i]}  |")
            i += 1
        outfile.write('\n\nMoves Made:\n')
        
        i = 0
        while i < len(moves):
            if i + 1 < len(moves):
                outfile.write(f'Move {i//2 + 1}: {moves[i]}, {moves[i+1]}\n')
            i += 2


#open cells
def open_cell(board, game, i, visited):
    if i in visited:
        return 0
    visited.add(i)
    
    if game[i] == 'B':
        # This should not happen if the function is called correctly
        return 0
    
    if game[i] == '0':
        board[i] = ' '
        counter = 1
        adjacent_indices = [
            i - 6, i - 5, i - 4, i - 1,
            i + 1, i + 4, i + 5, i + 6
        ]
        for adj in adjacent_indices:
            if 0 <= adj < 25 and adj not in visited:
                counter += open_cell(board, game, adj, visited)
    else:
        board[i] = game[i]
        counter = 1

    return counter

#check spaces
def check(board):
	rocks=0
	for i in board:
		if i == '\U0001FAA8' or i == '\U0001F6A9':
			rocks+=1
	if rocks <= 4:
		return True
	else:
		return False

#get coordinates
def getCoord(moves):
	row = int(input("Enter Row: "))
	if row < 0 or row > 4:
		while row < 0 or row > 4:
			print("\nPlease enter a number between 0 and 4.")
			row = int(input("Enter Row: "))
	moves.append(row)
	col = int(input("Enter Column: "))
	if col < 0 or col > 4:
		while col < 0 or col > 4:
			print("\nPlease enter a number between 0 and 4.")
			col = int(input("Enter Col: "))
	moves.append(col)
	coord = (5*row)+col
	return coord
	
#gameover
def gameOver(game, moves):
	#output board
	outputBoard(game, moves)
	i=0
	while i < len(game):
		if game[i] == 'B':
			game[i] = '\U0001F4A5' #all bombs explode
		elif game[i] == '0':
			game[i] = ' '
		i+=1
	displayBoard(game)
	print("Game Over\nThanks for Playing!")
	

#win
def win(game, moves):
	#output board
	outputBoard(game, moves)
	i=0
	while i < len(game):
		if game[i] == 'B':
			game[i] = '\U0001F4A3' #all bombs explode
		elif game[i] == '0':
			game[i] = ' '
		i+=1
	displayBoard(game)
	print("You win!\nThanks for Playing!")

#main function
def main():
	#initialize board
	board = []
	i=0
	while i < 25:
		board.append('\U0001FAA8') #rock emoji unicode
		i+=1
	#initialize gameplay board
	game = []
	i=0
	while i < 25:
		game.append('0') #fill with zeroes
		i+=1
	#generate 4 random numbers for coordinates
	random_nums = random.sample(range(0, 24 + 1), 4)
	#add bombs to gameplay board
	i = 0
	while i < 4:
		game[random_nums[i]] = 'B'
		i+=1

	#create coordinates
	i = 0
	while i < 25:
		if game[i] != 'B':
			coordinates = 0
			if i >= 6 and game[i-6] == 'B' and i % 5 != 0:
				coordinates+=1
			if i >= 5 and game[i-5] == 'B':
				coordinates+=1
			if i >= 4 and game[i-4] == 'B' and i != 4 and i != 9 and i != 14 and i != 19 and i != 24:
				coordinates+=1
			if i >= 1 and game[i-1] == 'B' and i % 5 != 0:
				coordinates+=1
			if i <= 23 and game[i+1] == 'B' and i != 4 and i != 9 and i != 14 and i != 19 and i != 24:
				coordinates+=1
			if i <= 20 and game[i+4] == 'B' and i % 5 != 0:
				coordinates+=1
			if i <= 19 and game[i+5] == 'B':
				coordinates+=1
			if i <= 18 and game[i+6] == 'B' and i != 4 and i != 9 and i != 14 and i != 19 and i != 24:
				coordinates+=1
			if coordinates > 0:
				game[i] = coordinates
		i+=1 #increment loop
	#visited list
	visited = set()
	#moves list
	moves = []
	#gameplay
	displayBoard(board)
	coord = getCoord(moves)
	if game[coord] == 'B':
		gameOver(game, moves)
		return
	elif game[coord] != '0':
		board[coord] = game[coord]
	else:
		open_cell(board, game, coord, visited)
	#gameplay loop
	counter = False
	while counter != True:
		displayBoard(board)
		#flag option
		flag = input("Would you like to enter a flag? (Y / N): ")
		if flag == 'Y' or flag == 'y':
			coord = getCoord(moves)
			board[coord] = '\U0001F6A9'
		else:
			coord = getCoord(moves)
			if game[coord] == 'B':
				gameOver(game, moves)
				return
			elif game[coord] != '0':
				board[coord] = game[coord]
			else:
				open_cell(board, game, coord, visited)
		counter = check(board)
	win(game, moves)
if __name__ == "__main__":
	main()