Summary: wkhtmltopdf
Name: wkhtmltopdf
Version: 0.9.9
Release: 1
URL: http://code.google.com/p/wkhtmltopdf/
Source0: wkhtmltopdf-0.9.9-static-i386.tar.bz2
License: GNU Lesser GPL
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
Requires: libXrender, fontconfig, libXext

%description
Simple shell utility to convert html to pdf using the webkit rendering engine, and qt.

#Disable stripping of static binaries
%global __os_install_post %{nil}

%prep
%setup -c

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

#Create /usr/bin dir
install -m 755 -d $RPM_BUILD_ROOT/%{_bindir}

#Copy wkhtmltopdf
install -m 755 %{name}-i386 $RPM_BUILD_ROOT%{_bindir}/%{name}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
