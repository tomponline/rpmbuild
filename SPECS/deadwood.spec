Summary: Deadwood DNS resolver
Name: deadwood
Version: 3.2.07
Release: 1
URL: http://maradns.samiam.org/
Source0: %{name}-%{version}.tar.bz2
License: GPL v2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
Beanstalkd message queue daemon

%prep
%setup -q

%build
#export FLAGS='-O3 -Os -DIPV6'
export FLAGS='-O3'
cd src
%{__make} -f Makefile.sl6

%install

#Install binary
%{__install} -p -D -m 0755 src/Deadwood %{buildroot}/usr/sbin/deadwood

#Install config script
%{__install} -p -D -m 0600 doc/dwood3rc %{buildroot}/etc/dwood3rc

#Create cache dir
%{__mkdir} -p -m 0700 %{buildroot}/etc/deadwood

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/sbin/deadwood
%attr(0600,root,root) %config(noreplace) /etc/dwood3rc
%dir %attr(0700,nobody,nobody) /etc/deadwood
