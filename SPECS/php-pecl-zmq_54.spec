Summary: ZeroMQ client
Name: php-pecl-zmq
Version: 1.1.2
Release: 1
URL: http://pecl.php.net/package/zmq
Source0: zmq-%{version}.tgz
License: Apache License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: php >= 5.4, autoconf
Requires: php >= 5.4

%description
ZeroMQ client

%prep
%setup -q -n zmq-%{version}

%build

#Run main configure script
phpize
./configure
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export INSTALL_ROOT=$RPM_BUILD_ROOT

EXTDIR=`php-config --extension-dir`

install -d -m 755 $RPM_BUILD_ROOT/$EXTDIR
cp -R modules/zmq.so $RPM_BUILD_ROOT/$EXTDIR/zmq.so

mkdir -p $RPM_BUILD_ROOT/etc/php.d/
echo "extension=zmq.so" > $RPM_BUILD_ROOT/etc/php.d/zmq.ini

%files
%defattr(-,root,root)
/usr
/etc/php.d/zmq.ini

