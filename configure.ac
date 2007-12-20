AC_INIT(ghh, 0.1, jean-francois@richard.name)
AC_CONFIG_SRCDIR(lib/__init__.py)
AC_CONFIG_HEADERS(config.h)
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE
GNOME_COMMON_INIT

AM_MAINTAINER_MODE
AM_DISABLE_STATIC
AM_PROG_LIBTOOL
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")
AC_PROG_CC

dnl ****************************************************************************
dnl * Pkg-Config
dnl ****************************************************************************
AC_CHECK_PROG(HAVE_PKGCONFIG, pkg-config, yes, no)
if test "x$HAVE_PKGCONFIG" = "xno"; then
  AC_MSG_ERROR(you need to have pkgconfig installed !)
fi

dnl ****************************************************************************
dnl * Translation & i18n
dnl ****************************************************************************
GETTEXT_PACKAGE="ghh"
IT_PROG_INTLTOOL([0.35.0])
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [The gettext package])
AM_GLIB_GNU_GETTEXT

dnl ****************************************************************************
dnl * Gnome Doc Utils
dnl ****************************************************************************
GNOME_DOC_INIT

dnl ****************************************************************************
dnl * Where's that git?
dnl ****************************************************************************
AC_PATH_PROG(GIT, git)

dnl ****************************************************************************
dnl * Asciidoc's a2x
dnl ****************************************************************************
AC_PATH_PROG(A2X, a2x)

dnl ****************************************************************************
dnl * Python 2.4
dnl ****************************************************************************
AM_PATH_PYTHON(2.4)

dnl ****************************************************************************
dnl * Gnome libs we need
dnl ****************************************************************************
PKG_CHECK_MODULES(GHH,
	gtk+-2.0			>= 2.12
	glib-2.0			>= 2.14
	libgnome-2.0			>= 2.20
)

dnl ****************************************************************************
dnl * Write the values of various paths in variables
dnl ****************************************************************************
AC_SUBST(VERSION)
AC_SUBST(PACKAGE)

AS_AC_EXPAND(EXPANDED_DATADIR, "$datarootdir")
AC_SUBST(EXPANDED_DATADIR)

AS_AC_EXPAND(EXPANDED_LIBDIR, "$libdir")
AC_SUBST(EXPANDED_LIBDIR)

AS_AC_EXPAND(EXPANDED_BINDIR, "$bindir")
AC_SUBST(EXPANDED_BINDIR)

AS_AC_EXPAND(EXPANDED_MANDIR, "$mandir")
AC_SUBST(EXPANDED_MANDIR)

dnl ****************************************************************************
dnl * --------------------------------------------------------------------------
dnl ****************************************************************************
AC_OUTPUT([
Makefile
src/git-home-history
src/Makefile
lib/Makefile
lib/defs.py
dbus/Makefile
ui/Makefile
data/ghh.pc
data/Makefile
doc/Makefile
po/Makefile.in
])

echo
echo $PACKAGE v$VERSION
echo
echo Prefix............... : $prefix
echo

