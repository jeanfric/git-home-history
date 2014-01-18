#!/usr/bin/env python
#
# Copyright (c) 2007 Jean-Francois Richard
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import ghh

import gobject
import gtk
import gtk.glade
import os
import os.path
import pygtk
import signal
import subprocess
import sys
import vte

class GHHCommitDialog(object):
    def __init__(self):
        self.glade_file = os.path.join(ghh.defs.DATA_DIR,
                                       "ghh/glade/gtk-ghh-commit.glade")
        self.widgets = gtk.glade.XML(self.glade_file)
        signal_handlers = {
            "gtk_main_quit" : gtk.main_quit,
            "kill_command" : self.kill_command
            }
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
        self.cmd_pid = None
        self.run_command_source = gobject.idle_add(self.run_command,
                                                   "%s commit" %
                                                   os.path.join(ghh.defs.BIN_DIR,
                                                                "git-home-history"))

    def _restore_normal_state(self):
        self.widgets.get_widget("stop_button").set_sensitive(False)
        self.widgets.get_widget("close_button").set_sensitive(True)
        gobject.source_remove(self.progress_source)
        self.widgets.get_widget("progressbar").set_fraction(1.00)
        self.widgets.get_widget("label").set_text("You can now close this window.")

    def kill_command(self, widget):
        if self.cmd_pid != None:
            os.kill(self.cmd_pid, signal.SIGTERM)
            self.terminal.feed("\n\nThe operation was stopped.\n\r")
            # it will in turn callback "child-exited"

    def pulse_progressbar(self):
         self.widgets.get_widget("progressbar").pulse()
         return True

    def run_command(self, to_exec):
        gobject.source_remove(self.run_command_source)
        self.progress_source = gobject.timeout_add(100, self.pulse_progressbar)

        self.widgets.get_widget("close_button").set_sensitive(False)
        self.widgets.get_widget("stop_button").set_sensitive(True)

        command = to_exec.split(' ')
        self.terminal.connect('child-exited', self.run_command_done)
        self.cmd_pid = self.terminal.fork_command(command=command[0], argv=command)
        #self.cmd_pid = self.terminal.fork_command(command="yes", argv="yes")

        # error from fork_command
        if self.cmd_pid < 0:
            print "fork exited with %s" % self.cmd_pid
            self.run_command_done(None)

    def run_command_done(self, widget):
        self._restore_normal_state()
        self.cmd_pid = None

def main():
    gtk.main()

if __name__ == "__main__":
    os.chdir(os.path.expanduser('~'))
    g = GHHCommitDialog()
    main()
