import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk


class QuantitySelector(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

        self.value = 1

        minus_button = Gtk.Button(label="-", relief=Gtk.ReliefStyle.NONE)
        minus_button.get_style_context().add_class("quantity_selector_button")
        minus_button.connect("clicked", self.minus_button_clicked)
        self.outputLabel = Gtk.Label(label=str(self.value))
        self.outputLabel.get_style_context().add_class("quantity_selector_label")
        plus_button = Gtk.Button(label="+", relief=Gtk.ReliefStyle.NONE)
        plus_button.get_style_context().add_class("quantity_selector_button")
        plus_button.connect("clicked", self.plus_button_clicked)

        self.attach(minus_button, 0, 0, 1, 1)
        self.attach(self.outputLabel, 1, 0, 1, 1)
        self.attach(plus_button, 2, 0, 1, 1)

    def minus_button_clicked(self, button):
        if self.value > 1:
            self.value -= 1
        self.refresh_output()

    def plus_button_clicked(self, button):
        self.value += 1
        self.refresh_output()

    def refresh_output(self):
        self.outputLabel.set_label(str(self.value))

    def get_value(self):
        return self.value
    def clear_value(self):
        self.value = 1
        self.refresh_output()
