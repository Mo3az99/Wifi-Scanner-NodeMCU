import math
import random
import time
import plot as plot
import serial
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas import DataFrame
# Define Default Node
x= 175
y=400
r=15
# Define Table Rows
total_rows = 0
total_columns = 0
# Serial Port
serialPort = serial.Serial(port="COM6", baudrate=115200,bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
# create root window
root = Tk()
root.title('Wireless Project')
# Create Node window
win=Tk()
win.title("Wifi Scanner")
canvas=Canvas(win, width=350, height=500, background='#c0c0c0' )
canvas.grid(row=0, column=0)
# Global Flags
ssid = []
rssi = []
flag = 0
channels = [0]*12

def draw_line_origin():
    canvas.create_oval(x-r,y-r,x+r,y+r,fill='black')

def draw_line(x,y,r):
    canvas.create_oval(x-r,y-r,x+r,y+r,fill='red')


# plot function is created for
# plotting the graph in
# tkinter window
def plot():
    # the figure that will contain the plot
    fig = Figure(figsize=(5, 5),
                 dpi=100)
    # list of squares
    y = [i ** 2 for i in range(101)]
    # adding the subplot
    plot1 = fig.add_subplot(111)
    # plotting the graph
    plot1.plot(y)
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master=root)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   root)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

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
    global channels
    global ssid
    global rssi
    number = int(number)
    my_list = [("SSID", "MAC", "RSSI (db)", "Channel","Encryption","Distance (m)")]
    channels = [0] * 12
    dict2={}
    ssid.clear()
    rssi.clear()
    for i in range(0,number):
        serialString = serialPort.readline().decode('utf-8')
        serialString = serialString.split(",")
        ssid.append(serialString[0])
        rssi.append(serialString[2])
        key ='{}'.format(serialString[0])
        dict2[key]=serialString[2]
        del serialString[4]
        serialtuple = tuple(serialString)
        L1 = list(serialtuple)
        L1.append(str(get_distance(int(serialtuple[2]))))
        d = get_distance(int(serialtuple[2]))
        if get_distance(int(serialtuple[2])) > 0:
            draw_line(x, y - 50 - (d*5), r)
        serialtuple = tuple(L1)
        channels[int(serialtuple[3])-1] += 1
        my_list.append(serialtuple)
    sorted_dict2=sorted(dict2.items(), key=lambda x: x[1], reverse=False)
    j=0
    for i in sorted_dict2:
        ssid[j] = i[0]
        rssi[j] = 100+ int(i[1])
        j+=1
        # print(i[0], i[1])
    print(ssid)
    print(rssi)
    return my_list

def get_distance(rssi):
    # return math.pow(10, (20.5 - rssi) / (10 * 2))
    distance = math.pow(10, (-38 - rssi) / (10 * 2))
    if distance > 100 :
        return -1
    else:
        return distance
    # txpower = -35  # one meter away RSSI
    # if rssi == 0:
    #     return -1
    # else:
    #     ratio = rssi * 1.0 / txpower
    #     if ratio < 1:
    #         return ratio ** 10
    #     else:
    #         return 0.89976 * ratio ** 7.7095 + 0.111
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
            canvas.delete("all")
            draw_line_origin()
            lst = read(serialString)
            print(channels)
            # table
            total_rows = len(lst)
            total_columns = len(lst[0])
            # figures
            figure1 = plt.Figure(figsize=(6, 5), dpi=100)
            ax1 = figure1.add_subplot(111)
            bar1 = FigureCanvasTkAgg(figure1, root)
            # bar1.get_tk_widget().pack(side=LEFT, fill=BOTH)
            bar1.get_tk_widget().grid(row=total_rows+5,column=0,columnspan=3,rowspan=20)
            data1 = {'Number' : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                     'channels': channels
            }
            df1 = DataFrame(data1, columns=['Number', 'channels'])
            df1 = df1[['Number', 'channels']].groupby('Number').sum()
            df1.plot(kind='bar', legend=True, ax=ax1)
            ax1.set_title('Channels Traffic')
            #Figure2
            figure2 = plt.Figure(figsize=(6, 5), dpi=100)
            ax2 = figure2.add_subplot(111)
            bar2 = FigureCanvasTkAgg(figure2, root)
            bar2.get_tk_widget().grid(row=total_rows + 5, column=3, columnspan=5, rowspan=20)
            data2 = {'SSID': ssid,
                     'RSSI': rssi
                     }
            df2 = DataFrame(data2, columns=['SSID', 'RSSI'])
            df2 = df2[['SSID', 'RSSI']].groupby('SSID').sum()
            df2.plot(kind='bar', legend=True, ax=ax2)
            ax2.set_title('SSID Quality')
            flag = 0
    root.title('Wireless Project')
    t = Table(root)
    root.after(1000, update)

update()
root.mainloop()


