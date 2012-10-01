Summary:	Text based browser for the world wide web
Name:		w3m
Version:	0.5.3
Release:	4
Epoch:		1
License:	MIT-like
Group:		Applications/Networking
Source0:	http://heanet.dl.sourceforge.net/w3m/%{name}-%{version}.tar.gz
# Source0-md5:	1b845a983a50b8dec0169ac48479eacc
Patch0:		%{name}-gzip_fallback.patch
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}-gc72.patch
Patch3:		%{name}-file-handle.patch
URL:		http://w3m.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gc-devel
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gettext-devel
BuildRequires:	gpm-devel
BuildRequires:	imlib2-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pkg-config
Provides:	webclient
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This a terminal based WWW browser. While it does not make any attempt
at displaying graphics, it has good support for HTML text formatting,
forms, and tables.

%package imgdisplay
Summary:	Image display support for w3m
Group:		Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description imgdisplay
Install this package if you want to display images in w3m run on xterm
or Linux framebuffer.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} '/^AC_PROG_CXX$/d' -i configure.ac

%build
cp -f /usr/share/automake/config.sub .
%{__gettextize}
%{__aclocal}
%{__autoconf}
%configure \
	--enable-gopher				\
	--enable-image="x11,fb,fb+s"		\
	--enable-keymap=lynx			\
	--with-browser=%{_bindir}/firefurz	\
	--with-editor=/bin/vi			\
	--with-imagelib="gdk-pixbuf"		\
	--with-mailer=/bin/mail			\
	--with-termlib=ncurses
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1

%{__make} install install-helpfile \
	DESTDIR=$RPM_BUILD_ROOT

# symlink instead of duplicated file
ln -sf w3mhelp-lynx_en.html $RPM_BUILD_ROOT%{_datadir}/w3m/w3mhelp.html

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/*.html doc/{README,keymap,menu}.* NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/w3m/cgi-bin/*.cgi
%attr(755,root,root) %{_libdir}/w3m/cgi-bin/w3mbookmark
%attr(755,root,root) %{_libdir}/w3m/cgi-bin/w3mhelperpanel
%attr(755,root,root) %{_libdir}/w3m/inflate
%attr(755,root,root) %{_libdir}/w3m/xface2xpm

%dir %{_datadir}/w3m
%dir %{_libdir}/w3m
%dir %{_libdir}/w3m/cgi-bin

%lang(ja) %{_datadir}/w3m/w3mhelp*ja.*
%{_datadir}/w3m/w3mhelp*en.*
%{_datadir}/w3m/w3mhelp-funcname.pl
%{_datadir}/w3m/w3mhelp.html
%{_mandir}/man1/*.1*
%lang(ja) %{_mandir}/ja/man1/*.1*

%files imgdisplay
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/w3m/w3mimgdisplay

