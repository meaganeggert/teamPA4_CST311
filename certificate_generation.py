
import subprocess

# This is where the ip-common_name translations will be added to /etc/hosts file
def addIPs():
    common_name_file = open('common_name.txt', 'r')
    common_name = common_name_file.read().strip()
    common_name_file.close()
    
    hosts_file = open('/etc/hosts', 'r')
    host_list = hosts_file.read()
    hosts_file.close()

    server_IP_to_common_name = "10.0.2.2\t" + common_name

    # if ip-common_name not already in /etc/hosts, then add all ip-common_name
    # otherwise skip
    if host_list.find(server_IP_to_common_name) == -1:
        host_file = open("/etc/hosts", "a")
        ip_file = open("ip_addresses.txt", "r")

        host_file.write("\n")
        for line in ip_file:
            mapping = line.split(":")
            host_file.write(mapping[1].strip() + "\t" + mapping[0].strip() + "\n")
        host_file.write(server_IP_to_common_name + "\n")

        host_file.close()
        ip_file.close()
    else:
        print("IP/Common Name connection previously established.")

def generateKey(chat_name, challenge_password):
    # This will generate private key, will be created in working directory
    subprocess.run("sudo openssl genrsa -out " + chat_name + "-key.pem 2048\n", shell=True)

def generateCSR(chat_name):
    # The passphrase here should be what you set it to in lab6a
    # This will generate the certificate signing request non-interactively, will be created in working directory
    subprocess.run("openssl req -nodes -new -config /etc/ssl/openssl.cnf -key " + chat_name + "-key.pem -out " + chat_name + ".csr -subj \"/C=US/ST=California/L=Seaside/O=CST311/CN=" + chat_name + "\"", shell=True)

def generateCert(chat_name):
    # This will generate the certificate, will be created in working directory
    subprocess.run("sudo openssl x509 -req -days 365 -in " + chat_name + ".csr -CA /etc/ssl/demoCA/cacert.pem -CAkey /etc/ssl/demoCA/private/cakey.pem -CAcreateserial -out " + chat_name + "-cert.pem", shell=True)


if __name__ == '__main__':
    # Establish common name for chat server and write to file
    common_name = open('common_name.txt', 'w')
    chat_name = input("Enter common name for your chat server: ")
    common_name.write(chat_name + '\n')
    common_name.close()

    challenge_password = input("Enter a challenge password for the server private key: ")

    # Add IP addresses to /etc/hosts
    addIPs()

    # Generate private key
    print("Generating key..")
    generateKey(chat_name, challenge_password)

    # Generate CSRs
    print("Generating CSR..")
    generateCSR(chat_name)

    # Generate certificate from CSRs
    print("Generating Certificate..")
    generateCert(chat_name)

    # Print certificate
    print('\nPrinting the decrypted certificate\n')
    subprocess.run("sudo openssl x509 -text -noout -in " + chat_name + "-cert.pem", shell=True)
