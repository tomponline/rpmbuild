Summary: MongoDB database driver
Name: php-pecl-mongo
Version: 1.4.1
Release: 1
URL: http://pecl.php.net/package/mongo
Source0: mongo-%{version}.tgz
License: Apache License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: php >= 5.5, autoconf
Requires: php >= 5.5
Provides: php-mongo

%description
MongoDB database driver

%prep
%setup -q -n mongo-%{version}

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
cp -R modules/mongo.so $RPM_BUILD_ROOT/$EXTDIR/mongo.so

mkdir -p $RPM_BUILD_ROOT/etc/php.d/
echo "extension=mongo.so" > $RPM_BUILD_ROOT/etc/php.d/mongo.ini

%files
%defattr(-,root,root)
/usr
/etc/php.d/mongo.ini

