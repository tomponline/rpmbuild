Summary: Beanstalkd
Name: beanstalkd
Version: 1.10
Release: 1
URL: https://github.com/beanstalkd/beanstalkd
Source0: %{name}-%{version}.tar.gz
License: MIT License
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
%if 0%{?rhel} < 7
Source1:  %{name}.init
%endif

%description
Beanstalkd message queue daemon.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}

%if 0%{?rhel} >= 7
#Install systemd files
%{__install} -p -D -m 0644 adm/systemd/beanstalkd.service $RPM_BUILD_ROOT/%{_unitdir}/%{name}.service
%{__install} -p -D -m 0644 adm/systemd/beanstalkd.socket $RPM_BUILD_ROOT/%{_unitdir}/%{name}.socket
%else
#Install init script
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%endif

%post
%if 0%{?rhel} < 7
/sbin/chkconfig --add %{name}
/sbin/chkconfig %{name} off
%endif

%preun
%if 0%{?rhel} < 7
if [ $1 = 0 ]; then
        /sbin/service %{name} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}
fi
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/beanstalkd
%if 0%{?rhel} >= 7
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%else
%{_initrddir}/%{name}
%endif
