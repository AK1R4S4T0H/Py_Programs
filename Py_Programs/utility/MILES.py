import tkinter as tk
from tkinter import ttk
#window
root = tk.Tk()
root.title('Miles to Kilos')
root.geometry('150x75')
root.pack_propagate(False)
root.config(bg='black')
# define miles to kilos
def mToK():
    num = float(put.get())
    if num > 0:
        num = float(num) * 1.60934
        label.config(text=('total:', num))
    else: pass
    return num
# 3ntry
put =  ttk.Entry(root)
put.pack()
# TOtal label
label = ttk.Label(root, text='Total:')
label.pack()
# button 
button = tk.Button(root, text='Miles to Kilos', command=mToK, bg='red', fg='white')
button.pack()
# mainloop
root.mainloop()