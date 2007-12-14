#!/usr/bin/env python

import dbus
bus = dbus.SessionBus()
g = bus.get_object('org.gnome.ghh',
                      '/org/gnome/ghh')
gg = dbus.Interface(g, dbus_interface='org.gnome.ghh.Test')

print g.Introspect()
print "get_version()"
print gg.get_version()
print "list_revision_dates_of_file('/test')"
print gg.list_revision_dates_of_file('/test')
print "get_latest_revision_date_of_file('/test')"
print gg.get_latest_revision_date_of_file('/test')
print "get_file_at_revision_date('/test', 1)"
print gg.get_file_at_revision_date('/test', 1)
