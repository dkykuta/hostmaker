#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from hmaker.scrolltext import ScrollText
from hmaker.activablelist import ActivableList, ScrollableActivableList

from hmaker.hostmanagerbox import MultiContentManager

from hmaker.filemanager import FileManager

class MainWindow:

    def delete_event(self, widget, event, data=None):
        print("delete event occurred")
        return False

    def destroy(self, widget, data=None):
        print("destroy signal occurred")
        Gtk.main_quit()

    def __init__(self):
        self.window = Gtk.Window()
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.manager = MultiContentManager(parent_window=self.window)
        self.window.add(self.manager)

        self.window.show_all()

    def main(self):
        Gtk.main()

def main():
    fm = FileManager()
    fm.set_data_dir('/tmp/hosts')
    fm.set_actives_file('/tmp/actives_hosts')
    mw = MainWindow()
    mw.main()
