Summary: MongoDB database driver
Name: php-pecl-mongodb
Version: 1.0.0
Release: 1
URL: http://pecl.php.net/package/mongodb
Source0: mongodb-%{version}.tgz
License: Apache License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: php >= 5.5, autoconf
Requires: php >= 5.5
Provides: php-mongodb

%description
MongoDB database driver

%prep
%setup -q -n mongodb-%{version}

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
cp -R modules/mongodb.so $RPM_BUILD_ROOT/$EXTDIR/mongodb.so

mkdir -p $RPM_BUILD_ROOT/etc/php.d/
echo "extension=mongodb.so" > $RPM_BUILD_ROOT/etc/php.d/mongodb.ini

%files
%defattr(-,root,root)
/usr
/etc/php.d/mongodb.ini

