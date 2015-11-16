Summary: minidlna-transacode
Name: minidlna-transcode
Version: 1.1.5
Release: 1
URL: http://sourceforge.net/projects/minidlna/
Source0: readymedia-transcode.tar.gz
License: GPL v2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
minidlna

%prep
%setup -q -n readymedia-transcode

%build
./configure --prefix=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr/sbin/minidlnad
/usr/share
