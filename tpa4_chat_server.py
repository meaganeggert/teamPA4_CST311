#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 5"
__credits__ = [
        "Meagan Eggert",
        "Maria Imperatrice",
        "Brandon Hoppens",
        "Ryan Matsuo"
]


import socket as s
import time
import threading
import select
import sys
import ssl

# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# to be changed when moved to /etc/ssl/demoCA/private
# and /etc/ssl/demoCA/newcerts
ssl_key_file = "/home/mininet/tpa4.chat.test-key.pem"
ssl_cert_file = "/home/mininet/tpa4.chat.test-cert.pem"
client_cert_file = "/etc/ssl/demoCA/cacert.pem"
# password = "CST311"

server_name = '10.0.2.2'
server_port = 12000
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(ssl_cert_file, ssl_key_file)
# context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context.verify_mode = ssl.CERT_REQUIRED
# context.load_cert_chain(certfile=ssl_cert_file, keyfile=ssl_key_file)
# context.load_verify_locations(cafile=client_cert_file)

client_used = {}
connected_clients = {}

inputs = []
outputs = []


def connection_handler(connection_socket, address):

    message = "You are connected to the server. "
    # client_count = len(connected_clients)

    # Send welcoming message to the client
    if connection_socket == connected_clients.get("Client X"):
        message += "Welcome, Client X! Type a message and press 'enter' to send."
        connected_clients.get("Client X").send(message.encode())
    if connection_socket == connected_clients.get("Client Y"):
        message += "Welcome, Client Y! Type a message and press 'enter' to send."
        connected_clients.get("Client Y").send(message.encode())
    if connection_socket == connected_clients.get("Client Z"):
        message += "Welcome, Client Z! Type a message and press 'enter' to send."
        connected_clients.get("Client Z").send(message.encode())
    # else:
    #     if client_count == 2:
    #     # Client Y
    #         message += "Welcome, Client Y! Type a message and press 'enter' to send."
    #         connected_clients.get("Client Y").send(message.encode())
    #     elif client_count == 3:
    #         # Client Z
    #         message += "Welcome, Client Z! Type a message and press 'enter' to send."
    #         connected_clients.get("Client Z").send(message.encode())
 
    server_active = True
    while server_active:
        try:
            input_ready, output_ready, err = select.select(inputs, outputs, [])
        except:
            print("Meagan broke something in the server code")
            # allow a little room for error so don't break
            # break

        # Meg - For each "ready" possible input, i.e. Client X or Client Y
        for input in input_ready:
            try:
                # If there's a message, receive it
                message_encoded = connection_socket.recv(1024)
                if not message_encoded:
                    break
                message = message_encoded.decode()
                response = message.lower()
                # If the message is 'bye'
                if response == "bye":
                    # Exit message received from Client X, prep to close the connection for Client X
                    if (connection_socket == connected_clients.get("Client X")):
                        response = "Client X has left the chat"
                        print(response)
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client X":
                                client_socket.send(response.encode())
                        server_active = False # boolean to close outer loop
                        client_used[0] = False # boolean to indicate Client X is free
                    # Exit message received from Client Y, prep to close the connection for Client Y
                    if (connection_socket == connected_clients.get("Client Y")):
                        response = "Client Y has left the chat"
                        print(response)
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client Y":
                                client_socket.send(response.encode())
                        server_active = False # boolean to close outer loop
                        client_used[1] = False # boolean to indicate Client Y is free
                    # Exit message received from Client Z, prep to close the connection for Client Z
                    if (connection_socket == connected_clients.get("Client Z")):
                        response = "Client Z has left the chat"
                        print(response)
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client Z":
                                client_socket.send(response.encode())
                        server_active = False # boolean to close outer loop
                        client_used[2] = False # boolean to indicate Client Z is free
                    break


                # Brandon - send message to other client (this version only works with hard coded numbers (two clients))
                # Meg - Adjusted to use usernames
                else:
                    log.info("Received query test \"" + str(message) + "\"")
#                   time.sleep(2)
                    # Message received from Client X
                    if connection_socket == connected_clients.get("Client X"):
                        response = "Client X: " + response
                        # Send message to Client Y and Client Z
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client X":
                                client_socket.send(response.encode())
                    # Message received from Client Y
                    elif connection_socket == connected_clients.get("Client Y"):
                        response = "Client Y: " + response
                        # Send message to Client X and Client Z
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client Y":
                                client_socket.send(response.encode())
                    # Message received from Client Z
                    elif connection_socket == connected_clients.get("Client Z"):
                        response = "Client Z: " + response
                        # Send message to Client X and Client Y
                        for client_name, client_socket in connected_clients.items():
                            if client_name != "Client Z":
                                client_socket.send(response.encode())
            except:
                print("There is an error")
            
            # If a client exited, break the loop
            if server_active == False:
                break
        if server_active == False:
            break

    # Close client socket
    # Only remove socket from connected_clients if connected_clients contains a socket and we want it to be removed
    if connected_clients.get("Client X") != None and client_used[0] == False:
        # Remove if connection is from Client X
        if connection_socket == connected_clients["Client X"]:
            del connected_clients["Client X"]
            inputs.remove(connection_socket)
            outputs.remove(connection_socket)
    if connected_clients.get("Client Y") != None and client_used[1] == False:
        # Remove if connection is from Client Y
        if connection_socket == connected_clients["Client Y"]:
            del connected_clients["Client Y"]
            inputs.remove(connection_socket)
            outputs.remove(connection_socket)
    if connected_clients.get("Client Z") != None and client_used[2] == False:
        # Remove if connection is from Client Z
        if connection_socket == connected_clients["Client Z"]:
            del connected_clients["Client Z"]
            inputs.remove(connection_socket)
            outputs.remove(connection_socket)
    
    
    connection_socket.close()
    # for key, value in connected_clients.items():
        # print(key, value)


def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign port number to socket, and bind to chosen port
  server_socket.bind((server_name,server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(3)

  # wrap socket with tls context
  s_sock = context.wrap_socket(server_socket, server_side=True)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))

  # Brandon - Initiate client_used to be used with update_socket and connection_handler.
  client_used[0] = False # Client X
  client_used[1] = False # Client Y
  client_used[2] = False # Client Z
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = s_sock.accept()

      # Meg - Keep track of connected_clients with username:
      # Brandon - updates based on client_used dictionary
    #   if len(connected_clients) == 0:
    #       connected_clients["Client X"] = connection_socket
    #   else:
    #       connected_clients["Client Y"] = connection_socket
      if client_used.get(0) == False:
        client_used[0] = True
        connected_clients["Client X"] = connection_socket
      elif client_used.get(1) == False:
        client_used[1] = True
        connected_clients["Client Y"] = connection_socket
      elif client_used.get(2) == False:
        client_used[2] = True
        connected_clients["Client Z"] = connection_socket

      inputs.append(connection_socket)
      outputs.append(connection_socket)
      # for key, value in connected_clients.items():
          # print(key, value)


      # Meg - Start a new thread
      # Brandon - made temporary change to second args (originally "address")
      client_thread = threading.Thread(target=connection_handler, args=(connection_socket, address))
      client_thread.start()
      log.info("Connected to client at " + str(address))

  finally:
    s_sock.close()
    server_socket.close()


if __name__ == "__main__":
  main()