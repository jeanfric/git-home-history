#!/usr/bin/env python

import dbus
import os
import os.path

bus = dbus.SessionBus()
g = bus.get_object('org.gnome.ghh',
                      '/org/gnome/ghh')
gg = dbus.Interface(g, dbus_interface='org.gnome.ghh.Test')

testfile = os.getcwd() + "/" + os.path.basename(__file__)
#testfile = "test"
print g.Introspect()
print "get_version()"
print gg.get_version()
print "list_revision_dates_of_file('%s')" % testfile
print gg.list_revision_dates_of_file(testfile)
print "get_latest_revision_date_of_file('%s')" % testfile
print gg.get_latest_revision_date_of_file(testfile)
v= gg.get_latest_revision_date_of_file(testfile) + 1

print "get_file_at_revision_date('%s', %s)" % (testfile, str(v))
print gg.get_file_at_revision_date(testfile, v)
