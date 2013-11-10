Summary: Tinc VPN
Name: tinc
Version: 1.0.23
Release: 1
URL: http://tinc-vpn.org/
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.init
License: GPL v2
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: lzo-devel, zlib-devel, openssl-devel

%description
TINC VPN

%prep
%setup -q

%build

./configure \
        --prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#Install init script
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

rm %{buildroot}/usr/share/info/dir

%post
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} off

%preun
if [ $1 = 0 ]; then
       	/sbin/service %{name} stop > /dev/null 2>&1
       	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/sbin/tincd
/usr/share/info/tinc.info.gz
/usr/share/man/man5/tinc.conf.5.gz
/usr/share/man/man8/tincd.8.gz
%{_initrddir}/%{name}
%dir %{_sysconfdir}/%{name}
