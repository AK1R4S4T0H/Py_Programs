import tkinter as tk
import AUDIO
import Calculator as Calc

root = tk.Tk()
root.title("STUFF")



butt_1 = tk.Button(root, text="AUDIO PLAYER", command=lambda: AUD())
butt_1.pack()

butt_2 = tk.Button(root, text="CALCULATOR", command=lambda: calu())
butt_2.pack()

butt_3 = tk.Button(root, text="CHATBOT")
butt_3.pack()

butt_4 = tk.Button(root, text="IMAGE VIEWER")
butt_4.pack()

butt_5 = tk.Button(root, text="JAPANESE")
butt_5.pack()

butt_6 = tk.Button(root, text="MIDI")
butt_6.pack()

butt_7 = tk.Button(root, text="PYPAD")
butt_7.pack()

butt_8 = tk.Button(root, text="PATTERN")
butt_8.pack()

butt_9 = tk.Button(root, text="PYTOEXE")
butt_9.pack()

butt_10 = tk.Button(root, text="STAR")
butt_10.pack()

def AUD():
    root = AUDIO.Audio()

def calu():
    Calc()




root.mainloop()
