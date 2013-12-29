Summary: ZeroMQ
Name: zeromq
Version: 4.0.3
Release: 1
URL: http://zeromq.org
Source0: %{name}-%{version}.tar.gz
License: LGPL v3
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
ZeroMQ

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT/%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/bin/curve_keygen
/usr/include
/usr/lib
/usr/share/man
