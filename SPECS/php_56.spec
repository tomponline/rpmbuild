%define contentdir /var/www
%define apiver no-debug-non-zts-20131226

Summary: The PHP HTML-embedded scripting language. (PHP: Hypertext Preprocessor)
Name: php
Version: 5.6.22
Release: 1
License: The PHP License v3.01
Group: Development/Languages
URL: http://www.php.net/
Source0: http://www.php.net/distributions/php-%{version}.tar.bz2
Source1: php.conf
Source2: php.ini
Source3: php-apache2handler.ini

BuildRoot: %{_tmppath}/%{name}-root

BuildRequires: gcc, binutils, libtool
BuildRequires: curl-devel >= 7.9, httpd >= 2.2, libstdc++-devel, openssl-devel, zlib-devel
BuildRequires: fileutils, file >= 4.0, perl, gcc-c++, readline-devel
BuildRequires: curl-devel, libjpeg-devel, libpng-devel, libxml2-devel, freetype-devel, 
BuildRequires: libmcrypt-devel, libxslt-devel, libc-client-devel, krb5-devel, libexif-devel
Requires: 	file >= 4.0, php-common = %{version}-%{release}, 
Requires:	php-cli = %{version}-%{release}, php-pdo = %{version}-%{release},
Obsoletes: 	php-mhash

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated webpages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module which adds support for the PHP
language to Apache HTTP Server.

%package common
Group: Development/Languages
Summary: Common files for PHP
Requires: php = %{version}-%{release}

%description common
Provides PHP common files

%package mysql
Group: Development/Languages
Summary: MySQL module of PHP
Requires: php = %{version}-%{release}, php-pdo

%description mysql
Provides PHP MySQL module

%package gd
Group: Development/Languages
Summary: GD module of PHP
Requires: php = %{version}-%{release}

%description gd
Provides PHP GD module

%package mcrypt
Group: Development/Languages
Summary: MCrypt module of PHP
Requires: php = %{version}-%{release}

%description mcrypt
Provides PHP MCrypt module

%package mbstring
Group: Development/Languages
Summary: Mbstring module of PHP
Requires: php = %{version}-%{release}

%description mbstring
Provides PHP Mbstring module

%package bcmath
Group: Development/Languages
Summary: Bcmath module of PHP
Requires: php = %{version}-%{release}

%description bcmath
Provides PHP Bcmath module

%package soap
Group: Development/Languages
Summary: SOAP module of PHP
Requires: php = %{version}-%{release}

%description soap
Provides PHP SOAP module

%package xml
Group: Development/Languages
Summary: XML module of PHP
Requires: php = %{version}-%{release}
Provides: php-xsl

%description xml
Provides PHP xml module

%package zip
Group: Development/Languages
Summary: ZIP module of PHP
Requires: php = %{version}-%{release}

%description zip
Provides PHP ZIP module

%package sockets
Group: Development/Languages
Summary: Sockets module of PHP
Requires: php = %{version}-%{release}

%description sockets
Provides PHP Sockets module

%package pcntl
Group: Development/Languages
Summary: Process control module of PHP
Requires: php = %{version}-%{release}

%description pcntl
Provides PHP Process Control module

%package gettext
Group: Development/Languages
Summary: GNU gettext module of PHP
Requires: php = %{version}-%{release}

%description gettext
Provides GNU gettext module in PHP

%package ftp
Group: Development/Languages
Summary: FTP module in PHP
Requires: php = %{version}-%{release}

%description ftp
Provides FTP module in PHP

%package imap
Group: Development/Languages
Summary: IMAP module in PHP
Requires: php = %{version}-%{release}, libc-client

%description imap
Provides IMAP module in PHP

%package exif
Group: Development/Languages
Summary: EXIF module in PHP
Requires: php = %{version}-%{release}, 

%description exif
Provides EXIF module in PHP

%package cli
Group: Development/Languages
Summary: CLI executable for PHP
Requires: php = %{version}-%{release}

%description cli
CLI executable for PHP

%package readline
Group: Development/Languages
Summary: Readline support for PHP
Requires: php = %{version}-%{release}

%description readline
Readline support for PHP

%package devel
Group: Development/Languages
Summary: Development files for PHP
Requires: php = %{version}-%{release}

%description devel
Development files for PHP

%package pdo
Group: Development/Languages
Summary: PHP Data Objects
Requires: php = %{version}-%{release}

%description pdo
Development PHP Data Objects

%prep
%setup -q

%build

CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS CPPFLAGS

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

APXS=%{_sbindir}/apxs

if [ -f %{_bindir}/apxs ]
  then
	APXS=%{_bindir}/apxs
fi

#Run mod_php and cli binaries
./configure \
        --prefix=%{_prefix} \
	--libdir=%{_libdir}/php \
        --sysconfdir=%{_sysconfdir} \
        --with-config-file-path=%{_sysconfdir} \
	--with-config-file-scan-dir=%{_sysconfdir}/php.d \
        --with-freetype-dir=%{_prefix} \
        --with-png-dir=%{_prefix} \
        --enable-gd-native-ttf \
        --with-jpeg-dir=shared,%{_prefix} \
        --with-openssl \
        --with-zlib \
        --with-libxml-dir=shared,%{_prefix} \
	--with-xsl=shared,%{_prefix} \
        --with-apxs2=${APXS} \
        --enable-mbstring=shared \
	--enable-bcmath=shared \
        --with-gd=shared \
        --with-mysql=shared,mysqlnd \
        --with-mysqli=shared,mysqlnd \
        --with-pdo-mysql=shared,mysqlnd \
        --with-curl \
        --with-mcrypt=shared \
	--enable-soap=shared \
	--enable-dom=shared \
	--enable-pdo \
	--enable-xmlreader=shared \
	--enable-xmlwriter=shared \
	--without-pear \
	--enable-ipv6 \
	--with-pic \
	--enable-inline-optimization \
	--disable-debug \
	--enable-zip=shared \
	--enable-sockets=shared \
	--enable-pcntl=shared \
	--with-gettext=shared \
	--enable-ftp=shared \
	--with-imap=shared,%{_prefix} \
	--with-imap-ssl=%{_prefix} \
	--with-readline \
	--enable-exif=shared \
	--with-kerberos=%{_prefix}
make %{?_smp_mflags}

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

export INSTALL_ROOT=$RPM_BUILD_ROOT

# Install the Apache module
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules
install -m 755 .libs/libphp5.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/

# Apache config fragment
install -m 755 -d $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/php.conf $RPM_BUILD_ROOT/etc/httpd/conf.d

# Install rest
make install-cli
make install-modules
make install-headers
make install-pdo-headers
make install-build
make install-programs

# Install php.ini
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/
install -m 644 $RPM_SOURCE_DIR/php.ini $RPM_BUILD_ROOT%{_sysconfdir}/php.ini
install -m 644 $RPM_SOURCE_DIR/php-apache2handler.ini $RPM_BUILD_ROOT%{_sysconfdir}/php-apache2handler.ini

#Create /var/lib/php
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session

#Create /etc/php.d directory and install module ini files
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
echo "extension=gd.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/gd.ini
echo "extension=mcrypt.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mcrypt.ini
echo "extension=mysql.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mysql.ini
echo "extension=mysqli.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mysqli.ini
echo "extension=pdo_mysql.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pdo_mysql.ini
echo "extension=xsl.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xsl.ini
echo "extension=soap.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/soap.ini
echo "extension=xmlreader.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xmlreader.ini
echo "extension=xmlwriter.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/xmlwriter.ini
echo "extension=dom.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/dom.ini
echo "extension=mbstring.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mbstring.ini
echo "extension=bcmath.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/bcmath.ini
echo "extension=zip.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/zip.ini
echo "extension=sockets.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/sockets.ini
echo "extension=pcntl.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pcntl.ini
echo "extension=gettext.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/gettext.ini
echo "extension=ftp.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/ftp.ini
echo "extension=imap.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/imap.ini
echo "extension=exif.so" >  $RPM_BUILD_ROOT%{_sysconfdir}/php.d/exif.ini
echo "zend_extension=opcache.so" > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f "/etc/php-cli.ini" ]
then
	echo "Disabling php-cli.ini..."
 	mv /etc/php-cli.ini /etc/php-cli.ini.disabled
fi

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.ini
%config(noreplace) %{_sysconfdir}/php-apache2handler.ini
%dir %{_libdir}/php/extensions
%dir %{_libdir}/php/extensions/%{apiver}
%{_libdir}/php/extensions/%{apiver}/opcache.so
%config(noreplace) /etc/php.d/opcache.ini
%dir %{_libdir}/php
%{_libdir}/php/build
/usr/include/php
/usr/php/man
/usr/bin/php
/usr/bin/php-config
/usr/bin/phpize
%dir %{_sysconfdir}/php.d
%{_libdir}/httpd/modules/libphp5.so
%attr(0770,root,apache) %dir %{_localstatedir}/lib/php/session
%config(noreplace) %{_sysconfdir}/httpd/conf.d/php.conf

%files mysql
%defattr(-,root,root)
/etc/php.d/mysql.ini
/etc/php.d/mysqli.ini
/etc/php.d/pdo_mysql.ini
%{_libdir}/php/extensions/%{apiver}/mysql.so
%{_libdir}/php/extensions/%{apiver}/mysqli.so
%{_libdir}/php/extensions/%{apiver}/pdo_mysql.so

%files gd
%defattr(-,root,root)
%config(noreplace) /etc/php.d/gd.ini
%{_libdir}/php/extensions/%{apiver}/gd.so

%files mcrypt
%defattr(-,root,root)
%config(noreplace) /etc/php.d/mcrypt.ini
%{_libdir}/php/extensions/%{apiver}/mcrypt.so

%files mbstring
%defattr(-,root,root)
%config(noreplace) /etc/php.d/mbstring.ini
%{_libdir}/php/extensions/%{apiver}/mbstring.so

%files bcmath
%defattr(-,root,root)
%config(noreplace) /etc/php.d/bcmath.ini
%{_libdir}/php/extensions/%{apiver}/bcmath.so

%files soap
%defattr(-,root,root)
%config(noreplace) /etc/php.d/soap.ini
%{_libdir}/php/extensions/%{apiver}/soap.so

%files xml
%defattr(-,root,root)
%config(noreplace) /etc/php.d/dom.ini
%config(noreplace) /etc/php.d/xmlwriter.ini
%config(noreplace) /etc/php.d/xmlreader.ini
%config(noreplace) /etc/php.d/xsl.ini
%{_libdir}/php/extensions/%{apiver}/dom.so
%{_libdir}/php/extensions/%{apiver}/xmlwriter.so
%{_libdir}/php/extensions/%{apiver}/xmlreader.so
%{_libdir}/php/extensions/%{apiver}/xsl.so

%files zip
%defattr(-,root,root)
%config(noreplace) /etc/php.d/zip.ini
%{_libdir}/php/extensions/%{apiver}/zip.so

%files sockets
%defattr(-,root,root)
%config(noreplace) /etc/php.d/sockets.ini
%{_libdir}/php/extensions/%{apiver}/sockets.so

%files pcntl
%defattr(-,root,root)
%config(noreplace) /etc/php.d/pcntl.ini
%{_libdir}/php/extensions/%{apiver}/pcntl.so

%files gettext
%defattr(-,root,root)
%config(noreplace) /etc/php.d/gettext.ini
%{_libdir}/php/extensions/%{apiver}/gettext.so

%files common

%files ftp
%defattr(-,root,root)
%config(noreplace) /etc/php.d/ftp.ini
%{_libdir}/php/extensions/%{apiver}/ftp.so

%files imap
%defattr(-,root,root)
%config(noreplace) /etc/php.d/imap.ini
%{_libdir}/php/extensions/%{apiver}/imap.so

%files exif
%defattr(-,root,root)
%config(noreplace) /etc/php.d/exif.ini
%{_libdir}/php/extensions/%{apiver}/exif.so

%files cli

%files readline

%files devel

%files pdo
