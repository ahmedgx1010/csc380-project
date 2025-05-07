import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib

class Main:
    def __init__(self):
        # Load the Glade file
        gladeFile = "main.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladeFile)

        # Get the main window from the Glade file
        window = self.builder.get_object("main_window")
        window.connect("delete-event", gtk.main_quit)

        # Connect signals
        self.builder.connect_signals(self)

        # Show the window
        window.show_all()


if __name__ == "__main__":
    main = Main()
    gtk.main()