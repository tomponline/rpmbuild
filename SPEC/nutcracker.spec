Summary: Twitter's twemproxy nutcracker
Name: nutcracker
Version: 0.2.2
Release: 1
URL: http://code.google.com/p/twemproxy/
Source0: %{name}-%{version}.tar.gz
License: Apache License 2.0
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root
Source1:  %{name}.init

%description
twemproxy (pronounced "two-em-proxy"), aka nutcracker is a fast and lightweight proxy for memcached and redis protocol. 
It was primarily built to reduce the connection count on the backend caching servers.

%prep
%setup -q

%build

%configure
%__make

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%makeinstall PREFIX=%{buildroot}

#Install init script
#%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

%post
#/sbin/chkconfig --add %{name}

%preun
#if [ $1 = 0 ]; then
#        /sbin/service %{name} stop > /dev/null 2>&1
#        /sbin/chkconfig --del %{name}
#fi

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/bin/nutcracker
