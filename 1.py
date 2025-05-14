# Вариант 2(14) Метод Виженера
# TODO похорошему после создания файла добавить бы его в список сразу
# TODO что-то сделать с ошибкой если не выбран файл

from tkinter import *
from os import listdir
from os.path import isfile, join
import csv

mypath = "./"

def ciph():
    key = [ord(i) for i in entryKey.get()]
    if not key:
        key = [0]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    for i in range(len(inputText)):
        inputText[i] = (inputText[i] + key[i % len(key)]) % 0xFF
    with open(mypath + "ciph", 'wb') as file:
        file.write(bytes(inputText))

def deciph():
    key = [ord(i) for i in entryKey.get()]
    if not key:
        key = [0]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    for i in range(len(inputText)):
        inputText[i] = (inputText[i] - key[i % len(key)]) % 0xFF
    with open(mypath + "deciph", 'wb') as file:
        file.write(bytes(inputText))

def freq():
    freqList = [0 for i in range(256)]
    fileName = filesList[listboxFiles.curselection()[0]]
    with open(mypath + fileName, 'rb') as file:
        inputText = file.read()
    inputText = list(inputText)
    for char in inputText:
        freqList[char] += 1
    
    with open(mypath + "freq.csv", 'w') as file:
        writer =  csv.writer(file, delimiter=';')
        for i, x in enumerate(freqList):
            writer.writerow([i, x * 100 / len(inputText)])


root = Tk()

btnCiph = Button(text="Зашифровать", command=ciph)
btnCiph.grid(row=1, column=1, padx=5, pady=5)

btnDeciph = Button(text="Расшифровать", command=deciph)
btnDeciph.grid(row=1, column=2, padx=5, pady=5)

btnDeciph = Button(text="Анализ", command=freq)
btnDeciph.grid(row=1, column=3, padx=5, pady=5)

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