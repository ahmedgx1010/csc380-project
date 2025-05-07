import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow:
    def __init__(self):
        # Load the Glade file
        builder = Gtk.Builder()
        builder.add_from_file("interface.glade")

        # Get the main window from the Glade file
        self.window = builder.get_object("main_window")
        if not self.window:
            raise Exception("Could not find 'main_window' in interface.glade")
        self.window.set_default_size(800, 600)

        # Connect signals
        builder.connect_signals(self)

        # Show the window
        self.window.show_all()

    def on_destroy(self, *args):
        Gtk.main_quit()

def main():
    app = MainWindow()
    Gtk.main()

if __name__ == "__main__":
    main()