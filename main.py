#!/usr/bin/env python

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from scrolltext import ScrollText
from activablelist import ActivableList, ScrollableActivableList

from hostmanagerbox import MultiContentManager

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

        self.manager = MultiContentManager("/tmp/hosts")
        self.window.add(self.manager)

        self.window.show_all()

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    mw = MainWindow()
    mw.main()
