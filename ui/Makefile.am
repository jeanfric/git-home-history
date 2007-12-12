gtk-ghh-commit: gtk-ghh-commit.py
	cp $< $@

gtk-ghh-restore: gtk-ghh-restore.py
	cp $< $@

gtk-ghh: gtk-ghh.py
	cp $< $@

bin_SCRIPTS = \
	gtk-ghh \
	gtk-ghh-restore \
	gtk-ghh-commit

BUILT_SOURCES = \
	gtk-ghh-commit \
	gtk-ghh-restore \
	gtk-ghh

ghhdir = $(pythondir)/deskbar
ghh_PYTHON = \
	defs.py \
	__init__.py

EXTRA_DIST = \
        defs.py.in

CLEANFILES = \
	$(BUILT_SOURCES)

DISTCLEANFILES = \
	defs.py \
	$(CLEANFILES)
