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
import tempfile
import time

class GHHRestorer(object):
    def __init__(self):
        self.glade_file = os.path.join(ghh.defs.DATA_DIR,
                                       "ghh/glade/gtk-ghh-restore.glade")
        self.widgets = gtk.glade.XML(self.glade_file)
        signal_handlers = {
            "gtk_main_quit" : gtk.main_quit,
            "restart_refresh_file_list" : self.restart_refresh_file_list,
            "output_files" : self.output_files
            }
        self.widgets.signal_autoconnect(signal_handlers)

        self.liststore = gtk.ListStore(gobject.TYPE_BOOLEAN, gobject.TYPE_STRING)
        self.widgets.get_widget("treeview").set_model(self.liststore)

        toggle_renderer = gtk.CellRendererToggle()
        toggle_renderer.set_property('activatable', True)
        toggle_renderer.connect('toggled', self.file_toggled, self.liststore)
        tvcolumn1 = gtk.TreeViewColumn(None, toggle_renderer)
        tvcolumn1.add_attribute(toggle_renderer, 'active', 0)
        tvcolumn1.set_resizable(True)

        text_renderer = gtk.CellRendererText()
        tvcolumn2 = gtk.TreeViewColumn('Files', text_renderer)
        tvcolumn2.add_attribute(text_renderer, 'text', 1)
        tvcolumn2.set_resizable(True)

        self.widgets.get_widget("treeview").append_column(tvcolumn1)
        self.widgets.get_widget("treeview").append_column(tvcolumn2)

        self.widgets.get_widget("hentry").set_value(time.localtime().tm_hour)
        self.widgets.get_widget("mentry").set_value(time.localtime().tm_min)

        self.progress_source = None
        self.idle_id = None
        self.subprocess = None
        self.toggled_count = 0
        self.widgets.get_widget("window").show_all()
        self.restart_refresh_file_list(None)

    def file_toggled(self, widget, path, model):
        model[path][0] = not model[path][0]
        if model[path][0] == False:
            self.toggled_count = self.toggled_count - 1
            if self.toggled_count <= 0:
                self.widgets.get_widget("viewfiles_button").set_sensitive(False)
        else:
            self.toggled_count = self.toggled_count + 1
            if self.toggled_count > 0:
                self.widgets.get_widget("viewfiles_button").set_sensitive(True)

    def output_files(self, widget):
        self.widgets.get_widget("viewfiles_button").set_sensitive(False)
        self.widgets.get_widget("refresh_button").set_sensitive(False)

        # get a local copy of things that may change on the UI
        timespec_in_use = self.timespec_in_use
        files = [x[1] for x in self.liststore if x[0] == True]
        outputdir = tempfile.mkdtemp()

        self.widgets.get_widget("refresh_button").set_sensitive(True)

        self.widgets.get_widget("progressbar").set_text("Extracting files")
        self.widgets.get_widget("progressbar").set_fraction(0)

        max = len(files)
        count = 0
        for a in files:
            count = count + 1
            self.widgets.get_widget("progressbar").set_fraction(count/max)
            outputfile = "%s/%s" % (outputdir, os.path.basename(a))
            #if os.path.exists(outputfile):
            # try to keep the same suffix as the original, for
            # easy finding of the file type
            outputfile = tempfile.mkstemp(suffix = ".%s" % os.path.basename(a),
                                              dir=outputdir)[1]
            cmd = "%s show %s as of %s > %s" % (os.path.join(ghh.defs.BIN_DIR,
                                                             "git-home-history"),
                                                a,
                                                self.timespec_in_use,
                                                outputfile)
            print cmd
            subprocess.Popen(cmd, shell=True)

        self.widgets.get_widget("progressbar").set_text("Opening file manager")
        subprocess.Popen("xdg-open %s" % outputdir, shell=True)
        self.widgets.get_widget("progressbar").set_text("")
        self.widgets.get_widget("progressbar").set_fraction(0)
        self.widgets.get_widget("viewfiles_button").set_sensitive(True)

    def calendar_date_to_string(self):
        year, month, day = self.widgets.get_widget("calendar").get_date()
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        return time.strftime("%F", time.localtime(mytime))

    def pulse_progressbar(self):
        self.widgets.get_widget("progressbar").pulse()
        return True

    def stop_refresh_file_list(self):
        if self.subprocess != None and self.subprocess.poll() == None:
            # close the pipe, kill the child
            self.subprocess.stdout.close()
        if self.idle_id != None:
            gobject.source_remove(self.idle_id)
        self.subprocess = None

    def restart_refresh_file_list(self, widget):
        self.stop_refresh_file_list()
        self.liststore.clear()

        self.progress_source = gobject.timeout_add(100, self.pulse_progressbar)
        self.widgets.get_widget("progressbar").set_text("Refreshing file list")

        self.toggled_count = 0
        self.widgets.get_widget("viewfiles_button").set_sensitive(False)
        timespec = "%s %s:%s" % (self.calendar_date_to_string(),
                                 self.widgets.get_widget("hentry").get_value_as_int(),
                                 self.widgets.get_widget("mentry").get_value_as_int())
        self.timespec_in_use = timespec
        t = time.strftime("%c", time.strptime(self.timespec_in_use, "%Y-%m-%d %H:%M"))
        self.widgets.get_widget("current_list_label").set_markup("<b>%s</b>" % t)
        self.idle_id = gobject.idle_add(self.refresh_file_list, timespec)

    def refresh_file_list(self, timespec):
        if self.subprocess == None:
            print "%s ls-stored-files as of %s" % (os.path.join(ghh.defs.BIN_DIR,
                                                                "git-home-history"),
                                                   timespec)
            self.subprocess = subprocess.Popen(
                "%s ls-stored-files as of %s" % (os.path.join(ghh.defs.BIN_DIR,
                                                              "git-home-history"),
                                                 timespec),
                shell=True,
                stdout=subprocess.PIPE,
                close_fds=True)

        # Read 16 lines at a time for maximum interactivity
        for i in range(0, 16):
            line = self.subprocess.stdout.readline()
            if len(line) > 0:
                self.liststore.append([False, line.strip()])

        if len(line) == 0 and self.subprocess.poll() != None:
            gobject.source_remove(self.progress_source)
            self.widgets.get_widget("progressbar").set_text("")
            self.widgets.get_widget("progressbar").set_fraction(0)
            return False
        # not finished yet ...  call back please, until end of
        # consumption of child output
        return True



def main():
    gtk.main()

if __name__ == "__main__":
    g = GHHRestorer()
    main()
