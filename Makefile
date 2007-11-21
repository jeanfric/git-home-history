#
# Copyright (c) 2007 Jean-Francois Richard <jean-francois@richard.name>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

DESTDIR        ?=
prefix         	= $(patsubst %/,%,$(DESTDIR))/usr
bindir          = ${prefix}/bin
mandir	        = $(prefix)/share/man
man1dir         = $(mandir)/man1

MAN1_TXT= git-home-history.txt
DOC_MAN1=$(patsubst %.txt,%.1,$(MAN1_TXT))
DOC_HTML=$(patsubst %.txt,%.html,$(MAN1_TXT))

all: git-home-history man
.DEFAULT: all

# A convenient target for jfrichard to send the data
# to the webserver
dist: all html
	./send-dist.sh

man: man1
man1: $(DOC_MAN1)

html: $(DOC_HTML)

%.html : %.txt
	a2x -f xhtml $<
	rm -f $(patsubst %.txt,%.xml,$<)

%.1 : %.txt
	a2x -f manpage $<
	rm -f $(patsubst %.txt,%.xml,$<)


install: all
	install -d -m755 $(man1dir)
	install -m644 $(DOC_MAN1) $(man1dir)

	install -d -m755 $(bindir)
	install -m755 git-home-history $(bindir)
	@echo 
	@echo Install complete
	@echo
	@echo Add $(mandir) to your MANPATH
	@echo Add $(bindir) to your PATH

clean:
	rm -f *.xml *.1 *.html

.PHONY: install uninstall clean all man1 man
