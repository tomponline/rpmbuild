%global __os_install_post %{nil}
Summary: Google Go language compiler
Name: golang
Version: 1.10.3
Release: 1
URL: https://golang.org/dl/
Source0: go%{version}.linux-amd64.tar.gz
License: https://golang.org/LICENSE
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
AutoReqProv: no

%description
Google Go language compiler

%prep

%build

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

#Unpack precompiled binaries
install -d -m 755 $RPM_BUILD_ROOT/usr/local
tar -C $RPM_BUILD_ROOT/usr/local -xzf %{SOURCE0}

#Modify system wide PATH to find go binary
install -d -m 755 $RPM_BUILD_ROOT/etc/profile.d
echo 'export PATH=$PATH:/usr/local/go/bin' > $RPM_BUILD_ROOT/etc/profile.d/golang.sh

%post
echo "I have modified your system PATH to include go, please log out and back in again"

%files
%defattr(-,root,root)
/usr/local/go
/etc/profile.d/golang.sh

