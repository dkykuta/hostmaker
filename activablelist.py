import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dialog import DialogConfirmation, DialogEntry
from os import listdir
from os.path import isfile, join
from filemanager import FileManager

class ActiveManager:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if 'switches' not in self.__shared_state:
            self.switches = {}

    def put(self, key, value):
        self.switches[key] = value

    def activate(self, key):
        return self.set_state(key, True)

    def deactivate(self, key):
        return self.set_state(key, False)

    def set_state(self, key, value):
        if key in self.switches:
            sw = self.switches[key]
            sw.set_active(value)
            return True
        return False

class ActivableListRow(Gtk.ListBoxRow):
    def __init__(self, label_text, row_content = None):
        Gtk.ListBoxRow.__init__(self)
        self.label_text = label_text
        self.label = Gtk.Label(label_text, xalign=0)
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.add(self.hbox)
        self.hbox.pack_start(self.label, False, True, 0)

        self.text_buffer = Gtk.TextBuffer()
        self.text_buffer.set_text(row_content or '')
        self.checkpoint()
        self.text_buffer.connect('changed', self.update_label)

        self.switch = Gtk.Switch()
        ActiveManager().put(label_text, self.switch)
        self.switch.props.valign = Gtk.Align.CENTER
        self.hbox.pack_end(self.switch, False, True, 0)

    def checkpoint(self):
        self.content_text = self.text_buffer.get_text(self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), True) 
        if self.content_text and self.content_text[-1] != '\n':
            self.content_text = "%s\n" % self.content_text
        self.text_buffer.set_text(self.content_text)
        self.text_buffer.set_modified(False)
        self.update_label()
        FileManager().save_file(self.label_text, self.content_text)

    def update_label(self, something=None):
        if self.text_buffer.get_modified():
            self.label.set_text("* %s" % (self.label_text))
        else:
            self.label.set_text(self.label_text)

    def get_text(self):
        return self.content_text

class XActivableList(Gtk.Box):
    def __init__(self, hadjustment=None, vadjustment=None, w=300, h=350):
        Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing = 5)
        self.fm = FileManager()
        self.new_button = Gtk.Button.new_with_label("New")
        self.del_button = Gtk.Button.new_with_label("Delete")
        self.buttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing = 5)
        self.buttonbox.pack_start(self.new_button, False, True, 0)
        self.buttonbox.pack_end(self.del_button, False, True, 0)
        
        self.new_button.connect('clicked', self.new_clicked)
        self.del_button.connect('clicked', self.del_clicked)

        self.slist = ScrollableActivableList(hadjustment=hadjustment, vadjustment=vadjustment, w=w, h=h)

        self.pack_end(self.slist, True, True, 0)
        self.pack_end(self.buttonbox, False, True, 0)

    def new_clicked(self, button):
        dialog = DialogEntry(ask_text = "Nome do novo item de hosts")
        try:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                row_name =  dialog.get_response_text()
                print(row_name)
                self.fm.save_file(row_name, "\n")
                self.slist.addRow(row_name)
                self.slist.show_all()
            elif response == Gtk.ResponseType.CANCEL:
                print("cancel")
        except:
            pass
        dialog.destroy()

    def del_clicked(self, button):
        dialog = DialogConfirmation()
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self.slist.remove_selected_row()
        elif response == Gtk.ResponseType.CANCEL:
            print("cancel")

        dialog.destroy()

    def addRow(self, row_label_text, row_content=None):
        self.slist.addRow(row_label_text, row_content)

    def connect_row_selected(self, method):
        self.slist.connect_row_selected(method)

    def apply_selected_row(self, method):
        self.slist.apply_selected_row(method)

    def apply_all_rows(self, method):
        self.slist.apply_all_rows(method)

    def get_enabled_rows(self):
        return self.slist.get_enabled_rows() 

class ScrollableActivableList(Gtk.ScrolledWindow):
    def __init__(self, hadjustment=None, vadjustment=None, w=300, h=350):
        Gtk.ScrolledWindow.__init__(self, hadjustment, vadjustment)
        self.set_size_request(w, h)

        self.act_list = ActivableList(w, h-50)

        self.add(self.act_list)
        self.nrows = 0

    def addRow(self, row_label_text, row_content=None):
        self.act_list.addRow(row_label_text, row_content)
        self.nrows += 1

    def connect_row_selected(self, method):
        self.act_list.connect('row-selected', method)

    def apply_selected_row(self, method):
        method(self.act_list.get_selected_row())

    def get_selected_row(self):
        return self.act_list.get_selected_row()

    def remove_selected_row(self):
        row = self.act_list.get_selected_row()
        if row:
            FileManager().delete_file(row.label_text)
            self.act_list.remove_row(row)
            self.nrows -= 1
        else:
            print("Nothing selected")

    def apply_all_rows(self, method):
        for i in range(self.nrows):
            method(self.act_list.get_row_at_index(i))
    
    def get_enabled_rows(self):
        ret = []
        for i in range(self.nrows):
            row = self.act_list.get_row_at_index(i)
            if row.switch.get_active():
                ret.append(row)
        return ret

class ActivableList(Gtk.ListBox):
    def __init__(self, w=300, h=350):
        Gtk.ListBox.__init__(self)
        self.set_size_request(w, h)

    def addRow(self, row_label_text, row_content = None):
        self.add(ActivableListRow(row_label_text, row_content))

    def remove_row(self, row):
        self.remove(row)
