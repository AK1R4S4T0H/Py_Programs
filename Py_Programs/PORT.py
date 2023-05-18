import socket
import threading
import time

target_host = input("Enter the target host: ")
port_range = input("Enter the port range (e.g., '80-100', 'common'): ")
num_threads = int(input("Enter the number of threads: "))

common_port_ranges = {
    "common": [(1, 1023)],
    "web": [(80, 80), (443, 443), (8080, 8080)],
    "ftp": [(20, 21)],
    "ssh": [(22, 22)],
    "telnet": [(23, 23)],
    "smtp": [(25, 25)],
    "dns": [(53, 53)],
    "http": [(80, 80)],
    "https": [(443, 443)],
    "mysql": [(3306, 3306)],
    "postgresql": [(5432, 5432)],
    "rdp": [(3389, 3389)],
    "vnc": [(5900, 5900)],
    "imap": [(143, 143)],
    "pop3": [(110, 110)],
    "ntp": [(123, 123)],
    "ldap": [(389, 389)],
    "snmp": [(161, 161)],
    "irc": [(6667, 6667)],
    "git": [(9418, 9418)],
    "docker": [(2375, 2375)],
    # Add more common port ranges as needed
}

if not port_range:
    port_range = "common"  # Set default to "common"

if port_range in common_port_ranges:
    ports = common_port_ranges[port_range]
else:
    start_port, end_port = map(int, port_range.split("-"))
    ports = [(start_port, end_port)]

lock = threading.Lock()
open_ports = []

def scan_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                with lock:
                    open_ports.append(port)
                service = get_service_name(port)
                print(f"Port {port} is open ({service})")
    except socket.error:
        pass

def get_service_name(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_host, port))
            if result == 0:
                service_info = sock.recv(1024).decode("utf-8")
                service_name = extract_service_name(service_info)
                if service_name != "Unknown":
                    return service_name
    except socket.error:
        pass
    
    # If service detection fails or encounters an error, use common ports dictionary
    for key, value in common_port_ranges.items():
        for port_range in value:
            if port in range(port_range[0], port_range[1] + 1):
                return key.capitalize()
    
    # If port doesn't match any common ports, return "Unknown"
    return "Unknown"
    
def extract_service_name(service_info):
    # Example 1: Extract service name from bracketed text
    match = re.search(r'\[(.*?)\]', service_info)
    if match:
        return match.group(1)
    
    # Example 2: Extract service name from specific keywords or patterns
    if "HTTP" in service_info:
        return "HTTP"
    if "HTTPS" in service_info:
        return "HTTPS"
    if "FTP" in service_info:
        return "FTP"
    if "SSH" in service_info:
        return "SSH"
    if "SMTP" in service_info:
        return "SMTP"
    if "DNS" in service_info:
        return "DNS"
    if "MySQL" in service_info:
        return "MySQL"
    # Add more specific keyword checks as needed
    
    # Example 3: Extract service name based on port number
    if service_info.startswith("Port "):
        port_number = int(service_info.split()[1])
        if port_number == 80:
            return "HTTP"
        elif port_number == 443:
            return "HTTPS"
        # Add more port-based service name checks as needed
    
    # Example 4: Check if the service matches any common port ranges
    for key, value in common_port_ranges.items():
        for port_range in value:
            start_port, end_port = port_range
            if port_number in range(start_port, end_port + 1):
                return key.capitalize()
    
    # Example 5: Default fallback for unknown service names
    return "Unknown"



start_time = time.time()

for port_range in ports:
    start_port, end_port = port_range
    threads = [threading.Thread(target=scan_port, args=(port,)) for port in range(start_port, end_port + 1)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

end_time = time.time()
scan_duration = end_time - start_time

box_width = 50

print('\u250C' + '\u2500' * (box_width - 2) + '\u2510')
print('\u2502' + f"Scan completed in {scan_duration} seconds".center(box_width - 2) + '\u2502')
print('\u2514' + '\u2500' * (box_width - 2) + '\u2518')

# Print open ports in a box
open_ports_info = ", ".join(str(port) for port in open_ports)
box_width = max(len(open_ports_info) + 4, 20)

print('\nOpen Ports:')
print('\u250C' + '\u2500' * (box_width - 2) + '\u2510')
print('\u2502' + open_ports_info.center(box_width - 2) + '\u2502')
print('\u2514' + '\u2500' * (box_width - 2) + '\u2518')

# Print detailed information for each open port
for port in open_ports:
    service = get_service_name(port)
    print('\n' + '=' * box_width)
    print(f"Port: {port}".center(box_width))
    print(f"Service: {service}".center(box_width))
    print('=' * box_width)
