import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd

def merge_csvs():
    folder_path = filedialog.askdirectory()
    if folder_path:
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        df_merged = pd.DataFrame()
        for csv_file in csv_files:
            csv_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(csv_path)
            df_merged = pd.concat([df_merged, df], ignore_index=True)
        
        save_path = filedialog.asksaveasfilename(defaultextension='.csv')
        if save_path:
            df_merged.to_csv(save_path, index=False)
            print('CSV files merged successfully!')

window = tk.Tk()
window.title('CSV Merger')

open_folder_button = tk.Button(window, text='Open Folder', command=merge_csvs)
open_folder_button.pack(pady=10)

window.mainloop()
