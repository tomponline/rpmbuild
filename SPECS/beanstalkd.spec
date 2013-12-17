Summary: Beanstalkd
Name: beanstalkd
Version: 1.9
Release: 1
URL: http://kr.github.com/beanstalkd/
Source0: %{name}-%{version}.tar.gz
License: GPL v2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
Source1:  %{name}.init

%description
Beanstalkd message queue daemon

%prep
%setup -q

%build

#Run main configure script
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}

#Install init script
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

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
/usr/bin/beanstalkd
%{_initrddir}/%{name}

