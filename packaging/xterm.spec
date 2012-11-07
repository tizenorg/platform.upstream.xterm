Name:           xterm
Version:        279
Release:        0
License:        MIT
Summary:        The basic X terminal program
Url:            http://invisible-island.net/xterm/
Group:          System/X11/Utilities
Source:         ftp://invisible-island.net/xterm/%{name}-%{version}.tgz
Source2:        ftp://invisible-island.net/xterm/%{name}-%{version}.tgz.asc
Source1:        luitx
Source3:        Backarrow2Delete
Source4:        Backarrow2BackSpace
Source6:        terminal.png
%define vttest_version 20120506
Source7:        ftp://invisible-island.net/vttest/vttest-%vttest_version.tgz
Source10:       ftp://invisible-island.net/vttest/vttest-%vttest_version.tgz.asc
Source8:        20x20ja.bdf.bz2
Source9:        20x20ko.bdf.bz2
# Snoop for the escape sequence assignment of the keypad
Source20:       snooper.tar.bz2
Patch1:         p_xterm-settings.diff
Patch2:         p_xterm-sigwinch.diff
Patch3:         bug-246573-tentative-patch.diff
Patch4:         desktop.diff
Patch5:         xterm-disallow-window-and-fonts-ops.patch
Patch6:         libtinfo.diff
Patch293793:    bugzilla-293793-do-not-insist-on-iso8859-fonts-for-the-menu.patch
BuildRequires:  freetype-devel
BuildRequires:  libXaw-devel
BuildRequires:  ncurses-devel
BuildRequires:  update-desktop-files
BuildRequires:  utempter-devel
Provides:       XFree86:/usr/X11R6/bin/xterm
Provides:       xorg-x11:/usr/X11R6/bin/xterm
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package contains the basic X.Org terminal program.

%prep
%setup -q -b7
%patch1 -p1 -b .xterm-settings
%patch2 -p0 -b .xterm-sigwinch
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch293793 -p1
cp $RPM_SOURCE_DIR/*bdf.bz2 .
bunzip2 *.bdf.bz2

%build
%define xappdefs   /usr/share/X11/app-defaults
%define xfontsd    /usr/share/fonts
%define xterminfo  /usr/lib/X11/etc

%configure \
    --enable-256-color \
    --enable-dec-locator \
    --enable-hp-fkeys \
    --enable-mini-luit \
    --enable-sco-fkeys \
    --enable-wide-chars \
    --with-utempter \
    --with-tty-group=tty \
    --with-app-defaults=%{xappdefs} \

make %{?_smp_mflags}

pushd "../vttest-%vttest_version"
%configure
make %{?_smp_mflags}
popd

if [ ! which bdftopcf ] ; then exit 1; fi
for i in *.bdf
do
    bdftopcf "$i" | gzip -9 >"${i%.bdf}.pcf.gz"
done

%install
%make_install

mkdir -p %{buildroot}%{xterminfo}
install -m 644 terminfo %{buildroot}%{xterminfo}/xterm.terminfo
install -m 644 termcap  %{buildroot}%{xterminfo}/xterm.termcap

pushd "../vttest-%vttest_version"
%make_install
popd
install -m 755 $RPM_SOURCE_DIR/luitx %{buildroot}/usr/bin
install -m 755 $RPM_SOURCE_DIR/Backarrow2Delete %{buildroot}/usr/bin
install -m 755 $RPM_SOURCE_DIR/Backarrow2BackSpace %{buildroot}/usr/bin
install -m 644 $RPM_SOURCE_DIR/README.SuSE .

mkdir -p %{buildroot}/usr/share/pixmaps
install -m 644 $RPM_SOURCE_DIR/terminal.png \
    %{buildroot}/usr/share/pixmaps

mkdir -p %{buildroot}%{xfontsd}/misc/
install -m 644 *.pcf.gz %{buildroot}%{xfontsd}/misc/
%tizen_update_desktop_file -i xterm TerminalEmulator


%files
%defattr(-,root,root)
%doc README README.i18n
/usr/bin/vttest
/usr/bin/luitx
%attr(755,root,root) /usr/bin/xterm
/usr/bin/resize
/usr/bin/uxterm
/usr/bin/koi8rxterm
/usr/bin/Backarrow2Delete
/usr/bin/Backarrow2BackSpace
/usr/share/man/man1/xterm.1.gz
/usr/share/man/man1/resize.1.gz
%{_mandir}/man1/vttest.1.gz
%{_mandir}/man1/koi8rxterm.1.gz
%{_mandir}/man1/uxterm.1.gz
/usr/share/applications/xterm.desktop
/usr/share/pixmaps/*
%dir %{xterminfo}
%{xterminfo}/xterm.termcap
%{xterminfo}/xterm.terminfo
%dir %{xfontsd}/misc
%{xfontsd}/misc/20x20ja.pcf.gz
%{xfontsd}/misc/20x20ko.pcf.gz
%{xappdefs}/KOI8RXTerm
%{xappdefs}/KOI8RXTerm-color
%{xappdefs}/UXTerm
%{xappdefs}/UXTerm-color
%{xappdefs}/XTerm
%{xappdefs}/XTerm-color

%changelog
