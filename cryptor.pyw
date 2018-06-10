import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import Label
import sys
import time
from threading import Thread
import webbrowser
import tkinter as tk

Kinter = tk()
Kinter.title("Kinter Cryptor")

def encrypt(key, filename):
    chunksize = 64*1024
    outputFile = "(encrypted)"+filename
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
    chunksize = 64*1024
    outputFile = filename[11:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def Main():
    string = StringVar()
    string.set("Voulez-vous (E)ncrypter ou (D)crypter ?: ")
    entree = Entry(Kinter, textvariable=string, width=30, bg="black", fg="white")
    entree.pack(side=TOP)

    if string == "E":
        filename = input("Fichier à Encrypter: ")
        password = input("Clé de cryptage: ")
        encrypt(getKey(password), filename)
        print("Fait.")
    elif string == 'D':
        filename = input("Fichier à Décrypter: ")
        password = input("Clé de décryptage: ")
        decrypt(getKey(password), filename)
        print("Fait.")
    else:
        print("Aucune option séléctionée, fermeture...")

if __name__ == '__main__':
    Main()

Kinter.mainloop()
