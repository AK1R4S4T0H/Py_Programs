# Simple Python Calculator GUI
# Prettier than normal calculators in my opinion
# tried to add a graphing function
# plan on adding more mathematical funcitons
#
""" Created by: AK1R4S4T0H
"""
import tkinter as tk;from tkinter import font as tkFont
import math


root = tk.Tk()
root.title('/Calc-ium/');root.config(bg='#8B00FF')
root.geometry = (200, 840);root.resizable(True, True)
root.attributes('-alpha', 0.97)
# fonts
helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)
Entry = tkFont.Font(family='Britannic Bold', size=15, weight=tkFont.BOLD)
# text box at top of window
e = tk.Entry(root, font=Entry, bd=85, fg='white', bg='black', width=35, borderwidth=5, state='normal')
e.grid(row=0, column=0, columnspan=10, ipadx=10, ipady=5, pady=5)
curr = e.get()
# this is what controls the  text box
def button_add(number):
    current = e.get()
    # e.delete(0)
    if number in range(0, 10):
        e.delete(-1100000, 11100000)
        e.insert(0, str(current) +  str(number))
    elif number == 'C':
        e.delete(-1100000, 11100000)
    return
# import mut graphs
def G_butt():
        import mut
        return
# add button
def butt_add():
    fi_num = e.get()
    global f_num
    f_num = float(fi_num)
    e.delete(-1100000, 11100000)
    e.insert(0, '+ ')
    return
# Subtract button
def butt_sub():
    fi_num = e.get()
    global f_num
    f_num = float(fi_num)
    e.delete(-1100000, 11100000)
    e.insert(0, '- ')
    return
# mult button
def butt_mult():
    fi_num = e.get()
    global f_num
    f_num = float(fi_num)
    e.delete(-1100000, 11100000)
    e.insert(0, '* ')
    return
# powers button
def butt_power():
    fi_num = e.get()
    global f_num
    f_num = float(fi_num)
    e.delete(-1100000, 11100000)
    e.insert(0, '** ')
    return
# division button
def butt_div():
    fi_num = e.get()
    global f_num
    f_num = float(fi_num)
    e.delete(-1100000, 11100000)
    e.insert(0, '/ ')
    return
# dot button
def butt_dot():
    b = e.get()
    e.insert(tk.END, '.')
    if '.' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, already has dot, redo problem!')
    else:
        pass
# sin button
def butt_sin():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, 'sin(' + b + ')')
    if 'sin(' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
def butt_tanh():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, 'tanh(' + b + ')')
    if 'tanh(' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
def butt_sinh():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, 'sinh(' + b + ')')
    if 'sinh(' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
# cos button
def butt_cos():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, 'cos(' + b + ')')
    if 'cos(' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
# tan button
def butt_tan():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, 'tan(' + b + ')')
    if 'tan(' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
# Square root button
def butt_sqrt():
    b = e.get()
    e.delete(-1100000, 11100000)
    e.insert(0, '√ ' + b )
    if '√ ' in b:
        e.delete(-1100000, 11100000)
        e.insert(0, 'Error, redo problem!')
    else:
        pass
# create the equals function, which is where all the magic happens
def butt_eq():
    
    b = e.get()
    e.delete(-1100000, 11100000)
    if '- ' in b:
        a = f_num
        b = float(b.strip('- '))
        e.delete(-1100000, 11100000)
        e.insert(0, (float(a) - float(b)))
    elif '+ ' in b:
        a = f_num
        b = float(b.strip('+ '))
        e.delete(-1100000, 11100000)
        e.insert(0, (float(a) + float(b)))
    elif '* ' in b:
        a = f_num
        b = float(b.strip('* '))
        e.delete(-1100000, 11100000)
        e.insert(0, (float(a) * float(b)))
    elif '** ' in b:
        a = f_num
        b = float(b.strip('* '))
        e.delete(-1100000, 11100000)
        e.insert(0, (float(a) ** float(b)))
    elif '/ ' in b:
        a = f_num
        b = float(b.strip('/ '))
        e.delete(-1100000, 11100000)
        e.insert(0, (float(a) / float(b)))
    elif 'sin(' in b:
        b = float(b.strip('sin()'))
        e.delete(-1100000, 11100000)
        e.insert(0, math.sin(float(b)))
    elif 'tanh(' in b:
        b = float(b.strip('tanh()'))
        e.delete(-1100000, 11100000)
        e.insert(0, math.tanh(float(b)))
    elif 'sinh(' in b:
        b = float(b.strip('sinh()'))
        e.delete(-1100000, 11100000)
        e.insert(0, math.sinh(float(b)))
    elif 'tan(' in b:
        b = float(b.strip('tan()'))
        e.delete(-1100000, 11100000)
        e.insert(0, math.tan(float(b)))
    elif 'cos(' in b:
        b = float(b.strip('cos()'))
        e.delete(-1100000, 11100000)
        e.insert(0, math.cos(float(b)))
    elif '√ ' in b:
        b = float(b.strip('√ '))
        e.delete(-1100000, 11100000)
        e.insert(0, math.sqrt(float(b)))
    return
# create the buttons
butt_1 = tk.Button(root, font=helv36, fg='black', bg='red', text='1', borderwidth=15, padx=5, pady=0, command=lambda: button_add(1))
butt_2 = tk.Button(root, font=helv36, fg='black', bg='yellow', text='2', borderwidth=15, padx=5, pady=0, command=lambda: button_add(2))
butt_3 = tk.Button(root, font=helv36, fg='black', bg='green', text='3', borderwidth=15, padx=5, pady=0, command=lambda: button_add(3))
butt_4 = tk.Button(root, font=helv36, fg='black', bg='red', text='4', borderwidth=15,  padx=5, pady=0, command=lambda: button_add(4))
butt_5 = tk.Button(root, font=helv36, fg='black', bg='yellow', text='5', borderwidth=15, padx=5, pady=0, command=lambda: button_add(5))
butt_6 = tk.Button(root, font=helv36, fg='black', bg='green', text='6', borderwidth=15, padx=5, pady=0, command=lambda: button_add(6))
butt_7 = tk.Button(root, font=helv36, fg='black', bg='red', text='7', borderwidth=15,  padx=5, pady=0, command=lambda: button_add(7))
butt_8 = tk.Button(root, font=helv36, fg='black', bg='yellow', text='8', borderwidth=15, padx=5, pady=0, command=lambda: button_add(8))
butt_9 = tk.Button(root, font=helv36, fg='black', bg='green', text='9', borderwidth=15, padx=5, pady=0, command=lambda: button_add(9))
butt_0 = tk.Button(root, font=helv36, fg='black', bg='orange', text='0', borderwidth=15, padx=5, pady=0, command=lambda: button_add(0))
C_button = tk.Button(root, font=helv36, fg='white', bg='grey', text='Clear', borderwidth=15, padx=23, pady=5, command=lambda: button_add('C'))
div_but = tk.Button(root, font=helv36, fg='white', bg='black', text='/', borderwidth=15, padx=23, pady=5, command=butt_div)
mult_but = tk.Button(root, font=helv36, fg='white', bg='black', text='X', borderwidth=15, padx=20, pady=5, command=butt_mult)
sub_but = tk.Button(root, font=helv36, fg='white', bg='black', text='-', borderwidth=15, padx=23, pady=5, command=butt_sub)
add_but = tk.Button(root, font=helv36, fg='white', bg='black', text='+', borderwidth=15, padx=20, pady=5, command=butt_add)
equal_but = tk.Button(root, font=helv36, fg='white', bg='grey', text='Enter', borderwidth=15, padx=23, pady=5, command=butt_eq)
dot_but = tk.Button(root, font=helv36, fg='white', bg='black', text='.', borderwidth=15, padx=23, pady=5, command=butt_dot)
G_button = tk.Button(root, font=helv36, fg='white', bg='grey', text='Graph', borderwidth=15, padx=20, pady=5, command=G_butt)
sin_but = tk.Button(root, font=helv36, fg='white', bg='black', text='sin', borderwidth=15, padx=23, pady=5, command=butt_sin)
tanh_but = tk.Button(root, font=helv36, fg='white', bg='black', text='tanh', borderwidth=15, padx=23, pady=5, command=butt_tanh)
sinh_but = tk.Button(root, font=helv36, fg='white', bg='black', text='sinh', borderwidth=15, padx=23, pady=5, command=butt_sinh)
cos_but = tk.Button(root, font=helv36, fg='white', bg='black', text='cos', borderwidth=15, padx=23, pady=5, command=butt_cos)
tan_but = tk.Button(root, font=helv36, fg='white', bg='black', text='tan', borderwidth=15, padx=23, pady=5, command=butt_tan)
sqrt_but = tk.Button(root, font=helv36, fg='white', bg='black', text='SqRt', borderwidth=15, padx=23, pady=5, command=butt_sqrt)
power_but = tk.Button(root, font=helv36, fg='white', bg='black', text='^', borderwidth=15, padx=23, pady=5, command=butt_power)
# adds them to grid
butt_1.grid(row=3 , column=0)
butt_2.grid(row=3 , column=1)
butt_3.grid(row=3 , column=2)
butt_4.grid(row=2 , column=0)
butt_5.grid(row=2 , column=1)
butt_6.grid(row=2 , column=2)
butt_7.grid(row=1 , column=0)
butt_8.grid(row=1 , column=1)
butt_9.grid(row=1 , column=2)
butt_0.grid(row=4 , column=1, ipadx=20)
# all buttons but nums
C_button.grid(row=1, column=3)
div_but.grid(row=6, column=1)
mult_but.grid(row=4, column=0)
sin_but.grid(row=4, column=2)
sinh_but.grid(row=6, column=3)
tanh_but.grid(row=6, column=4)
cos_but.grid(row=5, column=2)
tan_but.grid(row=6, column=2)
sqrt_but.grid(row=4, column=3)
power_but.grid(row=5, column=3)
add_but.grid(row=5, column=0)
sub_but.grid(row=5, column=1)
equal_but.grid(row=2, column=3)
dot_but.grid(row=6, column=0)
G_button.grid(row=3, column=3)
# runs the window
root.mainloop()