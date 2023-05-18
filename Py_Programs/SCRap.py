""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

def scrape_button_clicked():
    url = entry_url.get()
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string.strip()
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    links = [a['href'] for a in soup.find_all('a')]
    
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

window = tk.Tk()
window.title("Web Scraper")
window.geometry("600x400")

frame_input = tk.Frame(window)
frame_input.pack(pady=10)

entry_url = tk.Entry(frame_input, width=50)
entry_url.grid(row=0, column=0, padx=5)

button_scrape = tk.Button(frame_input, text="Scrape", command=scrape_button_clicked)
button_scrape.grid(row=0, column=1, padx=5)

frame_info = tk.Frame(window)
frame_info.pack(pady=10)

label_title = tk.Label(frame_info, text="Title:")
label_title.grid(row=0, column=0, sticky="w")

text_title = tk.Text(frame_info, height=1, width=50)
text_title.grid(row=0, column=1, padx=5)
text_title.configure(state='disabled')

label_paragraphs = tk.Label(frame_info, text="Paragraphs:")
label_paragraphs.grid(row=1, column=0, sticky="w")

text_paragraphs = tk.Text(frame_info, height=10, width=50)
text_paragraphs.grid(row=1, column=1, padx=5)
text_paragraphs.configure(state='disabled')

label_links = tk.Label(frame_info, text="Links:")
label_links.grid(row=2, column=0, sticky="w")

text_links = tk.Text(frame_info, height=10, width=50)
text_links.grid(row=2, column=1, padx=5)
text_links.configure(state='disabled')

window.mainloop()
