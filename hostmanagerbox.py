import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from scrolltext import ScrollText
from activablelist import ActivableList, ActivableListRow, ScrollableActivableList

class MultiContentManager(Gtk.Box):
    def __init__(self, w=600, h=600):
        Gtk.Container.__init__(self)
        self.set_size_request(w,h)

        self.scrolltext = ScrollText(w=w*2/3, h=500)
        self.scrolllist = ScrollableActivableList(w=w/3, h=500)
        self.outterbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing = 5)
        self.innerupperbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 10)
        self.innerlowerbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 10)

        self.button_save = Gtk.Button.new_with_label("Save")
        self.button_save_all = Gtk.Button.new_with_label("Save All")
        self.button_apply_hosts = Gtk.Button.new_with_label("Apply Hosts")
        self.button_save.connect('clicked', self.save)
        self.button_save_all.connect('clicked', self.save_all)
        self.button_apply_hosts.connect('clicked', self.apply_hosts)

        self.scrolllist.connect_row_selected(self.change_row)
    
        self.innerupperbox.pack_start(self.scrolllist, False, True, 5)
        self.innerupperbox.pack_start(self.scrolltext, False, True, 5)

        self.innerlowerbox.pack_start(self.button_save, False, True, 15)
        self.innerlowerbox.pack_start(self.button_save_all, False, True, 15)
        self.innerlowerbox.pack_end(self.button_apply_hosts, False, True, 15)

        self.outterbox.pack_start(self.innerupperbox, True, True, 0)
        self.outterbox.pack_start(self.innerlowerbox, False, True, 0)

        self.add(self.outterbox)

        for i in range(30):
            self.scrolllist.addRow("line %s" % i)

    def change_row(self, someobj, row):
        if row:
            self.scrolltext.set_buffer(row.text_buffer)

    def save(self, button):
        self.scrolllist.apply_selected_row(ActivableListRow.checkpoint)
        print('save')

    def save_all(self, button):
        self.scrolllist.apply_all_rows(ActivableListRow.checkpoint)
        print('save all')

    def apply_hosts(self, button):
        print('apply hosts')
