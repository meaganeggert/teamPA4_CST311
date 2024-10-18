
import subprocess

common_name = open('common_name.txt', 'w')

chat_name = input("Enter common name for your chat server: ")
common_name.write(chat_name)

# password = input("Enter a challenge password for the server private key: ")

common_name.close()
