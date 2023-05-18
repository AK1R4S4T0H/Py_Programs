""" Created by: AK1R4S4T0H
"""

import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

root = tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()


def getExcel ():
    global df
    
    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv (import_file_path)
    print (df)
    
browseButton_Excel = tk.Button(text="      Import Excel File     ", command=getExcel, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(10, 10, window=browseButton_Excel)

def plot ():
    plt.plot(df)
    plt.show()
    
plotButton = tk.Button(text='     Plot     ', command=plot, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 180, window=plotButton)
 

def plotBar():
    global df
    plt.bar(df["x"], df["y"])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Bar Chart')
    plt.show()
    
def plotLine():
    global df
    plt.plot(df["x"], df["y"])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Line Chart')
    plt.show()
    
def plotScatter():
    global df
    plt.scatter(df["x"], df["y"])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Scatter Chart')
    plt.show()
    
button1 = tk.Button(text='Bar Chart', command=plotBar, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(75, 150, window=button1)

button2 = tk.Button(text='Line Chart', command=plotLine, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(75, 180, window=button2)

button3 = tk.Button(text='Scatter Chart', command=plotScatter, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(75, 210, window=button3)


root.geometry = (400,400)
root.mainloop()