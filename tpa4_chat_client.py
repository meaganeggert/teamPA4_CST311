#!env python

"""Chat client for CST311 Programming Assignment 3"""
__author__ = "Team 5"
__credits__ = [
        "Meagan Eggert",
        "Maria Imperatrice",
        "Brandon Hoppens",
        "Ryan Matsuo"
        ]

# Import statements
import socket as s

import sys
import select

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.2.2'
server_port = 12000

inputs = []
outputs = []

def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    

    try:
        # Establish TCP connection
        client_socket.connect((server_name,server_port))
        
        # Meg - Add server_socket to both the list of potential inputs and potential outputs
        inputs.append(client_socket)
        outputs.append(client_socket)
    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
        exit(8)

    # Meg - Receive Client welcome message from server
    data = client_socket.recv(1024)
    welcome_message = data.decode()
    print(welcome_message)

    # Brandon - message outside while loop to allow for break on "bye",
    # otherwise we break on for loop, then restart due to while loop
    message = ""
    while True:
        if message.lower() == "bye":
            break
        try:
            input_ready, output_ready, err = select.select([sys.stdin, client_socket], [client_socket], [])
    
            for i in input_ready:
                if i == client_socket:
                    data = client_socket.recv(1024)
                    message = data.decode()
                    print(message)

                elif i == sys.stdin:
                    message = input()
                    try:
                        client_socket.send(message.encode())
                    except:
                        print("Error sending message")
                    if message.lower() == "bye":
                        break 
        except select.error as e:
            print("Error:", e)

    # Close socket
    client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
