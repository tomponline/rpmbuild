%define version	3.6.0
%define release	3

%define fsname  freeswitch
%define prefix  /usr
%define _prefix %{prefix}
%define _datarootdir    %{_prefix}/share

##############################################################################
# General
##############################################################################

Summary: FreeSWITCH en-gb-rachael  prompts
Name: freeswitch-sounds-en-gb-rachael
Version: %{version}
Release: %{release}
License: Commercial
Group: Applications/Communications
Packager: TomP <tomp@tomp.co.uk>
URL: http://www.freeswitch.org
Source0: british-english-rachael-en-gb-3.6.0-8k.tar.gz
BuildArch: noarch
Requires: freeswitch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
FreeSWITCH 8kHz en-gb Rachael prompts.

%prep
%setup -b0 -q -n sounds

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
