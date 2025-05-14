# Вариант 2(14) алгритм IDEA 
from tkinter import *
from os import listdir
from os.path import isfile, join

import ctypes
salt = b'aa'

ctypes.cdll.LoadLibrary("./4/libsha256.so")
_ciph = ctypes.CDLL('./4/libsha256.so')
_ciph.sha256.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.c_int64, ctypes.POINTER(ctypes.c_uint32))

def hash():
    hash = [0 for i in range(8)]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    cinput = (ctypes.c_char * len(inputText))()
    for i, x in enumerate(inputText):
        cinput[i] = x
    chash = (ctypes.c_uint32 * 8)()
    _ciph.sha256(cinput, len(inputText), chash)
    output = "hash: "
    for i in range(8):
        output = output + hex(chash[i])[2:]
    with open(mypath + "hash", 'wb') as file:
        file.write(chash)
    labelKey.config(text=output)


if __name__ == "__main__":
    mypath = "./4/"
    root = Tk()

    btnCiph = Button(text="Хешировать", command=hash)
    btnCiph.grid(row=1, column=1, padx=5, pady=5)

    #btnDeciph = Button(text="Расшифровать", command=deciph)
    #btnDeciph.grid(row=1, column=2, padx=5, pady=5)

    labelKey = Label(text="hash:")
    labelKey.grid(row=2, column=1,columnspan=2, padx=5, pady=5, sticky=W)

    labelList = Label(text="Список файлов:")
    labelList.grid(row=3, column=1, padx=5, pady=5, sticky=NE)

    #entryKey = Entry()
    #entryKey.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filesList_var = Variable(value=filesList)

    listboxFiles = Listbox(listvariable=filesList_var, selectmode=SINGLE)
    listboxFiles.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    root.mainloop()