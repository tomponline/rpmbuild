%define contentdir /var/www

Summary: Apache HTTP Server
Name: httpd
Version: 2.2.23
Release: 3
URL: http://httpd.apache.org/
Source0: http://www.apache.org/dist/httpd/httpd-%{version}.tar.gz
Source1: httpd.init
Source2: httpd.logrotate
Source3: httpd.sysconf
Source4: httpd.conf
Source5: httpd_syslog
Source6: httpd.syslog.conf
Source8: httpd.ssl.conf
Source14: httpd.errors.conf
Source16: httpd.mpmprefork.conf
Source17: httpd.apachectl
Source18: httpd.vhosts.conf

License: Apache Software License
Group: System Environment/Daemons
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: gcc, binutils, libtool
BuildRequires: expat-devel, findutils, zlib-devel, db4-devel, openssl-devel, distcache-devel, pcre-devel
Requires: /etc/mime.types, gawk, /usr/share/magic.mime, /usr/bin/find
Requires: initscripts >= 8.36, mailcap, db4, openssl
Prereq: /sbin/chkconfig, /bin/mktemp, /bin/rm, /bin/mv, /bin/cat
Prereq: sh-utils, textutils, /usr/sbin/useradd, file
Provides: httpd-common, httpd-mmn, mod_ssl, httpd-devel, apr-devel, apr
Obsoletes: httpd-common, httpd-mmn, mod_ssl, apr-devel, apr

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%prep
%setup -q

%build

CFLAGS="$RPM_OPT_FLAGS -fPIC"
SH_LDFLAGS="-Wl,-z,relro"
export CFLAGS SH_LDFLAGS

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

function mpmbuild()
{
mpm=$1; shift
./configure  \
        --enable-layout=RedHat \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir}/httpd/modules \
        --with-mpm=$mpm \
        --enable-pie \
        --enable-so \
        --with-included-apr \
	--with-pcre \
        --with-berkeley-db \
	--disable-userdir \
        --disable-authn-dbd \
	--disable-proxy-ftp \
        --disable-proxy-ajp \
	$*
make %{?_smp_mflags}
}

#Build HTTPD prefork mpm binary and shared modules
mpmbuild prefork \
	--enable-ssl=shared \
        --enable-deflate=shared \
        --enable-expires=shared \
        --enable-rewrite=shared \
        --enable-headers=shared \
        --enable-rewrite=shared \
        --enable-unique-id=shared \
        --enable-proxy=shared \
        --enable-proxy-http=shared \
        --enable-proxy-connect=shared \
        --enable-proxy-balancer=shared \
        --enable-file-cache=shared \
        --enable-cache=shared \
        --enable-disk-cache=shared \
        --enable-mem-cache=shared \
        --enable-distcache \
	--enable-dav=shared \
        --enable-static-htcacheclean 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

#Install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -m 644 $RPM_SOURCE_DIR/httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

#Install sysconfig file
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 $RPM_SOURCE_DIR/httpd.sysconf $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/httpd

#Make HTML directory
install -m 755 -d $RPM_BUILD_ROOT/%{contentdir}/html

#Create symlinks for /etc/httpd
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/run $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# Install SYSV init stuff
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 $RPM_SOURCE_DIR/httpd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/httpd

#Install custom apachectl script for multiple MPMs
install -m 755 $RPM_SOURCE_DIR/httpd.apachectl $RPM_BUILD_ROOT/usr/sbin/apachectl

#Install prefork
install -m 644 $RPM_SOURCE_DIR/httpd.mpmprefork.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/prefork.conf

# Install logging stuff
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 $RPM_SOURCE_DIR/httpd.logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/httpd
install -m 755 $RPM_SOURCE_DIR/httpd_syslog $RPM_BUILD_ROOT/usr/bin/httpd_syslog
install -m 644 $RPM_SOURCE_DIR/httpd.syslog.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/syslog.conf

#Install SSL config 
install -m 644 $RPM_SOURCE_DIR/httpd.ssl.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/ssl.conf

#Install main modules config
echo "LoadModule expires_module       modules/mod_expires.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/modules.conf
echo "LoadModule deflate_module       modules/mod_deflate.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/modules.conf
echo "LoadModule headers_module       modules/mod_headers.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/modules.conf
echo "LoadModule rewrite_module       modules/mod_rewrite.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/modules.conf

#Install unique config
echo "#LoadModule unique_id_module      modules/mod_unique_id.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/unique.conf

#Install proxy config
echo "#LoadModule proxy_module        modules/mod_proxy.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf
echo "#LoadModule proxy_http_module   modules/mod_proxy_http.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf
echo "#LoadModule proxy_connect_module	modules/mod_proxy_connect.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf
echo "#LoadModule proxy_balancer_module  modules/mod_proxy_balancer.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf

#Install default secure proxy config
echo "<IfModule proxy_module>" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf
echo "ProxyRequests Off" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf
echo "</IfModule>" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/proxy.conf

#Install cache config
echo "#LoadModule cache_module        modules/mod_cache.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/cache.conf
echo "#LoadModule disk_cache_module        modules/mod_disk_cache.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/cache.conf
echo "#LoadModule file_cache_module        modules/mod_file_cache.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/cache.conf
echo "#LoadModule mem_cache_module        modules/mod_mem_cache.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/cache.conf

#Install webdav config
echo "#LoadModule dav_module         modules/mod_dav.so" >> $RPM_BUILD_ROOT/etc/httpd/conf.d/dav.conf

#Install custom error pages
install -m 644 $RPM_SOURCE_DIR/httpd.errors.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/errors.conf

#Install vhost config file
install -d -m 755 $RPM_BUILD_ROOT/home/vhosts
install -m 644 $RPM_SOURCE_DIR/httpd.vhosts.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/vhosts.conf

#Clean up rubbish
rm -rf $RPM_BUILD_ROOT/%{contentdir}/cgi-bin
rm -rf $RPM_BUILD_ROOT/%{contentdir}/icons
rm -rf $RPM_BUILD_ROOT/%{contentdir}/manual
rm -rf $RPM_BUILD_ROOT/%{contentdir}/html/*
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf/extra
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf/original

#Add a blank index file
touch $RPM_BUILD_ROOT/%{contentdir}/html/index.html

%pre
# Add the "apache" user
/usr/sbin/useradd -c "Apache" -u 48 \
        -s /sbin/nologin -r -d %{contentdir} apache 2> /dev/null || :

%preun
if [ $1 = 0 ]; then
        /sbin/service httpd stop > /dev/null 2>&1
        /sbin/chkconfig --del httpd
fi

%post
# Register the httpd service
/sbin/chkconfig --add httpd
/sbin/chkconfig httpd on

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/httpd
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%config(noreplace) %{_sysconfdir}/httpd/conf/mime.types
%config(noreplace) %{_sysconfdir}/sysconfig/httpd
%{contentdir}/error
%dir /var/log/httpd
%dir /home/vhosts
%dir %{contentdir}/html
%{contentdir}/build
%config(noreplace) %{contentdir}/html/index.html
%dir /etc/httpd/conf
%dir /etc/httpd/conf.d
%config(noreplace) %{_sysconfdir}/httpd/conf.d/syslog.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/modules.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/proxy.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/cache.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/unique.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/errors.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/prefork.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/dav.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/vhosts.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/httpd
/usr
/etc/httpd/logs
/etc/httpd/modules
/etc/httpd/run
