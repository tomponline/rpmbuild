Summary: The Yasm Modular Assembler
Name: yasm
Version: 1.3.0
Release: 1
URL: http://yasm.tortall.net/
Source0: %{name}-%{version}.tar.gz
License: GPL v2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-root

%description
The Yasm Modular Assembler 

%prep
%setup -q

%build
#Run main configure script
./configure \
	--prefix=%{_prefix} 
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/usr
