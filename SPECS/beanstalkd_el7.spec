Summary: Beanstalkd
Name: beanstalkd
Version: 1.10
Release: 1
URL: https://github.com/beanstalkd/beanstalkd
Source0: %{name}-%{version}.tar.gz
License: MIT License
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
#Source1:  %{name}.init

%description
Beanstalkd message queue daemon.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}

#Install systemd files
%{__install} -p -D -m 0644 adm/systemd/beanstalkd.service $RPM_BUILD_ROOT/%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 adm/systemd/beanstalkd.socket $RPM_BUILD_ROOT/%{_unitdir}/%{name}.socket

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/beanstalkd
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket

