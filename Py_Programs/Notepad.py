# My Attempt at a Python Notepad clone, it is pretty much there
# ISSUES: Title
#
import tkinter as tk
from tkinter import filedialog
from tkinter import font

class Notes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notepad")
        self.root.geometry("800x500")
        self.root.configure(bg='black')
        self.root.winfo_colormapfull()
        self.current_file = None
        self.font_family = tk.StringVar(self.root)
        self.font_size = tk.StringVar(self.root)
        self.font_size.set('12')
        self.font_color = tk.StringVar(self.root)
        self.font_color.set('black')
        self.bold_on = False
        self.italic_on = False
        self.underline_on = False
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill='both', expand=True)

        # menu bar
        self.menu_bar = tk.Menu(self.root, bg='black', fg='white')
        self.root.config(menu=self.menu_bar, background='black')

        # file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg='black', fg='white', activebackground='white', activeforeground='black')
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # create edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg='black', fg='white', activebackground='white', activeforeground='black')
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.toggle_bold)
        self.edit_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.toggle_italic)
        self.edit_menu.add_command(label="Underline", accelerator="Ctrl+U", command=self.toggle_underline)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # create format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0, bg='black', fg='white', activebackground='white', activeforeground='black')
        self.font_family_menu = tk.Menu(self.format_menu, tearoff=0)
        fonts = list(font.families())
        fonts.sort()
        for font_family in fonts:
            self.font_family_menu.add_radiobutton(label=font_family, variable=self.font_family, value=font_family, command=self.change_font_family)
        self.format_menu.add_cascade(label="Font Family", menu=self.font_family_menu)
        self.format_menu.add_command(label="Font Size", command=self.change_font_size)
        self.format_menu.add_command(label="Font Color", command=self.change_font_color)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        # status bar
        self.status_bar = tk.Label(self.root, text="Ln 1, Col 1")
        self.status_bar.pack(side='bottom', fill='x')

        # text area
        self.text_area = tk.Text(self.frame, font=(self.font_family.get(), self.font_size.get()))
        self.text_area.pack(fill='both', expand=True)
        self.text_area.bind('<Any-KeyPress>', self.update)

        # scrollbar
        self.scroll_bar = tk.Scrollbar(self.text_area)
        self.scroll_bar.pack(side='right', fill='y')
        self.scroll_bar.config(command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scroll_bar.set)

        # bind status bar to text area
        self.text_area.bind('<KeyRelease>', self.update_status_bar)

    def update(self, event=None):
        self.update_title()
        
    def update_title(self):
        if self.current_file:
            self.root.title(self.current_file + " - Notes")
        else:
            self.root.title("Untitled - Notes")

    def update_status_bar(self, event=None):
        row, col = self.text_area.index('end-1c').split('.')
        status_text = "Ln {}, Col {}".format(int(row), int(col) + 1)
        self.status_bar.config(text=status_text)

    def new_file(self, event=None):
        self.current_file = None
        self.text_area.delete(1.0, 'end')
        self.update_title()

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
            self.current_file = file_path
            self.text_area.delete(1.0, 'end')
            self.text_area.insert('end', text)
            self.update_title()

    def save_file(self, event=None):
        if self.current_file:
            text = self.text_area.get(1.0, 'end')
            with open(self.current_file, 'w') as file:
                file.write(text)
            self.update_title()
        else:
            self.save_file_as()

    def save_file_as(self, event=None):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            text = self.text_area.get(1.0, 'end')
            with open(file_path, 'w') as file:
                file.write(text)
            self.current_file = file_path
            self.update_title()

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def toggle_bold(self):
        if self.bold_on:
            self.text_area.tag_remove('bold', 'sel.first', 'sel.last')
            self.bold_on = False
        else:
            self.text_area.tag_add('bold', 'sel.first', 'sel.last')
            self.text_area.tag_configure('bold', font=(self.font_family.get(), self.font_size.get(), 'bold'))
            self.bold_on = True

    def toggle_italic(self):
        if self.italic_on:
            self.text_area.tag_remove('italic', 'sel.first', 'sel.last')
            self.italic_on = False
        else:
            self.text_area.tag_add('italic', 'sel.first', 'sel.last')
            self.text_area.tag_configure('italic', font=(self.font_family.get(), self.font_size.get(), 'italic'))
            self.italic_on = True

    def toggle_underline(self):
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
            self.underline_on = False
        else:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
            self.underline_on = True

    def change_font_family(self):
        self.text_area.configure(font=(self.font_family.get(), self.font_size.get()))

    def change_font_size(self):
        font_size_window = tk.Toplevel(self.root)
        font_size_window.title("Font Size")
        font_size_window.resizable(0, 0)
        font_size_label = tk.Label(font_size_window, text="Select font size:")
        font_size_label.pack(side='top', padx=5, pady=5)
        font_size_spinbox = tk.Spinbox(font_size_window, from_=1, to=100, textvariable=self.font_size, width=5)
        font_size_spinbox.pack(side='top', padx=5, pady=5)
        font_size_spinbox.focus()
        font_size_spinbox.bind("<Return>", lambda event: self.text_area.configure(font=(self.font_family.get(), self.font_size.get())))

    def change_font_color(self):
        color = tk.colorchooser.askcolor()[1]
        if color:
            self.font_color.set(color)
            self.text_area.configure(fg=color)

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def new_file(self):
        self.current_file = None
        self.root.title("Untitled - Notes")
        self.text_area.delete('1.0', tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.current_file = file_path
            self.root.title(f"{file_path} - Notes")
            with open(file_path, 'r') as file:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', file.read())

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            self.current_file = file_path
            self.root.title(f"{file_path} - Notes")
            with open(file_path, 'w') as file:
                file.write(self.text_area.get('1.0', tk.END))

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    notepad = Notes()
    notepad.run()
