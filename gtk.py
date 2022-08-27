import gi

from script.Printer import Printer

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

from script.gui.Numpad import Numpad
from script.gui.QuantitySelector import QuantitySelector
from script.Configuration import Configuration
from script.Database import Database
from script.Barcode import generate_barcode
import os
from threading import Timer
from subprocess import call


# Global variable to provide the configuration data
configuration = Configuration()


class MainWindow(Gtk.Window):

    def __init__(self):
        global configuration
        self.database = None


        Gtk.Window.__init__(
            self, title="plangarten LabelPI - 2020 Plangarten GmbH", decorated=False)

        # Read configuration file and save in global variable configuration
        configuration.read_config_from_file("./config.ini")
        self.printer = Printer(configuration)

        # Set window size to screen resolution
        self.set_default_size(800, 480)
        # Window is not resizable
        self.set_resizable(False)

        # Create central GtkGrid and add it to the window
        self.grid = Gtk.Grid(vexpand=True, hexpand=True)
        self.grid.set_column_homogeneous(True)
        self.add(self.grid)

        # Load the print button icon from the print.ong file
        print_button_image = Gtk.Image()
        print_button_image.set_from_file("./gfx/print.png")

        # Create print button and add image, add print button css class
        self.printButton = Gtk.Button(sensitive=False, image=print_button_image, vexpand=False, hexpand=False,
                                      relief=Gtk.ReliefStyle.NONE)
        self.printButton.set_image_position(Gtk.PositionType.TOP)
        self.printButton.set_always_show_image(True)
        self.printButton.get_style_context().add_class("print_button")

        # Add click event handler to print button
        self.printButton.connect("clicked", self.print_button_clicked)

        # Create numpad, center and add numpad css class
        self.numpad = Numpad(self.printButton)
        self.numpad.get_style_context().add_class("numpad")

        # Create and center QuantitySelector
        self.quantitySelector = QuantitySelector()

        # Create label for error message and assign css class error_label.
        self.errorLabel = Gtk.Label(label="Die eingegebene Nummer\nwurde nicht gefunden.",
                                    justify=Gtk.Justification.CENTER, visible=False)
        self.errorLabel.get_style_context().add_class("error_label")

        # Generate GtkBox for print button and error message
        right_box_print_error = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # Add errorLabel and print button
        right_box_print_error.add(self.printButton)
        right_box_print_error.add(self.errorLabel)


        # Create GtkBox for right column
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        box.get_style_context().add_class("right_box")
        # Add quantity selector and print button box
        box.add(self.quantitySelector)
        box.add(right_box_print_error)

        # Create shutdown button with image off.png and connect click event
        shutdown_button_image = Gtk.Image()
        shutdown_button_image.set_from_file("./gfx/off.png")
        shutdown_button = Gtk.Button(image=shutdown_button_image, relief=Gtk.ReliefStyle.NONE, halign=Gtk.Align.START)
        shutdown_button.get_style_context().add_class("shutdown_button")
        shutdown_button.connect("clicked", self.shutdown_button_clicked)

        # Load and hide Database-Failed Indicator from error.png
        self.databaseConnectionFailedImage = Gtk.Image()
        self.databaseConnectionFailedImage.set_from_file("./gfx/error.png")
        self.databaseConnectionFailedImage.get_style_context().add_class("connection_failure_image")
        self.databaseConnectionFailedImage.set_halign(Gtk.Align.END)
        self.databaseConnectionFailedImage.set_visible(False)

        # Create GtkBox for bottom row
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, expand=True)
        # Add shutdown button and database failed indicator
        bottom_box.add(shutdown_button)
        bottom_box.add(self.databaseConnectionFailedImage)

        # Add widgets to main grid
        self.grid.attach(self.numpad, 0, 0, 1, 1)
        self.grid.attach(box, 1, 0, 1, 2)
        self.grid.attach(bottom_box, 0, 2, 2, 1)

        # Load and apply css file
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("./style/" + configuration.style_active_style + "/style.css")
        Gtk.StyleContext().add_provider_for_screen(Gdk.Screen.get_default(), css_provider,
                                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def print_button_clicked(self, button):
        global configuration
        # Perform database query for current number entered in numpad
        if self.database.query_number(self.numpad.get_value()):
            # If number is in database or no database connection, generate barcode
            generate_barcode(value=self.numpad.get_value(nulled=True), callback=self.print_ready, configuration=configuration, qty=self.quantitySelector.get_value(), printer=self.printer)
            # Reset print and numpad
            self.numpad.clear_value()
            # Reset quantitySelector
            self.quantitySelector.clear_value()
        else:
            # If number not found in database show error label and hide after 3 seconds
            self.errorLabel.set_visible(True)
            Timer(3, lambda m=self.numpad.get_value(): self.hide_error_message(m)).start()

    def hide_error_message(self, value):
        self.errorLabel.set_visible(False)

    def shutdown_button_clicked(self, widget):
        # If shutdown button was clicked, the PI will shut down
        # Dependency on hostname to prevent development machine from shutting down
        if socket.gethostname() == "labelpi":
            call("sudo nohup shutdown -h now", shell=True)

    def database_connection_failed(self):
        # Called from the database system if a connection cannot be established
        # Displays the Database Failed indicator
        self.databaseConnectionFailedImage.set_visible(True)

    def print_ready(self, filename):
        print(filename)
        # Called by the printing system after the print has been spooled
        # Deletes the temporary PDF file
        #if os.path.exists(filename):
        #    os.remove(filename)

    def show_all_init(self):
        # To respect the changed visibility settings of some widgets, show_all_init is called instead of show_all
        # Shows all widgets and hides the error label and the database failed indicator again
        self.show_all()
        self.databaseConnectionFailedImage.set_visible(False)
        self.errorLabel.set_visible(False)

    def init_database(self):
        # Establishes a connection to the database
        self.database = Database(configuration, connection_failure_callback=self.database_connection_failed)


# Change current working directory to the location of the file
os.chdir("/home/pi/labelpi-sql/")

# Instantiate and display MainWindow
window = MainWindow()
window.show_all_init()
# Initialize database
window.init_database()
window.connect("destroy", Gtk.main_quit)

import socket

# Hide cursor when run on labelpi.
if socket.gethostname() == "labelpi":
    cursor = Gdk.Cursor(Gdk.CursorType.BLANK_CURSOR)
    window.get_window().set_cursor(cursor)

Gtk.main()
