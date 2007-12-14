#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
import gobject
import os
import resource
import sys

def daemonize():
    """Double-forks this process to make it become a daemon"""
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if (pid == 0):
        os.setsid()
        try:
            pid = os.fork()
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)
        if (pid == 0):
            os.chdir("/")
            os.umask(0)
        else:
            os._exit(0)
    else:
        os._exit(0)

    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if (maxfd == resource.RLIM_INFINITY):
        maxfd = 1024
    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass
    os.open("/dev/null", os.O_RDWR)
    os.dup2(0, 1)
    os.dup2(0, 2)
    return(0)


class GHH(dbus.service.Object):

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
        return ['1', '2']

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = 's', out_signature = 't')
    def get_latest_revision_date_of_file(self, path):
        """Receive a "path/to/file", return the most recent revision stored in
        the history store"""
        return 1121212

    @dbus.service.method(dbus_interface = 'org.gnome.ghh.Test',
                         in_signature = 'st', out_signature = 's')
    def get_file_at_revision_date(self, file, time):
        """Receive a { "path/to/file" : "seconds from 1970" }, return a path
        to that (freshly uncompressed) file, as of the given revision date"""
        return str("/tmp/patate")


if __name__ == "__main__":
#    ret = daemonize()

    logfile_path = os.path.expanduser("~/.ghh-service.log")
    log = open(logfile_path, "w")
    log.write("ghh starting - pid %s\n" % os.getpid() )
    log.flush()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    name = dbus.service.BusName("org.gnome.ghh", session_bus)
    object = GHH(session_bus, '/org/gnome/ghh', log)

    mainloop = gobject.MainLoop()
    mainloop.run()
