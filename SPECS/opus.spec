Summary:	IETF Opus Interactive Audio Codec
Name:		opus
Version:	1.1
Release:	1%{?dist}
License:	BSD
Group:		Libraries
Source0:	http://downloads.xiph.org/releases/opus/%{name}-%{version}.tar.gz
# Source0-md5:	c5a8cf7c0b066759542bc4ca46817ac6
Patch0:		%{name}-sh.patch
URL:		http://opus-codec.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1.6
BuildRequires:	libtool
BuildRequires:	doxygen
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Opus codec is designed for interactive speech and audio
transmission over the Internet. It is designed by the IETF Codec
Working Group and incorporates technology from Skype's SILK codec and
Xiph.Org's CELT codec.

%package devel
Summary:	Header files for OPUS libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OPUS libraries.

%package static
Summary:	Static OPUS libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OPUS libraries.

%prep
%setup -q
%patch0 -p1

%build
./autogen.sh
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-custom-modes \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/opus/html

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README
%attr(755,root,root) %{_libdir}/libopus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libopus.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/html/*
%attr(755,root,root) %{_libdir}/libopus.so
%{_libdir}/libopus.la
%{_includedir}/opus
%{_libdir}/pkgconfig/opus.pc
%{_datadir}/aclocal/opus.m4
%{_mandir}/man3/opus_*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libopus.a
%changelog
* Thu May 21 2015 Chris Rienzo <Chris.Rienzo@citrix.com>
- Changes for FreeSWITCH source dependencies
- Removed .pl

* Tue Feb 03 2015 TLD Linux <feedback@tld-linux.org>
- For complete changelog see: http://git.tld-linux.org/?p=packages/opus.git;a=log;h=master

* Fri Dec 06 2013 Jakub Bogusz <qboosh@pld-linux.org> 83841a1
- updated to 1.1
- added sh patch (fixes build with sh not being bash)

* Sun Nov 03 2013 Jakub Bogusz <qboosh@pld-linux.org> b776a8b
- enable custom modes interface, release 2

* Thu Jul 18 2013 Jakub Bogusz <qboosh@pld-linux.org> c4ceab3
- updated to 1.0.3

* Sat Dec 08 2012 Jakub Bogusz <qboosh@pld-linux.org> 0db21e7
- updated to 1.0.2

* Thu Sep 13 2012 Jakub Bogusz <qboosh@pld-linux.org> 8e4598f
- updated to 1.0.1
- removed obsolete link patch

* Tue May 22 2012 Jakub Bogusz <qboosh@pld-linux.org> 829f5b6
- updated to 0.9.14

* Wed Feb 22 2012 Jakub Bogusz <qboosh@pld-linux.org> bf9fed0
- updated to 0.9.9

* Wed Nov 02 2011 Jakub Bogusz <qboosh@pld-linux.org> 1950c9f
- updated to 0.9.8

* Wed Aug 17 2011 Jakub Bogusz <qboosh@pld-linux.org> db78488
- updated to 0.9.6

* Tue Jul 12 2011 Jakub Bogusz <qboosh@pld-linux.org> 5a4888b
- updated to 0.9.5
- updated link patch
- removed outdated celt-rename patch (everything is now built as libopus library)

* Wed Mar 16 2011 Jakub Bogusz <qboosh@pld-linux.org> fd215a1
- updated to 0.9.3

* Fri Mar 11 2011 Jakub Bogusz <qboosh@pld-linux.org> 9a8599c
- new

