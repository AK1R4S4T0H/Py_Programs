import tkinter as tk
from tkinter import ttk
import pygame  # Import pygame for sound
import random  # For generating random values

# Initialize pygame mixer for sound
pygame.mixer.init()

def play_sound():
    # Load and play a sound when a popup is shown
    sound = pygame.mixer.Sound('')  # Replace with your sound file path
    sound.play()

def show_random_popups():
    # Generate a random number of popups (between 1 and 10 popups)
    num_popups = random.randint(1, 10000)

    for _ in range(num_popups):
        play_sound()  # Play sound on each popup
        popup = tk.Toplevel()
        popup.title("Popup")
        
        # Random size for the popup
        popup_width = random.randint(200, 400)
        popup_height = random.randint(150, 300)
        popup.geometry(f"{popup_width}x{popup_height}")

        # Random position for the popup on the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        random_x = random.randint(0, screen_width - popup_width)
        random_y = random.randint(0, screen_height - popup_height)

        popup.geometry(f"+{random_x}+{random_y}")
        popup.resizable(False, False)
        popup.configure(bg='black')

        label = ttk.Label(popup, text="Welcome to the Popup!!!!!", foreground='white', background='black', font=('Courier', 18, 'bold'))
        label.pack(pady=50)

        button = ttk.Button(popup, text="Close", command=popup.destroy)
        button.pack(pady=20, padx=50)

        popup.focus_set()
        popup.grab_set()
        popup.transient(root)
        popup.wait_window(popup)

root = tk.Tk()
root.title("Pop-up")
root.geometry("400x300")
root.configure(bg='black')

# Button to generate random popups dynamically
button = ttk.Button(root, text="Show Random Popups", command=show_random_popups)
button.pack(pady=100)

root.mainloop()
