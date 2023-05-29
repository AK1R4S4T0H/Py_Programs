import os
import sys
import gi
import pygame

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk, Pango

class Audio(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Music")
        self.set_opacity(0.75)
        self.set_default_size(333, 230)

        # CSS style provider
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b"""
            button {
                background-color: #7777EE;
                color: #FFFFFF;
            }
            button:hover {
                background-color: #DD33DD;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Main layout container
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        layout.set_margin_top(40)
        layout.set_margin_bottom(40)
        layout.set_margin_start(20)
        layout.set_margin_end(20)
        self.add(layout)

        font_desc = Pango.FontDescription("Helvetica Bold 13")

        # File label
        self.file_label = Gtk.Label(label="Please choose a song:")
        self.file_label.override_font(font_desc)
        layout.pack_start(self.file_label, False, False, 0)

        # File browse button
        self.file_button = Gtk.Button(label="Browse")
        self.file_button.connect("clicked", self.choose_file)
        self.file_button.override_font(font_desc)
        layout.pack_start(self.file_button, False, False, 0)

        # Play button
        self.play_button = Gtk.Button(label="Play")
        self.play_button.connect("clicked", self.play)
        self.play_button.override_font(font_desc)
        self.play_button.get_style_context().add_class("play-button")
        layout.pack_start(self.play_button, False, False, 0)

        # Pause button
        self.pause_button = Gtk.Button(label="Pause")
        self.pause_button.connect("clicked", self.pause)
        self.pause_button.override_font(font_desc)
        self.pause_button.get_style_context().add_class("pause-button")
        layout.pack_start(self.pause_button, False, False, 0)

        # Stop button
        self.stop_button = Gtk.Button(label="Stop")
        self.stop_button.connect("clicked", self.stop)
        self.stop_button.override_font(font_desc)
        self.stop_button.get_style_context().add_class("stop-button")
        layout.pack_start(self.stop_button, False, False, 0)

        # Volume label
        self.volume_label = Gtk.Label(label="Volume:")
        self.volume_label.override_font(font_desc)
        layout.pack_start(self.volume_label, False, False, 0)

        # Volume slider
        self.volume_slider = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 0, 100, 1
        )
        self.volume_slider.set_draw_value(False)
        self.volume_slider.connect("value-changed", self.set_volume)
        layout.pack_start(self.volume_slider, False, False, 0)

        # Variables
        self.file_path = None

        # Init pygame mixer
        pygame.mixer.init()

    def choose_file(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Choose a song",
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        dialog.set_current_folder(os.path.expanduser("~"))
        filter_audio = Gtk.FileFilter()
        filter_audio.set_name("Audio files")
        filter_audio.add_mime_type("audio/mpeg")
        dialog.add_filter(filter_audio)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_path = dialog.get_filename()
            name = os.path.basename(self.file_path)
            self.file_label.set_label("Song: " + name)

        dialog.destroy()

    def play(self, widget):
        if self.file_path:
            pygame.mixer.music.load(self.file_path)
            pygame.mixer.music.play()

    def pause(self, widget):
        pygame.mixer.music.pause()

    def stop(self, widget):
        pygame.mixer.music.stop()

    def set_volume(self, widget):
        value = self.volume_slider.get_value() / 100
        pygame.mixer.music.set_volume(value)

    def on_delete_event(self, widget, event):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Exit"
        )
        dialog.format_secondary_text("Are you sure you want to exit?")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            Gtk.main_quit()
        dialog.destroy()

if __name__ == "__main__":
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(b"""
        button.play-button:hover {
            background-color: #00DDAA;
        }
        button.pause-button:hover {
            background-color: #BBDD00;
        }
        button.stop-button:hover {
            background-color: #EE1100;
        }
    """)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    window = Audio()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
