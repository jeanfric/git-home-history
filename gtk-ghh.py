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
    if os.path.exists("./git-home-history"):
        return os.path.abspath("./git-home-history")
    return "git-home-history"

class GHHDialog(object):
    def __init__(self):
        self.glade_file = "gtk-ghh.glade"
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
        subprocess.Popen("%s init" % get_ghh(),
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
        subprocess.Popen("./gtk-ghh-restore.py", shell=True)

    def run_commit(self, widget):
        subprocess.Popen("./gtk-ghh-commit.py", shell=True)

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
""" % {"p" : get_ghh() })
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
