import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2, Gdk

class BrowserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Web Browser")
        self.set_default_size(800, 600)

        # CSS styling
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(bytes('''
        #toolbar {
            background-color: #494949;
            border-top: 1px solid #165753;

        }

        #toolbar:hover {
            background-color: #595959;
        }

        #entry {
            background-color: #696969;
            border: 1px solid #165753;
            padding: 2px;
            transition: background-color 0.3s ease-in-out;
        }

        #entry:hover {
            background-color: #698989;
        }

        #backButton,
        #forwardButton,
        #refreshButton,
        #inputButton {
            background-color: #DFDFDF;
            border: 1px solid #165753;
            border-radius: 5px;
            padding: 5px;
        }

        #backButton:hover,
        #forwardButton:hover,
        #refreshButton:hover,
        #inputButton:hover {
            background-color: #367773;
            border: 1px solid #468783;
        }

        #notebook {
            padding: 0;
        }

        #notebook tab {
            padding: 5px 10px;
            background: linear-gradient(to right, #00ff00, #0000ff);
        }
        ''', 'utf-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Main vertical box container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        # Notebook for tabs
        self.notebook = Gtk.Notebook()
        vbox.pack_start(self.notebook, True, True, 0)

        # Create initial tabs
        self.create_main_tab()
        self.create_tab()

        self.notebook.connect("switch-page", self.on_tab_switched)


    def create_main_tab(self):
        # Create a new web view for the main tab
        webview = WebKit2.WebView()
        webview.load_uri("https://www.youtube.com/")

        # Bottom bar container
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        bottom_bar.set_name("toolbar")

        # Entry box
        entry = Gtk.Entry()
        entry.set_name("entry")
        entry.set_text("https://www.youtube.com/")
        entry.connect("activate", self.on_entry_activated)
        bottom_bar.pack_start(entry, True, True, 0)

        # Buttons
        back_button = Gtk.Button(label="Back")
        back_button.set_name("backButton")
        back_button.connect("clicked", self.on_back_button_clicked)
        bottom_bar.pack_start(back_button, False, False, 0)

        forward_button = Gtk.Button(label="Forward")
        forward_button.set_name("forwardButton")
        forward_button.connect("clicked", self.on_forward_button_clicked)
        bottom_bar.pack_start(forward_button, False, False, 0)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.set_name("refreshButton")
        refresh_button.connect("clicked", self.on_refresh_button_clicked)
        bottom_bar.pack_start(refresh_button, False, False, 0)

        input_button = Gtk.Button(label="Go")
        input_button.set_name("inputButton")
        input_button.connect("clicked", self.on_input_button_clicked)
        bottom_bar.pack_start(input_button, False, False, 0)

        # Vertical box container for web view and bottom bar
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(webview, True, True, 0)
        vbox.pack_start(bottom_bar, False, False, 0)

        # Add the vertical box container to the notebook
        self.notebook.append_page(vbox, Gtk.Label(label="Main Tab"))
        

        # Connect the title changed signal
        webview.connect("load-changed", self.on_title_changed)

    def create_tab(self):
        # Create a new web view for the tab
        webview = WebKit2.WebView()

        # Bottom bar container
        bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        bottom_bar.set_name("toolbar")

        # Entry box
        entry = Gtk.Entry()
        entry.set_name("entry")
        entry.connect("activate", self.on_entry_activated)
        bottom_bar.pack_start(entry, True, True, 0)

        # Buttons
        back_button = Gtk.Button(label="Back")
        back_button.set_name("backButton")
        back_button.connect("clicked", self.on_back_button_clicked)
        bottom_bar.pack_start(back_button, False, False, 0)

        forward_button = Gtk.Button(label="Forward")
        forward_button.set_name("forwardButton")
        forward_button.connect("clicked", self.on_forward_button_clicked)
        bottom_bar.pack_start(forward_button, False, False, 0)

        refresh_button = Gtk.Button(label="Refresh")
        refresh_button.set_name("refreshButton")
        refresh_button.connect("clicked", self.on_refresh_button_clicked)
        bottom_bar.pack_start(refresh_button, False, False, 0)

        input_button = Gtk.Button(label="Go")
        input_button.set_name("inputButton")
        input_button.connect("clicked", self.on_input_button_clicked)
        bottom_bar.pack_start(input_button, False, False, 0)

        # Vertical box container for web view and bottom bar
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(webview, True, True, 0)
        vbox.pack_start(bottom_bar, False, False, 0)

        # Add the vertical box container to the notebook
        self.notebook.insert_page(vbox, Gtk.Label(label="New Tab"), +1)

        # Connect the title changed signal
        webview.connect("load-changed", self.on_title_changed)


    def on_tab_switched(self, notebook, current_page, _):
        if current_page == self.notebook.get_n_pages() - 1:
            self.create_tab()


    def on_entry_activated(self, entry):
        # Get the active tab's web view and load the entered URL
        page_num = self.notebook.get_current_page()
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        url = entry.get_text()
        webview.load_uri(url)

    def on_back_button_clicked(self, button):
        # Get the active tab's web view and navigate back
        page_num = self.notebook.get_current_page()
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        webview.go_back()

    def on_forward_button_clicked(self, button):
        # Get the active tab's web view and navigate forward
        page_num = self.notebook.get_current_page()
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        webview.go_forward()

    def on_refresh_button_clicked(self, button):
        # Get the active tab's web view and refresh the page
        page_num = self.notebook.get_current_page()
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        webview.reload()

    def on_input_button_clicked(self, button):
        # Get the active tab's web view and load the entered URL
        page_num = self.notebook.get_current_page()
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        entry = vbox.get_children()[1].get_children()[0]
        url = entry.get_text()
        webview.load_uri(url)

    def on_title_changed(self, webview, event):
        # Get the active tab's label and update it with the website title
        page_num = self.notebook.get_current_page()
        label = self.notebook.get_tab_label(self.notebook.get_nth_page(page_num))
        vbox = self.notebook.get_nth_page(page_num)
        webview = vbox.get_children()[0]
        title = webview.get_title()
        label.set_text(title)

if __name__ == "__main__":
    win = BrowserWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
