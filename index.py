from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        print(s)
        s = s + b"\0" * (AES.block_size - len(s) % AES.block_size)
        print(s)
        return s

    def encrypt(self, message):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)
    
    def encrypt_file(self, file_name):
        with open(file_name, "rb") as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", "wb") as fo:
                fo.write(enc)
        os.remove(file_name)

    def decrypt(self, cipherText, key):
        iv = cipherText[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plainText = cipher.decrypt(cipherText[AES.block_size:])
        return plainText.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, "rb") as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], "wb") as fo:
            fo.write(dec)
        
        
    def getAllfile(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subDirList, fileList in os.walk(dir_path):
            for name in fileList:
                if name != 'learn.py' and name != 'data.txt.enc':
                    dirs.append(os.path.join(dirName, name))
        return dirs
    
    def encrypt_all_file(self):
        dirs = self.getAllfile()
        for file_name in dirs:
            self.encrypt_file(file_name)
            
    def decrypt_all_files(self):
        dirs = self.getAllfile()
        for file_name in dirs:
            self.decrypt_file(file_name)
key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F' \
      b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'

enc = Encryptor(key)
clear = lambda: os.system('clear')

if os.path.isfile("data.txt.enc"):
    while True:
        password = str(input('Enter the password: '))
        enc.decrypt_file("data.txt.enc")
        p = ""
        with open("data.txt") as f:  # Open as binary
            p = f.readlines()
            if p[0] == password:  # Compare first byte
                enc.encrypt_file("data.txt.enc")
                break
    while True:
        clear()
        choice = int(input(
         """
         1. Press 1 to encrypt file.
         2. Press 2 to decrypt file.
         3. Press 3 to encrypt all files in the directory.
         4. Press 4 to decrypt all files in the directory.
         5. Press 5 to exit
         """))
        clear()
        if choice == 1:
            enc.encrypt_file(str(input("Enter the name of the file to encrypt: ")))
        elif choice == 2:
            enc.decrypt_file(str(input("Enter the filename of the file to decrypt: ")))
        elif choice == 3:
            enc.encrypt_all_file()
        elif choice == 4:
            enc.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Please select a valid option!")

else:
    while True:
        clear()
        password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
        repassword = str(input("Confirm Password: "))
        if password == repassword:
            break
        else:
            print("Password mismatched")
    f = open("data.txt", "w+")
    f.write(password)
    f.close()
    enc.encrypt_file("data.txt")
    print("Please restart the program to complete the setup")
