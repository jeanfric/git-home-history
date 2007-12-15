pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_in_files = ghh.pc.in
pkgconfig_DATA = $(pkgconfig_in_files:.pc.in=.pc)

gladedir = $(pkgdatadir)/glade
glade_DATA = \
	gtk-ghh-commit.glade \
	gtk-ghh-restore.glade \
	gtk-ghh.glade

DISTCLEANFILES = \
	$(pkgconfig_DATA)

EXTRA_DIST = \
	$(glade_DATA) \
	$(pkgconfig_in_files)

