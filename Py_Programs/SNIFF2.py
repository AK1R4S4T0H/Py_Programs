import socket
import struct
import os
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit

class PacketSnifferThread(QThread):
    packet_received = Signal(str)

    def run(self):
        # Check if the script is running with root privileges
        if os.geteuid() != 0:
            self.packet_received.emit("Please run the script as sudo or root.")
            return

        connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        while True:
            raw_data, addr = connection.recvfrom(65535)
            dest_mac, src_mac, eth_type = parse_ethernet_header(raw_data)
            if eth_type == 0x0800:  # IPv4
                version, header_length, ttl, protocol, src_ip, dest_ip = parse_ip_header(raw_data[14:])
                if protocol == 6:  # TCP
                    src_port, dest_port, sequence, acknowledgment, offset, flags = parse_tcp_header(raw_data[14 + header_length:])
                    packet_info = f"Source MAC: {src_mac}, Destination MAC: {dest_mac}\n" \
                                  f"Source IP: {src_ip}, Destination IP: {dest_ip}\n" \
                                  f"Source Port: {src_port}, Destination Port: {dest_port}\n" \
                                  "------------------------------------------------------"
                    self.packet_received.emit(packet_info)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Packet Sniffer")
        self.setGeometry(100, 100, 600, 400)

        self.text_area = QTextEdit(self)
        self.setCentralWidget(self.text_area)

        self.sniffer_thread = PacketSnifferThread()
        self.sniffer_thread.packet_received.connect(self.update_packet_info)
        self.sniffer_thread.start()

    def update_packet_info(self, packet_info):
        self.text_area.append(packet_info)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
