# My Attempt at a Python Notepad clone, it is pretty much there
# Attempting to add Tokenizer, to maybe eventually add syntax highlighting
# Added right click menu with many features
""" Created by: AK1R4S4T0H
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import tkinter.colorchooser as colorchooser
import tkinter as tk
from tkinter import ttk, filedialog, font, colorchooser


class Notes:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Notepad")
        self.current_file = None
        self.bold_on = False
        self.italic_on = False
        self.underline_on = False
        self.font_family = tk.StringVar()
        self.font_size = tk.StringVar()
        self.font_color = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.theme_use('default')

        self.style.configure("TFrame", background="black")
        self.style.configure("TLabel", background="black", foreground="white")
        self.style.configure("TMenu", background="black", foreground="white")
        self.style.configure("TButton", background="black", foreground="white")
        self.style.configure("TScrollbar", background="black", troughcolor="black", gripcount=0)
        self.style.map(
            "TScrollbar",
            background=[("active", "black")],
            troughcolor=[("active", "black")]
        )

        self.frame = ttk.Frame(self.root, style="TFrame")
        self.frame.pack(fill='both', expand=True)

        self.menu_bar = tk.Menu(self.root, bg="black", fg="white")
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, bg="black", fg="white")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg="black", fg="white")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Bold", accelerator="Ctrl+B", command=self.toggle_bold)
        self.edit_menu.add_command(label="Italic", accelerator="Ctrl+I", command=self.toggle_italic)
        self.edit_menu.add_command(label="Underline", accelerator="Ctrl+U", command=self.toggle_underline)

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0, bg="black", fg="white")
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.font_family_menu = tk.Menu(self.format_menu, tearoff=0, bg="black", fg="white")
        self.format_menu.add_cascade(label="Font Family", menu=self.font_family_menu)
        fonts = list(font.families())
        fonts.sort()
        for font_family in fonts:
            self.font_family_menu.add_radiobutton(label=font_family, variable=self.font_family, value=font_family,
                                                command=self.change_font_family)
        self.format_menu.add_command(label="Font Size", command=self.change_font_size)
        self.format_menu.add_command(label="Font Color", command=self.change_font_color)

        self.status_bar = ttk.Label(self.root, text="Ln 1, Col 1", anchor='w', justify='center')
        self.status_bar.pack(side='bottom', fill='x')

        default_font_size = 15

        self.text_area = tk.Text(self.frame, undo=True, bg="#221122", fg="white")
        self.text_area.pack(side='left', fill='both', expand=True)

        self.text_area.bind("<MouseWheel>", self.on_mousewheel)
        self.text_area.bind("<Button-4>", self.on_mousewheel)
        self.text_area.bind("<Button-5>", self.on_mousewheel)
        self.text_area.config(font=("TkDefaultFont", default_font_size))
        self.text_area.pack(side='left', fill='both', expand=True)
        self.text_area.bind('<KeyRelease>', self.update_status_bar)
        self.text_area.bind('<ButtonRelease-1>', self.update_status_bar)
        self.text_area.bind('<ButtonRelease-3>', self.update_status_bar)
        self.text_area.bind('<B1-Motion>', self.update_status_bar)
        self.text_area.bind('<B3-Motion>', self.update_status_bar)
        self.text_area.bind("<Control-n>", self.new_file)
        self.text_area.bind("<Control-o>", self.open_file)
        self.text_area.bind("<Control-s>", self.save_file)
        self.text_area.bind("<Control-S>", self.save_file_as)
        self.text_area.bind("<Control-x>", self.cut)
        self.text_area.bind("<Control-c>", self.copy)
        self.text_area.bind("<Control-v>", self.paste)
        self.text_area.bind("<Control-b>", self.toggle_bold)
        self.text_area.bind("<Control-i>", self.toggle_italic)
        self.text_area.bind("<Control-u>", self.toggle_underline)

        # right-click menu
        self.text_menu = tk.Menu(self.root, tearoff=0, bg='black', fg='white')
        self.text_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.text_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        self.text_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.text_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        self.text_menu.add_separator()
        self.text_menu.add_command(label="Cut", command=self.cut)
        self.text_menu.add_command(label="Copy", command=self.copy)
        self.text_menu.add_command(label="Paste", command=self.paste)
        self.text_menu.add_separator()
        self.text_menu.add_command(label="Bold", command=self.toggle_bold)
        self.text_menu.add_command(label="Italic", command=self.toggle_italic)
        self.text_menu.add_command(label="Underline", command=self.toggle_underline)
        self.text_menu.add_separator()
        self.text_menu.add_cascade(label="Font Family", menu=self.font_family_menu)
        self.text_menu.add_command(label="Font Size", command=self.change_font_size)
        self.text_menu.add_command(label="Font Color", command=self.change_font_color)
        self.text_menu.add_separator()
        self.text_menu.add_command(label="Exit", command=self.root.quit)
        # Bind the right-click menu to the text area
        self.text_area.bind("<Button-3>", self.show_text_menu)

        self.root.bind("<Control-s>", self.save_file)

    def on_mousewheel(self, event):
        self.text_area.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_status_bar(self, event=None):
        row, col = self.text_area.index('insert').split('.')
        status_text = "Ln {}, Col {}".format(int(row), int(col) + 1)
        self.status_bar.config(text=status_text)

    def show_text_menu(self, event):
        self.text_menu.tk_popup(event.x_root, event.y_root)

    def update(self, event=None):
        self.update_title()

    def update_title(self):
        if self.current_file:
            self.root.title(self.current_file + " - Notes")
        else:
            self.root.title("Untitled - Notes")

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
        font_size_spinbox.bind("<Return>",
                               lambda event: self.text_area.configure(font=(self.font_family.get(), self.font_size.get())))

    def change_font_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.font_color.set(color)
            self.text_area.configure(fg=color)

    def cut(self):
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        self.text_area.event_generate("<<Paste>>")

    def new_file(self, event=None):
        self.current_file = None
        self.text_area.delete(1.0, 'end')
        self.update_title()

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.text_area.delete(1.0, 'end')
                self.text_area.insert('end', text)
            self.current_file = file_path
            self.update_title()

    def run(self):
        self.root.mainloop()


notes = Notes()
notes.run()
