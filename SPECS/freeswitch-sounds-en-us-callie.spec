%define version 1.0.18
%define release 3

%define fsname  freeswitch
%define prefix  /usr
%define _prefix %{prefix}
%define _datarootdir    %{_prefix}/share

##############################################################################
# General
##############################################################################

Summary: FreeSWITCH en-gb-rachael  prompts
Name: freeswitch-sounds-en-us-callie
Version: %{version}
Release: %{release}
License: Commercial
Group: Applications/Communications
Packager: TomP <tomp@tomp.co.uk>
URL: http://www.freeswitch.org
Source0: %{name}-8000-%{version}.tar.gz
Source1: %{name}-16000-%{version}.tar.gz
Source2: %{name}-32000-%{version}.tar.gz
Source3: %{name}-48000-%{version}.tar.gz
BuildArch: noarch
Requires: freeswitch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FreeSWITCH 8kHz en-us Callie prompts.

%prep
%setup -b0 -b1 -b2 -b3 -c sounds

%build
# nothing to do here

%install
[ "%{buildroot}" != '/' ] && rm -rf %{buildroot}

# create the sounds directories
%{__install} -d -m 0755 %{buildroot}%{_datarootdir}/%{fsname}/sounds/
%{__cp} -r * %{buildroot}%{_datarootdir}/%{fsname}/sounds/

%clean
[ "%{buildroot}" != '/' ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_datarootdir}/%{fsname}/sounds
