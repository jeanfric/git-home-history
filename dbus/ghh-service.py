#!/usr/bin/env python

import commands
import dbus
import dbus.service
import dbus.mainloop.glib
import gobject
import os
import os.path
import string
import tempfile
import time

class GHHException(dbus.DBusException):
    _dbus_error_name = 'org.gnome.ghh.Exception'

class GHH(dbus.service.Object):

    def raise_on_no_fullpath(self, path):
        if path[0] != "/":
            raise GHHException("Specified path '%s' is not a full path" % path)

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = '', out_signature = 'i')
    def get_version(self):
        # TODO : will need to use defs.py from the GHH package!
        return 1

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = 's', out_signature = 'at')
    def list_revision_dates_of_file(self, path):
        """Receive a "path/to/file", return an array of seconds from 1970
        corresponding to all known revisions dates of the particular file"""
        self.raise_on_no_fullpath(path)
        # git does not support being told to use a full path (yet)
        # so we move to the base directory to call git on the basename
        # (ugly, yes)
        os.chdir(os.path.dirname(path))
        (status, output) = commands.getstatusoutput("git-log --pretty=format:%%ct '%s'" % os.path.basename(path))
        if status != 0:
            return [0]
        else:
            return map(long, filter(lambda n: n, output.split("\n")))

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = 's', out_signature = 't')
    def get_latest_revision_date_of_file(self, path):
        """Receive a "path/to/file", return the most recent revision stored in
        the history store"""
        return self.list_revision_dates_of_file(path)[0]

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = 'st', out_signature = 's')
    def get_file_at_revision_date(self, path, timespec):
        """Receive a { "path/to/file" : "seconds from 1970" }, return a path
        to that (freshly uncompressed) file, as of the given revision date"""
        self.raise_on_no_fullpath(path)

        # find the git base directory by checking from the current
        # path to / for a ".git" directory
        path_tokens = path.split("/")
        for i in range(0, len(path_tokens)):
            test_path = str("/").join(path_tokens[0:-i])
            if os.path.isdir(test_path + "/.git"):
                git_dir = test_path
                rel_to_git_path = str("/").join(path_tokens[-i:])
                break

        # check that this will parse under git
        (status, git_hash) = commands.getstatusoutput(
            """git-rev-parse "HEAD@{%s}:%s" """ %
            (timespec, rel_to_git_path))

        if status != 0:
            raise GHHException("Could not find the given file '%s' as of '%s'" %
                               (path, timespec))

        # git does not support being told to use a full path (yet) so
        # we move to the base directory to call git on the filename
        # whose path is set relative to the root of the git project
        os.chdir(git_dir)
        # try to keep the same suffix as the original, for easy
        # finding of the file type
        newpath = tempfile.mkstemp(prefix="%s." % str(timespec),
                                   suffix=".%s" % os.path.basename(path))[1]
        (status, output) = commands.getstatusoutput("GIT_PAGER=cat git-show %s > %s" %
                                                    (git_hash, newpath))
        if status != 0:
            raise GHHException("Could not extract the given file '%s' as of '%s'" % (path, timespec))

        return newpath


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.gnome.ghh", session_bus)
    object = GHH(session_bus, '/org/gnome/ghh')
    mainloop = gobject.MainLoop()
    mainloop.run()
