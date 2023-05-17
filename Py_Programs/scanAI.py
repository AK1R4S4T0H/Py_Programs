import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import asyncio
import nmap
import subprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

async def ai_agent(target):
    nm = nmap.PortScanner()
    scan_options = "-Pn -sV -O -p-"
    await asyncio.sleep(0)  # Allow other async tasks to run

    loop = asyncio.get_event_loop()
    scan_results = await loop.run_in_executor(None, nm.scan, target, scan_options)

    open_ports = []
    operating_system = ""
    services = []

    for port in scan_results['tcp'].keys():
        if scan_results['tcp'][port]['state'] == 'open':
            open_ports.append(port)

    if 'osmatch' in scan_results:
        operating_system = scan_results['osmatch'][0]['osclass'][0]['osfamily']

    if 'tcp' in scan_results:
        for port in scan_results['tcp'].keys():
            service_name = scan_results['tcp'][port]['name']
            service_version = scan_results['tcp'][port]['version']
            service_info = f"{service_name} ({service_version})"
            services.append(service_info)

    analysis = {
        'Open Ports': open_ports,
        'Operating System': operating_system,
        'Services': services
    }

    model = RandomForestClassifier()
    data = [[len(open_ports)]]
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    loop = asyncio.get_event_loop()
    prediction = await loop.run_in_executor(None, model.predict, data)
    analysis['Prediction'] = prediction[0]

    return analysis

def run_nmap(target):
    command = ["sudo", "nmap", "-Pn", "-sV", "-O", "-p-", target]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

def scan_button_click():
    target = ip_entry.get()
    output, error = run_nmap(target)
    output_text.delete(1.0, tk.END)
    if output:
        output_text.insert(tk.END, output)
    elif error:
        output_text.insert(tk.END, f"Error: {error}")

window = tk.Tk()
window.title("Nmap AI Agent")
window.geometry("450x450")


style = ttk.Style()
style.theme_use('clam')  
style.configure('TLabel', foreground='white', background='black')
style.configure('TEntry', foreground='white', background='black')
style.configure('TButton', foreground='white', background='gray')

ip_label = ttk.Label(window, text="Enter IP Address:")
ip_label.pack()

ip_entry = ttk.Entry(window, style='TEntry')
ip_entry.pack()

output_text = ScrolledText(window, height=20, width=50)
output_text.pack()

scan_button = ttk.Button(window, text="Scan", command=scan_button_click, style='TButton')
scan_button.pack(fill=tk.BOTH, expand=True)

window.mainloop()
