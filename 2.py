# Вариант 2(14) алгритм IDEA 
from tkinter import *
from os import listdir
from os.path import isfile, join
from os import urandom

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import ctypes
salt = b'aa'

_ciph = ctypes.CDLL('./2/libidea.so')
_ciph.ciph.argtypes = (ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16), ctypes.c_int64)
_ciph.deciph.argtypes = (ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16), ctypes.c_int64)

def ciph():
    password = entryKey.get()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=480000,
    )
    keys = kdf.derive(bytes(password, encoding="utf-8"))
    key = [keys[i*2]*0x100 + keys[i*2+1] for i in range(8)]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    addition = (8 - len(inputText) % 8) % 8
    if addition != 0:
        for i in range(addition):
            inputText.append(addition)
    cinput = (ctypes.c_uint16 * (len(inputText) // 2))()
    for i in range(len(inputText)//2):
        cinput[i] = inputText[i*2]*0x100 + inputText[i*2 + 1]
    ckey = (ctypes.c_uint16 * (len(key)))()
    for i in range(8):
        ckey[i] = key[i]
    _ciph.ciph(cinput, ckey, len(inputText))
    for i in range(len(inputText)//2):
        inputText[i*2] = cinput[i] // 0x100
        inputText[i*2 + 1] = cinput[i] % 0x100
    with open(mypath + "ciph", 'wb') as file:
        file.write(bytes(inputText))

def deciph():
    password = entryKey.get()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=480000,
    )
    
    keys = kdf.derive(bytes(password, encoding="utf-8"))
    key = [keys[i*2]*0x100 + keys[i*2+1] for i in range(8)]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    cinput = (ctypes.c_uint16 * (len(inputText) // 2))()
    for i in range(len(inputText)//2):
        cinput[i] = inputText[i*2]*0x100 + inputText[i*2 + 1]
    ckey = (ctypes.c_uint16 * (len(key)))()
    for i in range(8):
        ckey[i] = key[i]
    _ciph.deciph(cinput, ckey, len(inputText))
    for i in range(len(inputText)//2):
        inputText[i*2] = cinput[i] // 0x100
        inputText[i*2 + 1] = cinput[i] % 0x100
    if inputText[-1] in range(1,8):
        addon = inputText[-1]
        for i in range(addon):
            if inputText[-(i+1)] !=addon:
                break
        else:
            for i in range(addon):
                inputText.pop()
    with open(mypath + "deciph", 'wb') as file:
        file.write(bytes(inputText))

if __name__ == "__main__":
    mypath = "./2/"
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