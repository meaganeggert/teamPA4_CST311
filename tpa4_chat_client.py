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
import ssl

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# grab the common name to be used for the address and tsl
common_name_file = open('common_name.txt', 'r')
common_name = common_name_file.read().strip()
common_name_file.close()

# Set global variables
server_name = common_name
server_port = 12000

# set client certificate using this location
client_cert_file = "/etc/ssl/demoCA/cacert.pem"
# set ssl context to TLS client using the client certificate
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(client_cert_file)

inputs = []
outputs = []

def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # wrap the socket with the ssl socket
    s_sock = context.wrap_socket(sock=client_socket, server_hostname=server_name)
    

    try:
        # Establish TCP connection
        s_sock.connect((server_name,server_port))
        
        # Meg - Add server_socket to both the list of potential inputs and potential outputs
        inputs.append(s_sock)
        outputs.append(s_sock)
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
    data = s_sock.recv(1024)
    welcome_message = data.decode()
    print(welcome_message)

    # Brandon - message instantiated outside while loop to allow for break on "bye",
    # otherwise we break on for loop, then restart due to while loop
    message = ""
    while True:
        # if the last message was bye, then stop sending/listening messages
        if message.lower() == "bye":
            break
        try:
            input_ready, output_ready, err = select.select([sys.stdin, s_sock], [s_sock], [])

            for i in input_ready:
                # listen for and print incoming messages from the server
                if i == s_sock:
                    data = s_sock.recv(1024)
                    message = data.decode()
                    print(message)

                # send message to server
                elif i == sys.stdin:
                    message = input()
                    try:
                        s_sock.send(message.encode())
                    except:
                        print("Error sending message")
                    if message.lower() == "bye":
                        break 
        except select.error as e:
            print("Error:", e)

    # Close socket
    s_sock.close()
    client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
