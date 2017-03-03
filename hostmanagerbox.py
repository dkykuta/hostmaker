import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from scrolltext import ScrollText
from dialog import DialogConfirmation
from activablelist import ActivableList, ActivableListRow, ScrollableActivableList, XActivableList, ActiveManager

from filemanager import FileManager

class MultiContentManager(Gtk.Box):
    def __init__(self, w=600, h=600, parent_window=None):
        Gtk.Box.__init__(self)

        self.set_size_request(w,h)

        self.fm = FileManager()
        self.my_accelerators = Gtk.AccelGroup()
        parent_window.add_accel_group(self.my_accelerators)

        self.scrolltext = ScrollText(w=w*2/3, h=500)
        self.scrolllist = XActivableList(w=w/3, h=500)
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
        self.innerupperbox.pack_start(self.scrolltext, True, True, 5)

        self.innerlowerbox.pack_start(self.button_save, False, True, 15)
        self.innerlowerbox.pack_start(self.button_save_all, False, True, 15)
        self.innerlowerbox.pack_end(self.button_apply_hosts, False, True, 15)

        self.outterbox.pack_start(self.innerupperbox, True, True, 0)
        self.outterbox.pack_start(self.innerlowerbox, False, True, 0)

        self.add(self.outterbox)

        hosts_files = self.fm.list_files() 
        for f in hosts_files:
            content = self.fm.load_content(f) or ''
            self.scrolllist.addRow(f, content)

        for act in FileManager().get_actives():
            ActiveManager().activate(act)

        enabled_hosts = ""
        for row in self.scrolllist.get_enabled_rows():
            enabled_hosts = "%s%s\n" % (enabled_hosts, row.label_text)
        FileManager().set_actives(enabled_hosts)

        self.add_accelerator(self.button_save, "<Control>s", signal="clicked")
        self.add_accelerator(self.button_save_all, "<Control><Shift>s", signal="clicked")

    def change_row(self, someobj, row):
        color="purple"
        if row in self.scrolllist.get_enabled_rows():
            print "OON"
            color="green"
        else:
            print "OOFF"
            color="red"
        if row:
            self.scrolltext.set_buffer(row.text_buffer, color)

    def save(self, button):
        self.scrolllist.apply_selected_row(ActivableListRow.checkpoint)
        print('save')

    def save_all(self, button):
        self.scrolllist.apply_all_rows(ActivableListRow.checkpoint)
        print('save all')

    def apply_hosts(self, button):
        print('apply hosts')
        self.save_all(button)
        msg = "Deseja aplicar o host montado por:\n"
        enabled_hosts = ""
        for row in self.scrolllist.get_enabled_rows():
            enabled_hosts = "%s%s\n" % (enabled_hosts, row.label_text)
            msg = "%s - %s\n" % (msg, row.label_text)
        FileManager().set_actives(enabled_hosts)

        dialog = DialogConfirmation(msg)
        response = dialog.run()

        try:
            if response == Gtk.ResponseType.OK:
                hosts_content = "#################\n##  AUTOHOSTS  ##\n#################\n\n"
                for row in self.scrolllist.get_enabled_rows():
                    hosts_content = "%s# from %s\n%s\n\n" % (hosts_content, row.label_text, row.get_text().strip())
                hosts_content = hosts_content.strip()
                FileManager().save_etc_hosts(hosts_content)
            elif response == Gtk.ResponseType.CANCEL:
                print("cancel")
            dialog.destroy()
        except:
            dialog.destroy()
            errord = DialogConfirmation("An error occurred")
            response = errord.run()
            errord.destroy()


    def add_accelerator(self, widget, accelerator, signal):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            key, mod = Gtk.accelerator_parse(accelerator)
            widget.add_accelerator(signal, self.my_accelerators, key, mod, Gtk.AccelFlags.VISIBLE)
            print "The accelerator is well added with the signal " + signal
