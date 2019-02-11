Summary: IPv6 neighbour discovery advertisement sender
Name: ndsend
Version: 4.9.4
Release: 1
URL: https://download.openvz.org/utils/vzctl/current/src/vzctl-%{version}.tar.bz2
Source0: vzctl-%{version}.tar.bz2
License: LGPLv2+ and GPLv2
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
IPv6 neighbour discovery advertisement sender

%prep
%setup -q -n vzctl-%{version}

%build
gcc src/ndsend.c -o ndsend

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/usr/sbin
install -m 755 ndsend $RPM_BUILD_ROOT/usr/sbin/ndsend

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/usr/sbin/ndsend

