man_MANS = \
	git-home-history.1

ASCIIDOC_TO_MAN = $(A2X) -f manpage

git-home-history.1: git-home-history.txt
	$(ASCIIDOC_TO_MAN) $<

CLEANFILES = \
	$(patsubst %.1,%.xml,$(man_MANS)) \
	$(man_MANS)


