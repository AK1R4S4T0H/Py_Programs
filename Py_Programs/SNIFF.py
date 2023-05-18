""" Created by: AK1R4S4T0H
"""
import socket
import struct
import os

def parse_ethernet_header(data):
    dest_mac, src_mac, eth_type = struct.unpack('!6s6sH', data[:14])
    return format_mac_address(dest_mac), format_mac_address(src_mac), socket.htons(eth_type)


def format_mac_address(mac):
    return ':'.join('{:02x}'.format(byte) for byte in mac)

def parse_ip_header(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 0xF) * 4
    ttl, protocol, src_ip, dest_ip = struct.unpack('!8x B B 2x 4s 4s', data[:20])
    return version, header_length, ttl, protocol, format_ip_address(src_ip), format_ip_address(dest_ip)

def format_ip_address(ip):
    return '.'.join(str(byte) for byte in ip)

def parse_tcp_header(data):
    src_port, dest_port, sequence, acknowledgment, offset_reserved_flags = struct.unpack('!HHIIBH', data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flags = offset_reserved_flags & 0x1FF
    return src_port, dest_port, sequence, acknowledgment, offset, flags

def sniff_packets():
    # Check if the script is running with root privileges
    if os.geteuid() != 0:
        print("Please run the script as sudo or root.")
        return

    connection = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while True:
        raw_data, addr = connection.recvfrom(65535)
        dest_mac, src_mac, eth_type = parse_ethernet_header(raw_data)
        if eth_type == 0x0800:  # IPv4
            version, header_length, ttl, protocol, src_ip, dest_ip = parse_ip_header(raw_data[14:])
            if protocol == 6:  # TCP
                src_port, dest_port, sequence, acknowledgment, offset, flags = parse_tcp_header(raw_data[14 + header_length:])
                print(f"Source MAC: {src_mac}, Destination MAC: {dest_mac}")
                print(f"Source IP: {src_ip}, Destination IP: {dest_ip}")
                print(f"Source Port: {src_port}, Destination Port: {dest_port}")
                print("------------------------------------------------------")

sniff_packets()
