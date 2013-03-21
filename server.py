# server.py
#
#Tic-Tac-Toe by Andy Woo
#
# Last Updated: 12/02/2013

#!C:\python27

import socket
import sys
import time
import string

# Take input parameter for PORT
PORT = int(sys.argv [1])
BUFFER = 1024
TCP_IP = 'localhost'
clients = 0
# List of 2 socket objects for the 2 players
client_list = [] 


###### DECLARING ALL LOCAL FUNCTIONS FIRST

# This function sends the current board to both players
def sendBoards():
	# Print to the server the same board being sent
	printBoard()

	# Sending...
	for i in range(0,2):
		theBoard = ""
		theBoard += '\nCurrent board: \n\n'+' '+str(board[0])+' '+'|'+' '+str(board[1])+' '+'|'+' '+str(board[2])+'\n---+---+---\n'+' '+str(board[3])+' '+'|'+' '+str(board[4])+' '+'|'+' '+str(board[5])+'\n---+---+---\n'+' '+str(board[6])+' '+'|'+' '+str(board[7])+' '+'|'+' '+str(board[8])+'\n'
		client_list[i].sendall(theBoard)


# This function prints the board on the server window for reference
def printBoard():
	print '\nCurrent board: \n\n',' '+str(board[0])+' '+'|'+' '+str(board[1])+' '+'|'+' '+str(board[2]), '\n---+---+---\n'+' '+str(board[3])+' '+'|'+' '+str(board[4])+' '+'|'+' '+str(board[5]), '\n---+---+---\n'+' '+str(board[6])+' '+'|'+' '+str(board[7])+' '+'|'+' '+str(board[8]), '\n'


# This function sends friendly goodbye messages at end of game
def goodbye(a):
	# Friendly goodbye messages
	client_list[a].sendall('\nYOU WIN!')
	print '\n\nPLAYER', a, 'WINS!'
	if a == 0: a = 1
	elif a == 1: a = 0
	client_list[a].sendall('\nYOU LOSE!')

	# Also send final boards to both players
	sendBoards()


# This function checks if the game is over (victory or draw)
def checkGame(n,m):

	# CHECK FOR VICTORY:
	# Check the column of the newly played position
	if (board[n] == board[(n+3)%9] == board[(n+6)%9]):
		# WIN!
		goodbye(m)
		return True

	# Check the row of the newly played position
	if ((n==0) or (n==1) or (n==2)):
		offset = 0
	elif ((n==3) or (n==4) or (n==5)):
		offset = 3
	elif ((n==6) or (n==7) or (n==8)):
		offset = 6
	if (board[(n%3)+offset] == board[((n+1)%3)+offset] == board[((n+2)%3)+offset]):
		# WIN!
		goodbye(m)
		return True

	# Check diagonals...only applies if new position is an even number
	if (n%2 == 0):
		# Check first diagonal
		if ((n == 0) or (n == 4) or (n == 8)):
			if (board[0] == board[4] == board[8]):
				# WIN!
				goodbye(m)
				return True

		# Check second diagonal
		if ((n == 2) or (n == 4) or (n == 6)):
			if (board[2] == board[4] == board[6]):
				# WIN!
				goodbye(m)
				return True

	# CHECK FOR FULL BOARD (draw):
	for i in range(0,9):
		# If empty space found, board is NOT full
		if (board[i] != 0) and (board[i] != 1):
			return False
	
	# If it gets to this point, board is full with no victor
	client_list[0].sendall('\nDRAW!')
	client_list[1].sendall('\nDRAW!')
	# Also send final boards to both players
	sendBoards()
	return True

###### DONE DECLARING LOCAL FUNCTIONS


# Initial board setup
board = []
for i in range(0,9):
	board.append(' ')

# Create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associate the socket with the server address (which is localhost)
s.bind((TCP_IP, PORT))

# Put socket into server mode with listen, max of 2 connections in queue 
s.listen(2)
print 'Waiting for connections...'
while True:
	conn, clientAddr = s.accept()
	print 'Player ', clients, ' connected by ', clientAddr
	
	conn.sendall('YOU ARE PLAYER '+str(clients))

	# Append new socket object (conn) to list
	client_list.append(conn)
	clients += 1

	# Break when we have 2 players
	if clients == 2:
		break


# MAIN LOOP

currentPlayer = 0

while True:

	# Send both players the current board
	sendBoards()

	# Tell the current player that it's their turn
	client_list[currentPlayer].sendall('Your move')
	print 'Waiting on player', currentPlayer, '...\n'
	if (currentPlayer==0): client_list[1].sendall('Not your move yet...')
	if (currentPlayer==1): client_list[0].sendall('Not your move yet...')

	# Receive data from player
	move = client_list[currentPlayer].recv(BUFFER)
	print 'Player', currentPlayer, 'sent', move, '\n'

	# List indices must be integers
	move = int(move)

	# Update master board after checking for valid input
	if (move>8):
		client_list[currentPlayer].sendall('Please enter valid input (0-8) next time!')
		print 'Invalid input by player ', currentPlayer
	elif (board[move] == 0) or (board[move] == 1):
		client_list[currentPlayer].sendall('This spot is taken!')
		print 'Player ', currentPlayer, ' played on an occupied spot.'
	elif (board[move] != 0) and (board[move] != 1) and (move<9): 
		board[move] = currentPlayer

	# Check if the game is over, either victory or draw
	if (move<9) and checkGame(move, currentPlayer):

		# Close client sockets
		print 'Closing socket 0...'
		client_list[0].close()
		print 'Closing socket 1...'
		client_list[1].close()

		# Break out of main loop
		break

	# Change currentPlayer and proceed
	if currentPlayer == 0: currentPlayer = 1
	elif currentPlayer == 1: currentPlayer = 0


## END OF FILE