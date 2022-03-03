import os
import glob
import argparse
import subprocess
import cryptography
from cryptography.fernet import Fernet
from pathlib import Path

# def create_key():
#    """
#    Generates a key and save it into a file
#    """
#    key = Fernet.generate_key()
#    with open("key.key", "wb") as key_file:
#        key_file.write(key)

parser = argparse.ArgumentParser()

# Command line option to declare which file
parser.add_argument("-f", "--filename", help="This will will be encrypted/decrypted / USE DOUBLEQUOTE WHEN USING REGEX")

# Command line option to declare key
parser.add_argument("-k", "--key", help="The key to encrypt/decrypt the files")

# Command line option to decrypt
parser.add_argument("-d", "--decrypt", default=False, action="store_true", help="Decrypt file and write to it")

# Command line option to encrypt
parser.add_argument("-e", "--encrypt", default=False, action="store_true", help="Encrypt file and write to it")

# Command line option to create a new conf and directory for new given host
parser.add_argument("-c", "--create", help="With given option create directory and config for the host, needs a string")

# Initialize the options
args = parser.parse_args()

# Find all files with given filename argument
if args.filename:
    files = []
    for path in Path("./CERTS/").rglob(args.filename):
        files.append(path.resolve())


def encrypt(key):
    """
    Given a key (bytes), it encrypts the file
    """
    # Initialize encryption key
    cryptkey = Fernet(key)
    # Open all found files
    for file in files:
        # Read all file data
        isDirectory = os.path.isdir(file)
        if not isDirectory:
            with open(file, "rb") as fileread:
                # Read the decrypted data
                file_data = fileread.read()

            # Encrypted data
            encrypted_data = cryptkey.encrypt(file_data)

            # Write the encrypted file
            with open(file, "wb") as filewrite:
                filewrite.write(encrypted_data)

            print("Successfully encrypted " + str(file))


def decrypt(key):
    """
    Given a key (bytes), it decrypts the file
    """
    # Initialize decryption key
    cryptkey = Fernet(key)

    # Open all found files
    for file in files:
        isDirectory = os.path.isdir(file)
        if not isDirectory:
            # Read all file data
            with open(file, "rb") as fileread:
                # Read the encrypted data
                file_data = fileread.read()

            # Decrypt data
            decrypted_data = cryptkey.decrypt(file_data)

            # Write the decrypted file
            with open(file, "wb") as filewrite:
                filewrite.write(decrypted_data)

            print("Successfully decrypted " + str(file))


# Encrypt
if args.encrypt and not args.decrypt:
    encrypt(args.key)


# Decrypt
if args.decrypt and not args.encrypt:
    try:
        decrypt(args.key)
    except (cryptography.fernet.InvalidToken, TypeError):
        print("Already decrypted or invalid Token")

# If create and hostname is there do this
if args.create:
    if not os.path.exists(args.create):
        # If directory does not exists create it
        os.mkdir(args.create)
    # Create config file for the new Host
    conf = open(args.create + "/" + args.create + ".conf", "w")
    subprocess.call(["sed", "-e", f"s/@HOSTNAME@/{args.create}/g", "template.conf"], stdout=conf)
