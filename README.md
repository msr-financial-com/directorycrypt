# Dirctorcrypt

### Summary
The purpose of this repo is to decrypt or encrypt given files or create a new config for a new server

### Usage
Encrypt a file named test.key:


`$ python3 main.py -e -f test.key -k dwUh6-c-j3nW5Psmj9KOW7BIERCCW_dJmpAQ30vd1WI=`

Decrypt a file named test.key:


`$ python3 main.py -d -f test.key -k dwUh6-c-j3nW5Psmj9KOW7BIERCCW_dJmpAQ30vd1WI=`

Encrypt all files named .key (This will search recursiv through all directorys under the current directory)


`$ python3 main.py -e -f "*.key" -k dwUh6-c-j3nW5Psmj9KOW7BIERCCW_dJmpAQ30vd1WI=`

Create a new config for new server named test:


`$ python3 main.py -c test`

### Help
  ```
$ python3 main.py -h
usage: main.py [-h] [-f FILENAME] [-k KEY] [-d] [-e] [-c CREATE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        This will will be encrypted/decrypted / USE DOUBLEQUOTE WHEN USING REGEX
  -k KEY, --key KEY     The key to encrypt/decrypt the files
  -d, --decrypt         Decrypt file and write to it
  -e, --encrypt         Encrypt file and write to it
  -c CREATE, --create CREATE
                        With given option create directory and config for the host, needs a string
```
