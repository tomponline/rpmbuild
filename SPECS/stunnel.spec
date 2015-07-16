Summary: Stunnel
Name: stunnel
Version: 5.20
Release: 1
URL: https://www.stunnel.org
Source0: %{name}-%{version}.tar.gz
License: GPL v2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
Secure tunnel daemon

%prep
%setup -q

%build
#Run main configure script
./configure \
	--prefix=%{_prefix} \
        --sysconfdir=/etc
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/etc/stunnel/stunnel.conf-sample
/usr/bin/stunnel
/usr/bin/stunnel3
/usr/lib/stunnel/libstunnel.la
/usr/lib/stunnel/libstunnel.so
/usr/share/doc/stunnel
/usr/share/man/man8/stunnel*

