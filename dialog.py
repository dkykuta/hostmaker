import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import uuid

class DialogConfirmation(Gtk.Dialog):
    def __init__(self, conf_text=None):
        Gtk.Dialog.__init__(self, "Confirmation", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        self.label = Gtk.Label(conf_text or "Are you sure?")

        self.box = self.get_content_area()
        self.box.add(self.label)
        self.show_all()



class DialogEntry(Gtk.MessageDialog):
    def __init__(self, ask_text=None):
        Gtk.Dialog.__init__(self, "Enter info", None, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(250, 200)

        self.label = Gtk.Label(ask_text or "Enter the info")
        self.entry = Gtk.Entry()

        self.entry.connect("activate", 
                      lambda ent, dlg, resp: dlg.response(resp), 
                      self, Gtk.ResponseType.OK)

        self.box = self.get_content_area()
        self.box.add(self.label)
        self.box.add(self.entry)
        self.show_all()

    def get_response_text(self):
        return self.entry.get_text()
