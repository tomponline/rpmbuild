Summary: Pure-FTPD server
Name: pure-ftpd
Version: 1.0.42
Release: 3
License: LGPL
Group: System Environment/Daemons

Source: %{name}-%{version}.tar.bz2
Source1: %{name}.init
URL: http://www.pureftpd.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: /sbin/chkconfig

%description
Pure-FTPD

%prep
%setup -q

%build
	./configure \
        --prefix=%{_prefix} \
	--localstatedir=/var \
        --sysconfdir=/etc \
        --with-boring \
        --with-paranoidmsg \
        --without-humor \
        --without-usernames \
        --with-quotas \
	--without-inetd \
        --with-puredb \
	--with-tls \
	--with-certfile=/etc/pki/tls/private/pure-ftpd.pem
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/pure-ftpd

install -m 755 configuration-file/pure-config.pl $RPM_BUILD_ROOT%{_prefix}/sbin/
install -m 644 configuration-file/pure-ftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/

# replace some occurences of prefix and sysconfig:
sed "s|\(\$prefix *= *['\"]\)%{prefixdef}|\1%{_prefix}|g" < configuration-file/pure-config.pl > configuration-file/pure-config.pl_replaced
install -m 755 configuration-file/pure-config.pl_replaced $RPM_BUILD_ROOT%{_prefix}/sbin/pure-config.pl

%post
/sbin/chkconfig --add  %{name}

%preun
/sbin/chkconfig --del  %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/usr/bin/pure-pw
/usr/bin/pure-pwconvert
/usr/bin/pure-statsdecode
/usr/sbin/pure-authd
/usr/sbin/pure-ftpd
/usr/sbin/pure-ftpwho
/usr/sbin/pure-mrtginfo
/usr/sbin/pure-quotacheck
/usr/sbin/pure-uploadscript
%config(noreplace)  /etc/pure-ftpd.conf
/etc/rc.d/init.d/pure-ftpd
/usr/sbin/pure-config.pl
/usr/share/man/man8/pure-authd.8.gz
/usr/share/man/man8/pure-ftpd.8.gz
/usr/share/man/man8/pure-ftpwho.8.gz
/usr/share/man/man8/pure-mrtginfo.8.gz
/usr/share/man/man8/pure-pw.8.gz
/usr/share/man/man8/pure-pwconvert.8.gz
/usr/share/man/man8/pure-quotacheck.8.gz
/usr/share/man/man8/pure-statsdecode.8.gz
/usr/share/man/man8/pure-uploadscript.8.gz
