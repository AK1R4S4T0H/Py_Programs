import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import nmap
import subprocess
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def ai_agent(target):
    nm = nmap.PortScanner()
    scan_options = "-Pn -sV -O -p-"
    nm.scan(target, arguments=scan_options)
    scan_results = nm[target]

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
    prediction = model.predict(data)
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
window.geometry("400x400")

ip_label = tk.Label(window, text="Enter IP Address:")
ip_label.pack()

ip_entry = tk.Entry(window)
ip_entry.pack()

output_text = ScrolledText(window, height=20, width=50)
output_text.pack()

scan_button = tk.Button(window, text="Scan", command=scan_button_click, height=10)
scan_button.pack()

window.mainloop()
