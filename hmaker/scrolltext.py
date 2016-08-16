import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ScrollText(Gtk.ScrolledWindow):
    def __init__(self, hadjustment=None, vadjustment=None, textbuffer=None, w=300, h=550):
        Gtk.ScrolledWindow.__init__(self, hadjustment, vadjustment)
        self.textview = Gtk.TextView()
        self.textview.set_size_request(w,h)
        self.set_size_request(w,h)
        self.add(self.textview)
        if textbuffer:
            self.textview.set_buffer(text_buffer)
        else:
            self.textview.set_editable(False)
        self.textview.get_buffer().insert_at_cursor(' Select file to edit')

    def set_buffer(self, text_buffer):
        self.textview.set_editable(True)
        self.textview.set_buffer(text_buffer)
