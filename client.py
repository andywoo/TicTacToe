# client.py
# Tic-Tac-Toe by Andy Woo
#
# Last Updated: 12/02/2013

#!C:\python27

import socket
import sys
import time
import string

# Take input parameters for PORT and IP
PORT = int(sys.argv[2])
IP = sys.argv[1]
BUFFER = 1024


# Create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Connecting...'

# Connect to the IP and PORT given in user parameters
s.connect((IP, PORT))

print 'Connected!'

# Main loop
while True:

	# Print all received data
	data = s.recv(BUFFER)
	print data, '\n'

	if (data == 'Your move'):
		move = raw_input("Make a move (enter 0-8): ")
		print 'You selected position ', move
		s.sendall(move)

	if ((data=='\nYOU WIN!') or (data=='\nYOU LOSE!') or (data=='\nDRAW!')):

		# Show final board
		final = s.recv(BUFFER)
		print final, '\n'

		print 'Closing socket...'
		s.close()
		break


## END OF FILE