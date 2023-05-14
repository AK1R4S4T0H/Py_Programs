import random
import tkinter as tk

japanese_phrases = {'A','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w', 'x','y','z',
'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V', 'W','X','Y','Z',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17','18', '19', '20'}

root = tk.Tk()
root.title("ABC's")
root.geometry("400x400")

# create the label widget for displaying the Japanese phrases
japanese_label = tk.Label(root, font=("Fantasy", 50), bg="black", fg="white")

# function to display a random Japanese phrase and its definition
def display_phrase():
    phrase = random.choice(list(japanese_phrases))
    japanese_label.config(text=f"{phrase}")
    
    # set the timer to call the function again after 10 seconds
    root.after(10000, display_phrase)

# create the button widget and bind it to the display_phrase function
button = tk.Button(root, text="Show me a phrase!", command=display_phrase)

# pack the label and button widgets into the window
japanese_label.pack(expand=True, fill='both')
button.pack()



# run the tkinter event loop
root.mainloop()