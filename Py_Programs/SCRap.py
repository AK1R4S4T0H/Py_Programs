""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
from bs4 import BeautifulSoup
import requests
import os
import csv

class Scrap():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Web Scraper")
        self.window.geometry("600x600")
        self.style = ttk.Style()
        self.style.theme_use('alt')  # Default theme
        self.window.config(background="#a2a6d6")
        self.style.configure("TFrame", background="#a2a6d6")
        self.style.configure("TRadiobutton", background="#a2a6d6", foreground="black")
        self.style.configure("TLabel", background="#a2a6d6", foreground="black")
        self.style.configure("TButton", background="#a2a6d6", foreground="black")
        self.style.map("TButton",
                background=[('active', '#d6c9d9'), ('!active', '#a2a6d6')],
                foreground=[('active', 'black'), ('!active', 'black')])
        self.style.map("TRadiobutton",
                background=[('active', '#d6c9d9'), ('!active', '#a2a6d6')],
                foreground=[('active', 'black'), ('!active', 'black')])

        def scrape_button_clicked():
            url = entry_url.get()

            # Check URL for http:// or https://
            if not url.startswith('http://') and not url.startswith('https://'):
                # Try with https://
                url_with_https = f'https://{url}'
                try:
                    response = requests.get(url_with_https)
                    response.raise_for_status()  # Check request errors
                except requests.RequestException:
                    # Try http://
                    url_with_http = f'http://{url}'
                    try:
                        response = requests.get(url_with_http)
                        response.raise_for_status() 
                    except requests.RequestException as e:
                        display_error_message(f"Request Error: {str(e)}")
                        return
                except Exception as e:
                    display_error_message(f"An error occurred: {str(e)}")
                    return
            else:
                # URL includes http:// https://
                try:
                    response = requests.get(url)
                    response.raise_for_status() 
                except requests.RequestException as e:
                    display_error_message(f"Request Error: {str(e)}")
                    return
                except Exception as e:
                    display_error_message(f"An error occurred: {str(e)}")
                    return

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string.strip()
            paragraphs = [p.get_text() for p in soup.find_all('p')]
            links = [a['href'] for a in soup.find_all('a')]

            display_scraped_content(title, paragraphs, links)

        def clear_button_clicked():
            entry_url.delete(0, tk.END)
            text_title.configure(state='normal')
            text_title.delete('1.0', tk.END)
            text_title.configure(state='disabled')
            text_paragraphs.configure(state='normal')
            text_paragraphs.delete('1.0', tk.END)
            text_paragraphs.configure(state='disabled')
            text_links.configure(state='normal')
            text_links.delete('1.0', tk.END)
            text_links.configure(state='disabled')

        def display_error_message(message):
            text_title.configure(state='normal')
            text_title.delete('1.0', tk.END)
            text_title.insert(tk.END, f"Error: {message}")
            text_title.configure(state='disabled')
            text_paragraphs.configure(state='normal')
            text_paragraphs.delete('1.0', tk.END)
            text_paragraphs.configure(state='disabled')
            text_links.configure(state='normal')
            text_links.delete('1.0', tk.END)
            text_links.configure(state='disabled')

        def display_scraped_content(title, paragraphs, links):
            text_title.configure(state='normal')
            text_title.delete('1.0', tk.END)
            text_title.insert(tk.END, title)
            text_title.configure(state='disabled')
            
            text_paragraphs.configure(state='normal')
            text_paragraphs.delete('1.0', tk.END)
            for paragraph in paragraphs:
                text_paragraphs.insert(tk.END, f"{paragraph}\n")
            text_paragraphs.configure(state='disabled')
            
            text_links.configure(state='normal')
            text_links.delete('1.0', tk.END)
            for link in links:
                text_links.insert(tk.END, f"{link}\n")
            text_links.configure(state='disabled')
            # Append scraped data to CSV 
            directory = "scrap"
            filename = "scrap.csv"
            os.makedirs(directory, exist_ok=True)  # Create "scrap" dir if it doesn't exist
            
            file_path = os.path.join(directory, filename)
            
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([title])
                writer.writerow(paragraphs)
                writer.writerow(links)

        def open_link(event, url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string.strip()
                paragraphs = [p.get_text() for p in soup.find_all('p')]
                links = [a['href'] for a in soup.find_all('a')]
                display_scraped_content(title, paragraphs, links)
            except requests.RequestException as e:
                display_error_message(f"Request Error: {str(e)}")
            except Exception as e:
                display_error_message(f"An error occurred: {str(e)}")

        frame_input = ttk.Frame(self.window)
        frame_input.grid(row=0, column=0, pady=10)

        entry_url = ttk.Entry(frame_input, width=50)
        entry_url.grid(row=0, column=0, padx=5)

        button_scrape = ttk.Button(frame_input, text="Scrape", command=scrape_button_clicked)
        button_scrape.grid(row=0, column=1, padx=5)

        button_clear = ttk.Button(frame_input, text="Clear", command=clear_button_clicked)
        button_clear.grid(row=0, column=2, padx=5)

        frame_display = ttk.Frame(self.window)
        frame_display.grid(row=1, column=0)

        theme_var = tk.IntVar()
        theme_var.set(0)  # Default theme
        
        text_title = scrolledtext.ScrolledText(frame_display, wrap=tk.WORD, width=73, height=3)
        text_title.insert(tk.END, "Title")
        text_title.configure(state='disabled')
        text_title.grid(row=0, column=0, pady=5)
        text_title.config(background="#d6c9d9", foreground="black")

        text_paragraphs = scrolledtext.ScrolledText(frame_display, wrap=tk.WORD, width=73, height=10)
        text_paragraphs.insert(tk.END, "Paragraphs")
        text_paragraphs.configure(state='disabled')
        text_paragraphs.grid(row=1, column=0, pady=5)
        text_paragraphs.config(background="#d6c9d9", foreground="black")

        text_links = scrolledtext.ScrolledText(frame_display, wrap=tk.WORD, width=73, height=13)
        text_links.insert(tk.END, "Links")
        text_links.grid(row=2, column=0, pady=5)
        text_links.config(background="#d6c9d9", foreground="black")

        frame_theme = ttk.Frame(self.window)
        frame_theme.grid(row=2, column=0, pady=10, padx=10, sticky=tk.SW)

        def change_theme():
            theme = theme_var.get()
            
            if theme == 0: # Light theme
                self.style.theme_use('alt')  
                self.window.config(background="#a2a6d6")
                self.style.configure("TFrame", background="#a2a6d6")
                self.style.configure("TRadiobutton", background="#a2a6d6", foreground="black")
                self.style.configure("TLabel", background="#a2a6d6", foreground="black")
                self.style.configure("TButton", background="#a2a6d6", foreground="black")
                self.style.map("TButton",
                background=[('active', '#d6c9d9'), ('!active', '#a2a6d6')],
                foreground=[('active', 'black'), ('!active', 'black')])
                self.style.map("TRadiobutton",
                background=[('active', '#d6c9d9'), ('!active', '#a2a6d6')],
                foreground=[('active', 'black'), ('!active', 'black')])
                text_title.config(background="#d6c9d9", foreground="black")
                text_paragraphs.config(background="#d6c9d9", foreground="black")
                text_links.config(background="#d6c9d9", foreground="black")


            elif theme == 1: # Dark theme
                self.style.theme_use('alt')  
                self.window.config(background="#4c4c4c")
                self.style.configure("TFrame", background="#4c4c4c")
                self.style.configure("TButton", background="#4c4c4c", foreground="white")
                self.style.configure("TRadiobutton", background="#4c4c4c", foreground="white")
                self.style.configure("TLabel", background="#4c4c4c", foreground="white")
                self.style.map("TButton",
                background=[('active', 'red')],
                foreground=[('active', 'white')])
                self.style.map("TRadiobutton",
                background=[('active', 'red')],
                foreground=[('active', 'white')])
                text_title.config(background="#7c7c7c", foreground="white")
                text_paragraphs.config(background="#7c7c7c", foreground="white")
                text_links.config(background="#7c7c7c", foreground="white")

        label_theme = ttk.Label(frame_theme, text="Theme:")
        label_theme.grid(row=0, column=0, sticky=tk.W, padx=5)

        radio_default = ttk.Radiobutton(frame_theme, text="Light", variable=theme_var, value=0, command=change_theme)
        radio_default.grid(row=0, column=1, padx=5)

        radio_dark = ttk.Radiobutton(frame_theme, text="Dark", variable=theme_var, value=1, command=change_theme)
        radio_dark.grid(row=0, column=2, padx=5)

        def popup():
            popup = tk.Toplevel()
            popup.title("About")
            popup.geometry("300x200")
            popup.resizable(False, False)
            popup.configure(bg='black')
            label = ttk.Label(popup, text="About Web Scraper:", foreground='white', background='black', font=('Courier', 18, 'bold'))
            label.pack(pady=5)
            label1 = ttk.Label(popup, text="Scrap web pages based on URL inputed", foreground='white', background='black', font=('Courier', 10, 'bold'))
            label1.pack(pady=5)
            label2 = ttk.Label(popup, text="Goes to 1st Link every 10 seconds", foreground='white', background='black', font=('Courier', 11, 'bold'))
            label2.pack(pady=5)
            label3 = ttk.Label(popup, text="saves in Folder in parent dir", foreground='white', background='black', font=('Courier', 11, 'bold'))
            label3.pack(pady=5)
            label3 = ttk.Label(popup, text="DIR: scrap, FILE: scrap.csv", foreground='white', background='black', font=('Courier', 11, 'bold'))
            label3.pack(pady=5)
            popup.focus_set()
            popup.grab_set()
            popup.transient(self.window)
            popup.wait_window(popup)

        about = ttk.Button(frame_theme, text="About", command=popup)
        about.grid(row=0, column=5, padx=5)

if __name__ == "__main__":
    scrap = Scrap()
    scrap.window.mainloop()
