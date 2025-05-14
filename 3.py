# Вариант 2(14) алгритм IDEA 
from tkinter import *
from os import listdir
from os.path import isfile, join
from os import urandom

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ctypes
salt = b'aa'

_ciph = ctypes.CDLL('./3/libstreamciph.so')
_ciph.ciph.argtypes = (ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.c_int64)
#_ciph.deciph.argtypes = (ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_uint8), ctypes.c_int64)

def ciph():
    password = entryKey.get()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=30,
        salt=salt,
        iterations=480000,
    )
    keys = kdf.derive(bytes(password, encoding="utf-8"))
    print(keys.hex())
    keys = list(keys)
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)

    a = 2**10
    oldFilebgn = inputText[:a]

    cinput = (ctypes.c_uint8 * len(inputText))()
    for i, x in enumerate(inputText):
        cinput[i] = x
    ckey = (ctypes.c_uint8 * (len(keys)))()
    for i, x in enumerate(keys):
        ckey[i] = x
    _ciph.ciph(cinput, ckey, len(inputText))
    for i, x in enumerate(cinput):
        inputText[i] = x

    with open(mypath + "ciph", 'wb') as file:
        file.write(bytes(inputText))
    if fileName[-4:] == ".bmp":
        with open(mypath + "ciph.bmp", 'wb') as file:
            file.write(bytes(oldFilebgn + inputText[a:]))

def deciph():
    password = entryKey.get()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=30,
        salt=salt,
        iterations=480000,
    )
    keys = kdf.derive(bytes(password, encoding="utf-8"))
    keys = list(keys)
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)

    a = 2**10
    oldFilebgn = inputText[:a]

    cinput = (ctypes.c_uint8 * len(inputText))()
    for i, x in enumerate(inputText):
        cinput[i] = x
    ckey = (ctypes.c_uint8 * (len(keys)))()
    for i, x in enumerate(keys):
        ckey[i] = x
    _ciph.ciph(cinput, ckey, len(inputText))
    for i, x in enumerate(cinput):
        inputText[i] = x

    with open(mypath + "deciph", 'wb') as file:
        file.write(bytes(inputText))
    if fileName[-4:] == ".bmp":
        with open(mypath + "deciph.bmp", 'wb') as file:
            file.write(bytes(oldFilebgn + inputText[a:]))

if __name__ == "__main__":
    mypath = "./3/"
    root = Tk()

    btnCiph = Button(text="Зашифровать", command=ciph)
    btnCiph.grid(row=1, column=1, padx=5, pady=5)

    btnDeciph = Button(text="Расшифровать", command=deciph)
    btnDeciph.grid(row=1, column=2, padx=5, pady=5)

    labelKey = Label(text="Ключ:")
    labelKey.grid(row=2, column=1, padx=5, pady=5, sticky=E)

    labelList = Label(text="Список файлов:")
    labelList.grid(row=3, column=1, padx=5, pady=5, sticky=NE)

    entryKey = Entry()
    entryKey.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filesList_var = Variable(value=filesList)

    listboxFiles = Listbox(listvariable=filesList_var, selectmode=SINGLE)
    listboxFiles.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    root.mainloop()