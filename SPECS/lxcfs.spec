Summary: Linux Containers File System
Name: lxcfs
Version: 3.0.3.1
Release: 1%{?dist}
URL: https://linuxcontainers.org/lxcfs/downloads/
Source0: %{name}-%{version}.tar.gz
License: Apache 2
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  systemd
BuildRequires:  docbook2X
BuildRequires:  doxygen
BuildRequires:  fuse-devel
Requires: fuse

%description
Linux Containers

%prep
%setup -q -n lxcfs

%build
./bootstrap.sh
%configure \
        --with-init-script=systemd
%{make_build}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/var/lib/lxcfs

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%dir /var/lib/lxcfs
/lib/systemd/system/lxcfs.service
/usr/bin/lxcfs
%config(noreplace) /usr/share/lxc/config/common.conf.d/00-lxcfs.conf
/usr/share/lxcfs/lxc.mount.hook
/usr/share/lxcfs/lxc.reboot.hook
/usr/lib64/lxcfs/liblxcfs.la
/usr/lib64/lxcfs/liblxcfs.so
