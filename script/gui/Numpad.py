import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ButtonEntry:
    def __init__(self, label, width, height, position_x, position_y):
        # Describes a Numpad button, its size and position
        self.label = label
        self.width = width
        self.height = height
        self.positionX = position_x
        self.positionY = position_y


class Numpad(Gtk.Grid):
    def __init__(self, print_button):
        Gtk.Grid.__init__(self)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

        self.value = ""

        self.printButton = print_button

        button_entries = [

            ButtonEntry('7', 1, 1, 0, 0),
            ButtonEntry('8', 1, 1, 1, 0),
            ButtonEntry('9', 1, 1, 2, 0),

            ButtonEntry('4', 1, 1, 0, 1),
            ButtonEntry('5', 1, 1, 1, 1),
            ButtonEntry('6', 1, 1, 2, 1),

            ButtonEntry('1', 1, 1, 0, 2),
            ButtonEntry('2', 1, 1, 1, 2),
            ButtonEntry('3', 1, 1, 2, 2),

            ButtonEntry('0', 2, 1, 0, 3),
            ButtonEntry('<', 1, 1, 2, 3),
        ]

        self.outputLabel = Gtk.Label(label="")
        self.outputLabel.get_style_context().add_class("numpad_label")
        self.outputLabel.set_margin_bottom(20)

        clear_button_image = Gtk.Image()
        clear_button_image.set_from_file("./gfx/clear.png")
        clear_button = Gtk.Button(image=clear_button_image, relief=Gtk.ReliefStyle.NONE)
        clear_button.set_always_show_image(True)

        clear_button.set_margin_bottom(20)
        clear_button.get_style_context().add_class("numpad_button")
        clear_button.connect("clicked", self.clear_button_clicked)

        self.attach(self.outputLabel, 0, 0, 2, 1)
        self.attach(clear_button, 2, 0, 1, 1)

        for buttonEntry in button_entries:

            if buttonEntry.label is "<":
                backspace_button_image = Gtk.Image()
                backspace_button_image.set_from_file("./gfx/backspace.png")
                button = Gtk.Button(image=backspace_button_image, relief=Gtk.ReliefStyle.NONE)
            else:
                button = Gtk.Button(label=buttonEntry.label, relief=Gtk.ReliefStyle.NONE)

            button.set_margin_top(1)
            button.set_margin_bottom(1)
            button.set_margin_start(1)
            button.set_margin_end(1)
            button.get_style_context().add_class("numpad_button")
            if buttonEntry.label != "<":
                button.connect("clicked",
                               lambda e, buttonEntry=buttonEntry: self.number_button_clicked(buttonEntry.label))
            else:
                button.connect("clicked", lambda e: self.backspace_button_clicked())

            self.attach(button, buttonEntry.positionX, buttonEntry.positionY + 1, buttonEntry.width, buttonEntry.height)

    def number_button_clicked(self, buttonValue):
        if len(self.value) < 5:
            self.value = self.value + str(buttonValue)

        self.refresh_output()

    def backspace_button_clicked(self):
        if len(self.value) > 0:
            self.value = self.value[:-1]
        self.refresh_output()

    def clear_button_clicked(self, button):
        self.clear_value()

    def refresh_output(self):
        self.outputLabel.set_label(self.value)
        if len(self.value) >= 3:
            self.printButton.set_sensitive(True)
        else:
            self.printButton.set_sensitive(False)

    def clear_value(self):
        self.value = ""
        self.refresh_output()

    def get_value(self, nulled=False):
        if len(self.value) > 0:
            if not nulled:
                return self.value
            else:
                val = self.value
                while (len(val) < 5):
                    val = "0" + val
                return val
        return None
