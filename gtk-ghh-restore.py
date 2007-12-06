#!/usr/bin/env python

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

def get_ghh():
    return "git-home-history"
#    return os.path.abspath(os.path.join(sys.path[0], "git-home-history"))

class GHHRestorer(object):
    def __init__(self):
        self.glade_file = "gtk-ghh-restore.glade"
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

        self.idle_id = None
        self.subprocess = None

        self.widgets.get_widget("window").show_all()

    def file_toggled(self, widget, path, model):
        model[path][0] = not model[path][0]
        return

    def output_files(self, widget):
        outputdir = tempfile.mkdtemp()
        for a in [x[1] for x in self.liststore if x[0] == True]:
            outputfile = "%s/%s" % (outputdir, os.path.basename(a))
            if os.path.exists(outputfile):
                outputfile = tempfile.mkstemp(prefix = "%s." % os.path.basename(a),
                                              dir=outputdir)[1]
            cmd = "%s show %s as of %s > %s" % (get_ghh(),
                                                a,
                                                self.timespec_in_use,
                                                outputfile)
            print cmd
            subprocess.Popen(cmd, shell=True)
        subprocess.Popen("xdg-open %s" % outputdir, shell=True)
        gtk.main_quit()

    def calendar_date_to_string(self):
        year, month, day = self.widgets.get_widget("calendar").get_date()
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        return time.strftime("%F", time.localtime(mytime))


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
        timespec = "%s %s:%s" % (self.calendar_date_to_string(),
                                 self.widgets.get_widget("hentry").get_value_as_int(),
                                 self.widgets.get_widget("mentry").get_value_as_int())
        self.timespec_in_use = timespec
        self.idle_id = gobject.idle_add(self.refresh_file_list, timespec)

    def refresh_file_list(self, timespec):
        if self.subprocess == None:
            print "%s ls-stored-files as of %s" % (get_ghh(), timespec)
            self.subprocess = subprocess.Popen(
                "%s ls-stored-files as of %s" % (get_ghh(), timespec),
                shell=True,
                stdout=subprocess.PIPE,
                close_fds=True)

        # Read 16 lines at a time for maximum interactivity
        for i in range(0, 16):
            line = self.subprocess.stdout.readline()
            if len(line) > 0:
                self.liststore.append([False, line.strip()])

        if len(line) == 0 and self.subprocess.poll() != None:
            return False
        # not finished yet ...  call back please, until end of
        # consumption of child output
        return True



def main():
    gtk.main()

if __name__ == "__main__":
    g = GHHRestorer()
    main()
