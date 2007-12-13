#!/usr/bin/env python

import dbus
bus = dbus.SessionBus()
g = bus.get_object('org.gnome.ghh',
                      '/org/gnome/ghh')
gg = dbus.Interface(g, dbus_interface='org.gnome.ghh.Test')
props = gg.get_version()
print props
