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
import subprocess
import sys
import vte

class GHHDialog(object):
    def __init__(self):
        self.glade_file = os.path.join(ghh.defs.DATA_DIR,
                                       "ghh/glade/gtk-ghh.glade")
        self.widgets = gtk.glade.XML(self.glade_file)
        signal_handlers = {
            "gtk_main_quit" : gtk.main_quit,
            "toggle_autostart" : self.toggle_autostart,
            "edit_ignores" : self.edit_ignores,
            "run_commit" : self.run_commit,
            "run_restore" : self.run_restore
            }
        self.widgets.signal_autoconnect(signal_handlers)
        # we don't want to know.
        # no.    don't try.     no.
        subprocess.Popen("%s init" % os.path.join(ghh.defs.BIN_DIR,
                                                  "git-home-history"),
                         shell=True,
                         stdout=open('/dev/null', 'w'),
                         stderr=open('/dev/null', 'w'))
        self.widgets.get_widget("dialog").show_all()

    def edit_ignores(self, widget):
        subprocess.Popen("xdg-open ~/.gitignore", shell=True)

    def toggle_autostart(self, widget):
        autostart_widget = self.widgets.get_widget("autostart_toggle")
        if autostart_widget.get_active():
            Autostart().add()
        else:
            Autostart().remove()

    def run_restore(self, widget):
        subprocess.Popen(os.path.join(ghh.defs.BIN_DIR, "gtk-ghh-restore"),
                         shell=True)

    def run_commit(self, widget):
        subprocess.Popen(os.path.join(ghh.defs.BIN_DIR, "gtk-ghh-commit"),
                         shell=True)

class Autostart(object):
    def __init__(self):
        if "KDE_FULL_SESSION" in os.environ:
            autostart_dir = os.path.expanduser("~/.kde/Autostart")
        else:
            config_home = os.environ.get('XDG_CONFIG_HOME', '~/.config')
            self.autostart_dir = os.path.join(
                os.path.expanduser(config_home),
                "autostart")
        self.destination = os.path.join (
            self.autostart_dir,
            "git-home-history.desktop")

    def is_enabled(self):
        return os.path.exists(self.destination)

    def add(self):
        if os.path.exists(self.destination):
            return
        try:
            os.makedirs(self.autostart_dir)
        except:
            pass
        try:
            f = open(self.destination, "w")
            f.write(
"""[Desktop Entry]
Version=1.0
Type=Application
Name=git-home-history
TryExec=%(p)s
Exec=nice %(p)s private--init-and-commit
""" % {"p" : os.path.join(ghh.defs.BIN_DIR, "git-home-history") })
            f.close()
        except:
            pass

    def remove(self):
        if not os.path.exists(self.destination):
            return
        try:
            os.remove (self.destination)
            os.removedirs(self.autostart_dir)
        except:
            pass


def main():
    gtk.main()

if __name__ == "__main__":
    g = GHHDialog()
    main()
