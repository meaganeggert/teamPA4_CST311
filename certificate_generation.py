
import subprocess

def addIPs():
    pass

def generateKey(chat_name, challenge_password):
    subprocess.run("sudo openssl genrsa -out " + chat_name + "-key.pem 2048\n", shell=True)
    # not sure how to automatically pass in the following questions for the private key generation.
    # pass

def generateCSR(chat_name):
    # The passphrase here should be what you set it to in lab6a
    subprocess.run("sudo openssl req -nodes -new -config /etc/ssl/openssl.cnf -key " + chat_name + "-key.pem -out " + chat_name + ".csr", shell=True)
    # pass

def generateCert(chat_name):
    subprocess.run("sudo openssl x509 -req -days 365 -in " + chat_name + ".csr -CA /etc/ssl/demoCA/cacert.pem -CAkey /etc/ssl/demoCA/private/cakey.pem -CAcreateserial -out " + chat_name + "-cert.pem", shell=True)
    # pass


if __name__ == '__main__':
    # Establish common name for chat server and write to file
    common_name = open('common_name.txt', 'w')
    chat_name = input("Enter common name for your chat server: ")
    common_name.write(chat_name + '\n')
    common_name.close()

    challenge_password = input("Enter a challenge password for the server private key: ")

    # Add IP addresses to /etc/hosts
    # addIPs()

    # # Generate private key
    print("generating key")
    generateKey(chat_name, challenge_password)

    # # Generate CSRs
    print("generating csr")
    generateCSR(chat_name)

    # # Generate certificate from CSRs
    print("generating cert")
    generateCert(chat_name)

    print('\nThe key that was generated\n')
    subprocess.run("sudo openssl x509 -text -noout -in " + chat_name + "-cert.pem", shell=True)
