from cryptography.fernet import Fernet
import argparse
import subprocess
import glob
import os

#def create_key():
#    """
#    Generates a key and save it into a file
#    """
#    key = Fernet.generate_key()
#    with open("key.key", "wb") as key_file:
#        key_file.write(key)

parser = argparse.ArgumentParser()

#Command line option to declare which file
parser.add_argument('-f', '--filename', nargs='+',
                    help='This will will be encrypted/decrypted')

#Command line option to decrypt
parser.add_argument('-d', '--decrypt', default=False, action='store_true',
                    help='Decrypt file and write to it')

#Command line option to encrypt
parser.add_argument('-e', '--encrypt', default=False, action='store_true',
                    help='Encrypt file and write to it')

#Command line option to create a new conf and directory for new given host
parser.add_argument('-c', '--create',
                    help='With given option create directory and config for the host, needs a string')

#Initialize the options
args = parser.parse_args()

#Find alle key files
if args.filename:
    files=[]
    for file in args.filename:
        files.extend(glob.glob("**/" + file, recursive=True))

def load_key():
    """
    Gets the key from the command that was executed
    """
    #Directory of the key to encrypt/decrypt
    getkey = "cat key.key2"
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
            #Read the decrypted data
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
        #Read all file data
        with open(file, "rb") as fileread:
            #Read the encrypted data
            file_data = fileread.read()
    
        #Decrypt data
        decrypted_data = cryptkey.decrypt(file_data)

        #Write the decrypted file
        with open(file, "wb") as filewrite:
            filewrite.write(decrypted_data)

#Encrypt
if args.encrypt == True and args.decrypt == False:
    key = load_key()
    encrypt(key)

#Decrypt
if args.decrypt == True and args.encrypt == False:
    key = load_key()
    decrypt(key)

#If create and hostname is there do this
if args.create:
    if os.path.exists(args.create) == False:
        #If directory does not exists create it
        os.mkdir(args.create)
    #Create config file for the new Host
    conf = open(args.create + "/" + args.create + ".conf", "w")
    subprocess.call(["sed", "-e", f's/@HOSTNAME@/{args.create}/g', "template.conf"], stdout=conf)