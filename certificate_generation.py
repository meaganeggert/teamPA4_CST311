
import subprocess

def addIPs():
    pass

def generateKey():
    pass

def generateCSR():
    pass

def generateCert():
    pass


if __name__ == '__main__':
    # Establish common name for chat server and write to file
    common_name = open('common_name.txt', 'w')
    
    chat_name = input("Enter common name for your chat server: ")
    common_name.write(chat_name)

    common_name.close()

    # Add IP addresses to /etc/hosts
    addIPs()

    # Generate private key
    generateKey()

    # Generate CSRs
    generateCSR()

    # Generate certificate from CSRs
    generateCert()


