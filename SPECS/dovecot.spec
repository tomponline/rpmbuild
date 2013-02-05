Summary: Dovecot Secure imap server
Name: dovecot
Version: 2.1.14
Release: 1
License: LGPL
Group: System Environment/Daemons

Source: %{name}-%{version}.tar.gz
Source1: dovecot.init
URL: http://www.dovecot.org/
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: openssl-devel
BuildRequires: zlib-devel
Prereq: openssl >= 0.9.7f-4, /sbin/chkconfig, /usr/sbin/useradd

%define dovecot_uid 97
%define dovecot_gid 97

%description
Dovecot is an IMAP server for Linux/UNIX-like systems, written with security 
primarily in mind.  It also contains a small POP3 server.  It supports mail 
in either of maildir or mbox formats.

%prep
%setup -q

%build
	./configure \
	--prefix=%{_prefix} \
	--localstatedir=/var \
	--sysconfdir=/etc \
	--without-docs \
	--with-ssl=openssl
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/%{name}

mkdir -p $RPM_BUILD_ROOT/etc/%{name}

%pre
/usr/sbin/useradd -c "dovecot" -u %{dovecot_uid} -s /sbin/nologin -r -d /usr/libexec/dovecot dovecot 2>/dev/null || :

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
 /usr/sbin/userdel dovecot 2>/dev/null || :
 /usr/sbin/groupdel dovecot 2>/dev/null || :
 [ -f /var/lock/subsys/%{name} ] && /sbin/service %{name} stop > /dev/null 2>&1
 /sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/etc/dovecot
/etc/rc.d/init.d/dovecot
/usr
