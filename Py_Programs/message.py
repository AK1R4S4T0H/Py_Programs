from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

from cryptography.fernet import Fernet
import socket
import threading
import random
import http.server
import socketserver
import netifaces

# Generate a random encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""


class ChatApp(App):
    def __init__(self, **kwargs):
        super(ChatApp, self).__init__(**kwargs)
        self.message_log = []
        self.receiver_ip = ""
        self.receiver_port = 12345
        self.connection_status = "Disconnected"
        self.http_server_thread = None
        self.http_server_port = None

    def build(self):
        Window.size = (400, 600)
        layout = BoxLayout(orientation='vertical')

        # IP address dropdown
        self.ip_dropdown = DropDown()
        ip_addresses = self.get_local_ip_addresses()
        for ip_address in ip_addresses:
            btn = Button(text=ip_address, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_ip_address(btn.text))
            self.ip_dropdown.add_widget(btn)

        # Manually enter IP option
        manual_ip_option = Button(text="Enter IP Manually", size_hint_y=None, height=44)
        manual_ip_option.bind(on_release=self.open_manual_ip_popup)
        self.ip_dropdown.add_widget(manual_ip_option)

        # IP address button
        ip_button = Button(text='Select IP Address', size_hint=(1, None), height=50)
        ip_button.bind(on_release=self.ip_dropdown.open)
        layout.add_widget(ip_button)

        # IP address label
        self.ip_label = Label(text="Selected IP: ", size_hint=(1, 0.1))
        layout.add_widget(self.ip_label)

        # Port input
        self.port_input = TextInput(text=str(self.receiver_port), size_hint=(1, 0.1), multiline=False, readonly=False)
        layout.add_widget(self.port_input)

        # Connection status progress bar
        self.progress_bar = ProgressBar(max=1.0, size_hint=(1, None), height=20)
        self.progress_bar.value = 0.0
        layout.add_widget(self.progress_bar)

        # Message log
        scroll_view = ScrollView()
        self.message_label = Label(text='\n'.join(self.message_log), valign='top', text_size=(Window.width - 20, None))
        scroll_view.add_widget(self.message_label)
        layout.add_widget(scroll_view)

        # Message input
        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False, readonly=False)
        layout.add_widget(self.message_input)

        # Send button
        send_button = Button(text='Send', size_hint=(1, 0.1))
        send_button.bind(on_release=self.send_message)
        layout.add_widget(send_button)

        # HTTP server button
        http_server_button = Button(text='Start HTTP Server', size_hint=(1, 0.1))
        http_server_button.bind(on_release=self.start_http_server)
        layout.add_widget(http_server_button)

        # Update port button
        update_port_button = Button(text='Update Port', size_hint=(1, 0.1))
        update_port_button.bind(on_release=self.update_port)
        layout.add_widget(update_port_button)

        return layout

    def get_local_ip_addresses(self):
        addresses = []
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            ifaddresses = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in ifaddresses:
                for link in ifaddresses[netifaces.AF_INET]:
                    addresses.append(link['addr'])
        return addresses

    def select_ip_address(self, ip_address):
        if ip_address == "Enter IP Manually":
            self.open_manual_ip_popup()
        else:
            self.receiver_ip = ip_address
            self.ip_label.text = f"Selected IP: {self.receiver_ip}"

        self.ip_dropdown.dismiss()

    def open_manual_ip_popup(self, *args):
        from kivy.uix.popup import Popup

        popup_layout = BoxLayout(orientation='vertical', padding=10)

        ip_input = TextInput(text="", multiline=False)
        popup_layout.add_widget(ip_input)

        submit_button = Button(text="Submit", size_hint=(1, None), height=40)
        submit_button.bind(on_release=lambda btn: self.select_ip_address(ip_input.text))
        popup_layout.add_widget(submit_button)

        popup = Popup(title="Enter IP Address", content=popup_layout, size_hint=(0.6, 0.3))
        popup.open()

    def send_message(self, instance):
        message = self.message_input.text
        self.message_input.text = ''

        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(message.encode()).decode()

        # Add the message to the log
        self.message_log.append(f"You: {message}")
        self.message_log.append(f"Encrypted: {encrypted_message}")
        self.message_label.text = '\n'.join(self.message_log)

        # Send the encrypted message to the receiver
        self.send_encrypted_message(encrypted_message)

    def send_encrypted_message(self, encrypted_message):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.receiver_ip, self.receiver_port)

        try:
            # Connect to the receiver's IP address and port
            sock.connect(server_address)

            # Send the encrypted message
            sock.sendall(encrypted_message.encode())

            # Update connection status
            self.connection_status = "Connected"
            self.progress_bar.value = 1.0
        except ConnectionRefusedError:
            # Update connection status
            self.connection_status = "Disconnected"
            self.progress_bar.value = 0.0
        finally:
            # Close the socket connection
            sock.close()

    def update_connection_status(self, dt):
        self.ip_label.text = f"Selected IP: {self.receiver_ip} | Port: {self.receiver_port} | Status: {self.connection_status}"

    def start_http_server(self, instance):
        if self.http_server_thread is None or not self.http_server_thread.is_alive():
            self.receiver_port = self.get_random_port()
            self.http_server_port = self.receiver_port

            self.http_server_thread = threading.Thread(target=self.run_http_server, daemon=True)
            self.http_server_thread.start()

            self.connection_status = "Connected"
            Clock.schedule_interval(self.update_connection_status, 1.0)
        else:
            self.connection_status = "Disconnected"

    def run_http_server(self):
        server_address = ('', self.http_server_port)
        httpd = ThreadedHTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()

    def update_port(self, instance):
        new_port = self.port_input.text
        if new_port.isdigit():
            self.receiver_port = int(new_port)
            self.connection_status = "Disconnected"
            self.progress_bar.value = 0.0
        else:
            self.port_input.text = str(self.receiver_port)

    def get_random_port(self):
        return random.randint(49152, 65535)


if __name__ == '__main__':
    ChatApp().run()

