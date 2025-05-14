# Вариант 4(14) ЭЦП ГОСТ Р 34.10-94
from tkinter import *
from os import listdir
from os.path import isfile, join
from time import time
import datetime
from random import randrange, seed


bitsize = 32

import ctypes

ctypes.cdll.LoadLibrary("./5/libprime.so")
_prime = ctypes.CDLL("./5/libprime.so")
_prime.getPrime.argtypes = [ctypes.c_uint64]
_prime.getPrime.restype = ctypes.c_uint64
_prime.isPrime.argtypes = [ctypes.c_uint64]



def genkey():
    seed(time())
    #fileName = filesList[listboxFiles.curselection()[0]]
    #with open(mypath + fileName, 'rb') as file:
    #    inputText = file.read()
    #inputText = list(inputText)
    p = _prime.getPrime(ctypes.c_uint64(randrange(2**(bitsize-1), 2**bitsize)))
    #q = _prime.getPrime(ctypes.c_uint64(randrange(int(2**(bitsize/2-1)), int(2**(bitsize/2)))))
    qmin = 2**(bitsize/2-1)
    q = _prime.getPrime(ctypes.c_uint64(int(2**(bitsize/2))))
    while (p-1)%q!=0 and q>qmin:
        q = _prime.getPrime(ctypes.c_uint64(q))
    while q<=qmin:
        p = _prime.getPrime(ctypes.c_uint64(p))
        q = _prime.getPrime(ctypes.c_uint64(int(2**(bitsize/2))))
        while (p-1)%q!=0 and q>qmin:
            q = _prime.getPrime(ctypes.c_uint64(q))
        
    a = 2
    while not(pow(a,q,p) == 1):
        a+=1
        #print(a)
    x = randrange(1, q)
    y = a**x % p
    #output = "ЭЦП верна?: "

    with open(mypath + "kyes " + 
              datetime.datetime.today().strftime("%S-%M-%H %d.%m.%y")
, 'w') as file:
        file.write(f"p {p}\nq {q}\na {a}\n\ny {y}\n\nx {x}")
    filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filesList_var = Variable(value=filesList)
    listboxFiles.config(listvariable=filesList_var)
    #label.config(text=output)

def makeSig():
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    h = hash(m)
    return [h, r, s]

def checkDS():
    DS = 0



if __name__ == "__main__":
    mypath = "./5/"
    root = Tk()

    btnCiph = Button(text="Сделать ЭЦП", command=genkey)
    btnCiph.grid(row=1, column=1, padx=5, pady=5)

    btnDeciph = Button(text="Проверить ЭЦП", command=checkDS)
    btnDeciph.grid(row=1, column=2, padx=5, pady=5)

    label = Label(text="vali?:")
    label.grid(row=2, column=1,columnspan=2, padx=5, pady=5, sticky=W)

    labelList = Label(text="Список файлов:")
    labelList.grid(row=3, column=1, padx=5, pady=5, sticky=NE)

    entryKey = Entry()
    entryKey.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    filesList = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    filesList_var = Variable(value=filesList)

    listboxFiles = Listbox(listvariable=filesList_var, selectmode=SINGLE)
    listboxFiles.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky=W)

    root.mainloop()