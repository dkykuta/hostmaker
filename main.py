#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from scrolltext import ScrollText
from activablelist import ActivableList, ScrollableActivableList
import os

from hostmanagerbox import MultiContentManager
from dialog import DialogConfirmation

from filemanager import FileManager

class MainWindow:

    def delete_event(self, widget, event, data=None):
        print("delete event occurred")
        return False

    def destroy(self, widget, data=None):
        print("destroy signal occurred")
        Gtk.main_quit()

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("HostMAKER")
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.manager = MultiContentManager(parent_window=self.window, w=800)
        self.window.add(self.manager)

        self.window.show_all()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    if os.geteuid() != 0:
        dialog = DialogConfirmation("Run as root")
        dialog.run()
        exit("You need to be root")
    maindir = '/var/lib/hostmaker'
    data_dir = "%s/data" % (maindir)
    act_file = "%s/active_hosts" % (maindir)
    fm = FileManager()
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    if not os.path.exists(act_file):
        open(act_file, 'a').close()
    fm.set_data_dir(data_dir)
    fm.set_actives_file(act_file)
    mw = MainWindow()
    mw.main()
