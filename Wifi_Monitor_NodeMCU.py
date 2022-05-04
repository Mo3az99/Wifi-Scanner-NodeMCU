import random

import serial
from tkinter import *
total_rows = 0
total_columns = 0
serialPort = serial.Serial(port="COM6", baudrate=115200,
                           bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
# create root window
root = Tk()
root.title('Wireless Project')
flag = 0

class Table:


    def __init__(self, root):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])
    def clear(self,root):
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, " ")


def read(number):
    number = int(number)
    lsst = [("SSID", "MAC", "RSSI (db)", "Channel","Hidden","Encryption")]
    for i in range(0,number):
        serialString = serialPort.readline().decode('utf-8')
        serialString = serialString.split(",")
        lsst.append(tuple(serialString))
    return lsst
def update():
    global t
    global total_rows
    global total_columns
    global lst
    global root
    global flag
    if flag == 1 :
        flag = 0
        root.destroy()
        root = Tk()
        root.title('Wireless Project')
    if (serialPort.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline().decode('utf-8')
        if (serialString[0:14] == "Networks found"):
            serialString = serialPort.readline().decode('utf-8')
            print("Networks Found", serialString)
            t.clear(root)
            lst = read(serialString)
            flag = 0
            total_rows = len(lst)
            total_columns = len(lst[0])
    root.title('Wireless Project')
    t = Table(root)

    root.after(1000, update)

update()
root.mainloop()

