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

#Command line option to decrypt data
#parser.add_option("-k", "--key", dest="key",
#                  help="Key that is required to encrypt/decrypt the file")

#Initialize the options
(options, args) = parser.parse_args()

#Find alle key files
files = glob.glob("**/*.key", recursive=True)

def load_key():
    """
    Gets the key from the current directory named key.key
    """
    getkey = "cat /home/msr/test/key.key"
    process = subprocess.Popen(getkey.split(), stdout=subprocess.PIPE)
    output = process.stdout.read()
    return output

def encrypt(key):
    """
    Given a key (bytes), it encrypts the file
    """
    f = Fernet(key)
    for file in files:
        #read all file data
        with open(file, "rb") as fileread:
            file_data = fileread.read()
        #encrypted data
        encrypted_data = f.encrypt(file_data)

        #write the encrypted file
        with open(file, "wb") as filewrite:
            filewrite.write(encrypted_data)

def decrypt(key):
    """
    Given a key (bytes), it decrypts the file
    """
    f = Fernet(key)
    for file in files:
        with open(file, "rb") as fileread:
            #read the encrypted data
            file_data = fileread.read()
    
        #decrypt data
        decrypted_data = f.decrypt(file_data)

        #write the decrypted file
        with open(file, "wb") as filewrite:
            filewrite.write(decrypted_data)

#Encrypt
if options.encrypt == True and options.decrypt == False:
    key = load_key()
    print(key)
    encrypt(key)

#Decrypt
if options.decrypt == True and options.encrypt == False:
    key = load_key()
    decrypt(key)