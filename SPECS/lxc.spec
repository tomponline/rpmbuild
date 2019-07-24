Summary: Linux Containers
Name: lxc
Version: 3.2.1
Release: 1%{?dist}
URL: https://linuxcontainers.org/lxc/downloads/
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+ and GPLv2
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: kernel-headers
BuildRequires: libselinux-devel
BuildRequires: pkgconfig(libseccomp)
BuildRequires: libcap libcap-devel
BuildRequires: libtool
BuildRequires: libseccomp-devel
BuildRequires: systemd
BuildRequires: pkgconfig(bash-completion)
Buildrequires: docbook2X
Buildrequires: doxygen
BuildRequires: graphviz libxslt pkgconfig
BuildRequires: systemd-units
Requires: wget rsync openssl bash-completion
Requires: %{name}-libs = %{version}-%{release}

Patch0: lxc-tree-wide-initialize-all-auto-cleanup-variables.patch

%description
Containers are insulated areas inside a system, which have their own namespace
for filesystem, network, PID, IPC, CPU and memory allocation and which can be
created using the Control Group and Namespace features included in the Linux
kernel.

This package provides the lxc-* tools, which can be used to start a single
daemon in a container, or to boot an entire "containerized" system, and to
manage and debug your containers.

%package	libs
Summary:	Shared library files for %{name}
Group:		System Environment/Libraries
%description	libs
The %{name}-libs package contains libraries for running %{name} applications.

%package	devel
Summary:	Development library for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}, pkgconfig
%description	devel
The %{name}-devel package contains header files and library needed for
development of the Linux containers.

%prep
%setup -q

%patch0 -p1

%build
./autogen.sh
export bashcompdir=%{_sysconfdir}/bash_completion.d
%configure \
	--enable-seccomp \
	--enable-selinux \
	--enable-capabilities \
	--with-init-script=systemd \
	--with-systemdsystemunitdir=%{_unitdir} \
	--enable-doc \
	--enable-bash \
	--disable-rpath \
	--disable-apparmor \
	--disable-cgmanager \
	--disable-silent-rules \
	--with-distro=centos

%{make_build}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

#Disable use of dmesg inside container.
echo "syslog errno 1" >> %{buildroot}%{_datadir}/%{name}/config/common.seccomp

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/lxc*
%{_mandir}/man5/lxc*
%{_mandir}/man7/lxc*
%{_mandir}/ja/man1/lxc*
%{_mandir}/ja/man5/lxc*
%{_mandir}/ja/man7/lxc*
%{_mandir}/ko/man1/lxc*
%{_mandir}/ko/man5/lxc*
%{_mandir}/ko/man7/lxc*
%{_datadir}/doc/*
%{_datadir}/lxc/*
%{_sysconfdir}/bash_completion.d
%config(noreplace) %{_sysconfdir}/lxc/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
%{_unitdir}/lxc-net.service
%{_unitdir}/lxc.service
%{_unitdir}/lxc@.service

%files libs
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/%{name}
%{_localstatedir}/*
%{_libexecdir}/%{name}/hooks/unmount-namespace
%{_libexecdir}/%{name}/lxc-apparmor-load
%{_libexecdir}/%{name}/lxc-monitord
%attr(4111,root,root) %{_libexecdir}/%{name}/lxc-user-nic
%attr(555,root,root) %{_libexecdir}/%{name}/lxc-net
%attr(555,root,root) %{_libexecdir}/%{name}/lxc-containers

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
