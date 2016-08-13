import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ActivableListRow(Gtk.ListBoxRow):
    def __init__(self, label_text):
        Gtk.ListBoxRow.__init__(self)
        self.label_text = label_text
        self.label = Gtk.Label(label_text, xalign=0)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.add(self.hbox)
        self.hbox.pack_start(self.label, False, True, 0)

        self.text_buffer = Gtk.TextBuffer()
        row_content = label_text # file content
        self.text_buffer.set_text(row_content)
        self.checkpoint()
        self.text_buffer.connect('changed', self.update_label)

        self.switch = Gtk.Switch()
        self.switch.props.valign = Gtk.Align.CENTER
        self.hbox.pack_end(self.switch, False, True, 0)

    def checkpoint(self):
        self.text_buffer.set_modified(False)
        self.update_label()

    def update_label(self, something=None):
        if self.text_buffer.get_modified():
            self.label.set_text("* %s" % (self.label_text))
        else:
            self.label.set_text(self.label_text)

class ScrollableActivableList(Gtk.ScrolledWindow):
    def __init__(self, hadjustment=None, vadjustment=None, w=300, h=350):
        Gtk.ScrolledWindow.__init__(self, hadjustment, vadjustment)
        self.act_list = ActivableList(w, h)
        self.set_size_request(w, h)
        self.add(self.act_list)
        self.nrows = 0

    def addRow(self, row_label_text):
        self.act_list.addRow(row_label_text)
        self.nrows += 1

    def connect_row_selected(self, method):
        self.act_list.connect('row-selected', method)

    def apply_selected_row(self, method):
        method(self.act_list.get_selected_row())

    def apply_all_rows(self, method):
        for i in range(self.nrows):
            method(self.act_list.get_row_at_index(i))

class ActivableList(Gtk.ListBox):
    def __init__(self, w=300, h=350):
        Gtk.ListBox.__init__(self)
        self.set_size_request(w, h)
    def addRow(self, row_label_text):
        self.add(ActivableListRow(row_label_text))
