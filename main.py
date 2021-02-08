from cryptography.fernet import Fernet
from optparse import OptionParser
import subprocess
import glob

#def create_key():
#    """
#    Generates a key and save it into a file
#    """
#    key = Fernet.generate_key()
#    with open("key.key", "wb") as key_file:
#        key_file.write(key)

parser = OptionParser()

#Command line option to encrypt data
parser.add_option("-e", "--encrypt", action="store_true", dest="encrypt", default=False,
                  help="encrypt the data and write to file", metavar="ENCRYPT")

#Command line option to decrypt data
parser.add_option("-d", "--decrypt", action="store_true", dest="decrypt", default=False,
                  help="decrypt the data and write to file")

#Initialize the options
(options, args) = parser.parse_args()

#Find alle key files
files = glob.glob("**/*.key", recursive=True)

def load_key():
    """
    Gets the key from the command that was executed
    """
    #Directory of the key to encrypt/decrypt
    getkey = "cat /home/msr/test/key.key"
    #Call the command
    process = subprocess.Popen(getkey.split(), stdout=subprocess.PIPE)
    #Get the output
    output = process.stdout.read()

    return output

def encrypt(key):
    """
    Given a key (bytes), it encrypts the file
    """
    #Initialize encryption key
    cryptkey = Fernet(key)

    #Open alle files named .key
    for file in files:
        #Read all file data
        with open(file, "rb") as fileread:
            file_data = fileread.read()
        #Encrypted data
        encrypted_data = cryptkey.encrypt(file_data)

        #Write the encrypted file
        with open(file, "wb") as filewrite:
            filewrite.write(encrypted_data)

def decrypt(key):
    """
    Given a key (bytes), it decrypts the file
    """
    #Initialize decryption key
    cryptkey = Fernet(key)

    #Open alle files named .key
    for file in files:
        with open(file, "rb") as fileread:
            #Read the encrypted data
            file_data = fileread.read()
    
        #Decrypt data
        decrypted_data = cryptkey.decrypt(file_data)

        #Write the decrypted file
        with open(file, "wb") as filewrite:
            filewrite.write(decrypted_data)

#Encrypt
if options.encrypt == True and options.decrypt == False:
    key = load_key()
    encrypt(key)

#Decrypt
if options.decrypt == True and options.encrypt == False:
    key = load_key()
    decrypt(key)