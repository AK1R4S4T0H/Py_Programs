# check your terminal for SUDO login, cant nmap without sudo
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import subprocess

def run_nmap(target, options):
    command = ["sudo", "nmap"] + options + [target]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

def preview_command(target, options):
    command = "sudo nmap " + " ".join(options) + " " + target
    return command

def scan_button_click():
    target = ip_entry.get()
    selected_options = [option for option, var in zip(option_values, option_vars) if var.get() == "1"]
    output, error = run_nmap(target, selected_options)
    output_text.delete(1.0, tk.END)
    if output:
        output_text.insert(tk.END, output)
    elif error:
        output_text.insert(tk.END, f"Error: {error}")

def preview_button_click():
    target = ip_entry.get()
    selected_options = [option for option, var in zip(option_values, option_vars) if var.get() == "1"]
    command = preview_command(target, selected_options)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, command)

window = tk.Tk()
window.title("Nmap GUI")
window.geometry("600x800")
window.config(background="black")

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', foreground='white', background='black')
style.configure('TEntry', foreground='black', background='black')
style.configure('TButton', foreground='white', background='#1c1c1c')

ip_label = ttk.Label(window, text="Enter IP Address:")
ip_label.pack()

ip_entry = ttk.Entry(window, style='TEntry', width=50)
ip_entry.pack()

options_frame = ttk.Frame(window, padding=10)
options_frame.pack()

options = [
    ("-sS", "SYN scan"),
    ("-sT", "Connect scan"),
    ("-sU", "UDP scan"),
    ("-sA", "ACK scan"),
    ("-sW", "Window scan"),
    ("-sM", "Maimon scan"),
    ("-sN", "Null scan"),
    ("-sF", "FIN scan"),
    ("-sX", "Xmas scan"),
    ("-sY", "SCTP INIT scan"),
    ("-sZ", "SCTP COOKIE-ECHO scan"),
    ("-sO", "IP protocol scan"),
    ("-p-", "All ports"),
    ("-p1-65535", "Scan all 65535 ports"),
    ("-F", "Fast scan mode"),
    ("-r", "Scan ports consecutively"),
    ("-A", "Aggressive scan"),
    ("-O", "OS detection"),
    ("-T0", "Paranoid timing template"),
    ("-T1", "Sneaky timing template"),
    ("-T2", "Polite timing template"),
    ("-T3", "Normal timing template"),
    ("-T4", "Aggressive timing template"),
    ("-T5", "Insane timing template"),
    ("-d", "Enable debugging output"),
    ("-v", "Increase verbosity level"),
    ("-n", "Disable DNS resolution"),
    ("-Pn", "Treat all hosts as online"),
    ("-PE", "ICMP echo request ping"),
    ("-PP", "ICMP timestamp ping"),
    ("-PM", "ICMP netmask ping"),
    ("-PR", "ARP ping"),
    ("-sn", "Ping scan"),
    ("-PR", "ARP scan"),
    ("-PO", "IP protocol scan"),
    ("-PS", "TCP SYN scan"),
    ("-PA", "TCP ACK scan"),
    ("-PU", "UDP scan"),
    ("-PY", "SCTP INIT scan"),
    ("-PE", "ICMP echo request ping"),
    ("-PP", "ICMP timestamp ping"),
    ("-PM", "ICMP netmask ping"),
    ("-PR", "ARP ping"),
    ("-PE", "ICMP echo request ping"),
    ("-PA", "TCP ACK scan"),
    ("-PU", "UDP scan"),
    ("-PY", "SCTP INIT scan"),
    ("-g <portranges>", "Send packets to specified ports"),
    ("-p <portranges>", "Only scan specified ports"),
    ("-iL <inputfile>", "Input from list of hosts/networks"),
    ("-oN <file>", "Output normal format"),
    ("-oX <file>", "Output XML format"),
    ("-oS <file>", "Output  s|<rIpt kIddi3 0uTpuT"),
    ("-oG <file>", "Output Grepable format"),
    ("-v", "Increase verbosity level"),
    ("-d", "Enable debugging output"),
    ("-h", "Print this help summary page."),
]


option_vars = []
option_values = []

num_columns = 3 # Number of columns in the grid layout
for i, (option, description) in enumerate(options):
    row = i // num_columns
    column = i % num_columns
    option_var = tk.StringVar()
    option_vars.append(option_var)
    option_values.append(option)
    check_button = ttk.Checkbutton(options_frame, text=description, variable=option_var)
    check_button.grid(row=row, column=column, sticky=tk.W)

button_frame = ttk.Frame(window)
button_frame.pack()

preview_button = ttk.Button(button_frame, text="Preview Command", command=preview_button_click, style='TButton')
preview_button.pack(side=tk.LEFT, padx=5)

scan_button = ttk.Button(button_frame, text="Scan", command=scan_button_click, style='TButton')
scan_button.pack(side=tk.LEFT)

output_text = ScrolledText(window, height=17, width=80, bg='grey', fg='white')
output_text.pack()

window.mainloop()

