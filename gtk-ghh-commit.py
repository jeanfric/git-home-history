#!/usr/bin/env python

import gobject
import gtk
import gtk.glade
import os
import os.path
import pygtk
import subprocess
import sys
import vte

def get_ghh():
    return "git-home-history"
#    return os.path.abspath(os.path.join(sys.path[0], "git-home-history"))

class GHHCommitDialog(object):
    def __init__(self):
        self.glade_file = "gtk-ghh-commit.glade"
        self.widgets = gtk.glade.XML(self.glade_file)
        signal_handlers = { "gtk_main_quit" : gtk.main_quit }
        self.widgets.signal_autoconnect(signal_handlers)

        self.terminal = vte.Terminal()
        vscrollbar = gtk.VScrollbar()
        vscrollbar.set_adjustment(self.terminal.get_adjustment())
        self.terminal.set_scrollback_lines(512)
        self.terminal.set_scroll_on_output(True)

        thbox = self.widgets.get_widget("hbox")
        thbox.pack_start(self.terminal, False, False)
        thbox.pack_start(vscrollbar)

        self.widgets.get_widget("dialog").show_all()

        self.run_command_source = gobject.idle_add(self.run_command, "%s commit" % get_ghh())

    def run_command(self, to_exec):
        self.widgets.get_widget("close_button").set_sensitive(False)
        gobject.source_remove(self.run_command_source)
        command = to_exec.split(' ')
        self.terminal.connect('child-exited', self.run_command_done)
        self.terminal.fork_command(command=command[0], argv=command)
        # don't call me again, GTK!
        return False

    def run_command_done(self, widget):
        self.widgets.get_widget("close_button").set_sensitive(True)
        self.terminal.feed("\n\nThe operation has terminated.")

def main():
    gtk.main()

if __name__ == "__main__":
    g = GHHCommitDialog()
    main()
