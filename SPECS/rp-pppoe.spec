Summary: A PPP over Ethernet client (for xDSL support)
Name: rp-pppoe
Version: 3.12
Release: 1%{?dist}
License: GPLv2+
Group: System Environment/Daemons
Url: http://www.roaringpenguin.com/pppoe/

Source0: http://www.roaringpenguin.com/files/download/%{name}-%{version}.tar.gz
Source1: pppoe-connect
Source2: pppoe-setup
Source3: pppoe-start
Source4: pppoe-status
Source5: pppoe-stop
Source6: pppoe-server.init

#Patch0: rp-pppoe-3.8-redhat.patch
# enable rp-pppoe plugin
#Patch1: rp-pppoe-3.10-plugin.patch
# fix build issue with kernel (without pppoe support)
#Patch2: rp-pppoe-3.10-build.patch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires(post): chkconfig initscripts fileutils
Requires(postun): chkconfig initscripts fileutils
Requires: ppp >= 2.4.2
Requires: initscripts >= 5.92
Requires: iproute >= 2.6
Requires: mktemp

BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: coreutils
BuildRequires: ppp ppp-devel

ExcludeArch: s390 s390x

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. This package contains the
Roaring Penguin PPPoE client, a user-mode program that does not
require any kernel modifications. It is fully compliant with RFC 2516,
the official PPPoE specification.

%prep
%setup -q

#%patch0 -p1 -b .config
#%patch1 -p1 -b .plugin
#%patch2 -p1 -b .build

%build
cd src
autoconf
export CFLAGS="%{optflags} -D_GNU_SOURCE -fno-strict-aliasing"
%configure --enable-plugin
make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/sbin
mkdir -p %{buildroot}%{_sysconfdir}/etc/rc.d/init.d

make -C src install DESTDIR=%{buildroot}

mv %{buildroot}%{_sbindir}/* %{buildroot}/sbin

install -m 0755 %{SOURCE1} %{buildroot}/sbin
install -m 0755 %{SOURCE2} %{buildroot}/sbin
install -m 0755 %{SOURCE3} %{buildroot}/sbin
install -m 0755 %{SOURCE4} %{buildroot}/sbin
install -m 0755 %{SOURCE5} %{buildroot}/sbin
install -m 0755 %{SOURCE6} %{buildroot}%{_sysconfdir}/rc.d/init.d/pppoe-server

pushd %{buildroot}%{_sbindir}
ln -s ../../sbin/* .
ln -s ../../sbin/pppoe-stop adsl-stop
ln -s ../../sbin/pppoe-start adsl-start
ln -s ../../sbin/pppoe-setup adsl-setup
popd

rm -rf %{buildroot}/etc/ppp/pppoe.conf \
       %{buildroot}/etc/rc.d/init.d/pppoe \
       %{buildroot}/usr/doc \
       %{buildroot}%{_sysconfdir}/ppp/plugins

# correct permissions
chmod 644 scripts/pppoe-status
chmod 755 %{buildroot}%{_sysconfdir}/ppp/firewall*

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add pppoe-server
exit 0

%preun
if [ "$1" = "0" ]; then
   /sbin/service pppoe-server stop > /dev/null 2>&1
   /sbin/chkconfig --del pppoe-server
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
   /sbin/service pppoe-server condrestart > /dev/null 2>&1
fi
exit 0


%triggerpostun -- rp-pppoe < 3.2-1
if [ -f /etc/rc.d/init.d/pppoe ]; then
   rm -f /etc/rc.d/init.d/pppoe
fi
exit 0

%triggerin -- rp-pppoe < 3.2-1
/sbin/service pppoe stop >/dev/null 2>&1 || true
/sbin/chkconfig --del pppoe >/dev/null 2>&1 || true

BOOT=""
DEVPATH=/etc/sysconfig/networking/devices
NETDEV=ifcfg-xDSL

[ -f /etc/ppp/pppoe.conf ] && CONFIG=/etc/ppp/pppoe.conf . /etc/ppp/pppoe.conf >/dev/null 2>&1
[ -n "$BOOT" ] || exit 0
[ -n "$DEVICE" ] || exit 0
[ -d $DEVPATH ] || mkdir -p $DEVPATH

touch $DEVPATH/$NETDEV && chmod 700 $DEVPATH/$NETDEV
echo "DEVICE=$DEVICE" >$DEVPATH/$NETDEV

[ -n "$BOOT" ] || BOOT=no
echo "ONBOOT=$BOOT" >>$DEVPATH/$NETDEV 

if [ "$USEPEERDNS" = "yes" ]; then
	echo "PEERDNS=yes" >>$DEVPATH/$NETDEV 
else
	echo "PEERDNS=no" >>$DEVPATH/$NETDEV 
fi

echo "DEFROUTE=yes" >>$DEVPATH/$NETDEV 
echo "TYPE=xDSL" >>$DEVPATH/$NETDEV 
echo "ETH=$ETH" >>$DEVPATH/$NETDEV 
echo "USER=$USER" >>$DEVPATH/$NETDEV 
echo "PASS=$PASS" >>$DEVPATH/$NETDEV 
echo "DEMAND=$DEMAND" >>$DEVPATH/$NETDEV 
echo "CONNECT_TIMEOUT=$CONNECT_TIMEOUT" >>$DEVPATH/$NETDEV 
echo "CONNECT_POLL=$CONNECT_POLL" >>$DEVPATH/$NETDEV 
echo "PING=\".\"" >>$DEVPATH/$NETDEV 
echo "SYNCHRONOUS=$SYNCHRONOUS" >>$DEVPATH/$NETDEV
echo "CLAMPMSS=$CLAMPMSS" >>$DEVPATH/$NETDEV
echo "LCP_INTERVAL=$LCP_INTERVAL" >>$DEVPATH/$NETDEV
echo "LCP_FAILURE=$LCP_FAILURE" >>$DEVPATH/$NETDEV
echo "PPPOE_TIMEOUT=$PPPOE_TIMEOUT" >>$DEVPATH/$NETDEV
echo "FIREWALL=$FIREWALL" >>$DEVPATH/$NETDEV
echo "PPPOE_EXTRA=$PPPOE_EXTRA" >>$DEVPATH/$NETDEV
echo "PIDFILE=/var/run/pppoe-adsl.pid" >>$DEVPATH/$NETDEV
echo "SERVICENAME=$SERVICENAME" >>$DEVPATH/$NETDEV
echo "ACNAME=$ACNAME" >>$DEVPATH/$NETDEV

pushd /etc/sysconfig/network-scripts
ln -f ../networking/devices/$NETDEV ifcfg-$DEVICE
popd

exit 0

%files
%defattr(-,root,root)
%doc doc/LICENSE scripts/pppoe-connect scripts/pppoe-setup scripts/pppoe-init
%doc scripts/pppoe-start scripts/pppoe-status scripts/pppoe-stop
%doc configs
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%{_mandir}/man?/*
%{_sysconfdir}/ppp/firewall*
%{_sysconfdir}/rc.d/init.d/*
/sbin/*
%{_sbindir}/*

%changelog
* Mon Feb 29 2016 Than Ngo <than@redhat.com> - 3.10-16
- add missing BR on ppp-devel

* Fri Feb 12 2016 Than Ngo <than@redhat.com> - 3.10-15
- Resolves: bz#1182080, disable it again

* Wed Jan 27 2016 Than Ngo <than@redhat.com> - 3.10-14
- Resolves: bz#841194, enable rp-pppoe plugin

* Fri Nov 27 2015 Than Ngo <than@redhat.com> - 3.10-13
- Resolves: bz#746579, handle default route and ip-down.local correctly

* Fri Nov 20 2015 Than Ngo <than@redhat.com> - 3.10-12
- Resolves: bz#1182080, build rp-pppoe also for s390 and s390x

* Fri Apr 11 2014 Than Ngo <than@redhat.com> - 3.10-11
- Resolves: bz#1009268, add symlink adsl-setup

* Thu Jun 13 2013 Than Ngo <than@redhat.com> - 3.10-10
- fix file permission

* Wed Jun 12 2013 Than Ngo <than@redhat.com> - 3.10-9
- Resolves: bz#841190, pppoe-server enabled by default

* Tue Jun 29 2010 Than Ngo <than@redhat.com> - 3.10-8
- Resolves: bz#596206, rebuid with -fno-strict-aliasing

* Fri Feb 19 2010 Than Ngo <than@redhat.com> - 3.10-7
- peer review: fix rpmlint Errors

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 3.10-6
- rebuilt

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 3.10-5
- wrong path to initscript bz#522010
- add remove services in %%postun/%%preun

* Mon Sep 07 2009 Than Ngo <than@redhat.com> - 3.10-4
- add feature, save and restore all information about default routes bz#191242
- add startup script for pppoe-server bz#507123

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 3.10-1
- 3.10

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.8-5
- fix license tag

* Thu Apr 10 2008 Karsten Hopp <karsten@redhat.com> 3.8-4
- Build with $RPM_OPT_FLAGS (#249978) (Ville Skyttä)

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 3.8-3
- rebuild

* Tue Mar 20 2007 Than Ngo <than@redhat.com> - 3.8-2.fc7
- setting DEBUG for adsl-start causes adsl-connect to exit, #195828

* Tue Mar 20 2007 Than Ngo <than@redhat.com> - 3.8-1.fc7
- update to 3.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.5-32.1
- rebuild

* Sat Jun 10 2006 Than Ngo <than@redhat.com> 3.5-32
- fix build problem in mock

* Wed Feb 15 2006 Than Ngo <than@redhat.com> 3.5-31
- apply patch to use mktemp

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.5-30.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.5-30.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 15 2005 Than Ngo <than@redhat.com> 3.5-30
- defaultroute should not overridden #152014

* Mon Jul 04 2005 Than Ngo <than@redhat.com> 3.5-29 
- fix broken dependencies 

* Mon Jun 13 2005 Than Ngo <than@redhat.com> 3.5-28
- use iproute2 instead of old ifconfig #134816

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.5-27
- rebuilt

* Sat Jan 22 2005 Than Ngo <than@redhat.com> 3.5-26
- rename config files #145255

* Wed Jan 19 2005 David Woodhouse <dwmw2@redhat.com> 3.5-25
- Kill br2684ctl after ifdown if we started it

* Wed Jan 19 2005 David Woodhouse <dwmw2@redhat.com> 3.5-24
- Add support for RFC2684 Ethernet-over-ATM (for PPPoE-over-ATM)

* Mon Nov 22 2004 Than Ngo <than@redhat.com> 3.5-23
- fix typo in adsl-setup #140287

* Fri Oct 15 2004 Than Ngo <than@redhat.com> 3.5-22
- Fix ip conflict in dsl connect, #135012

* Thu Oct 07 2004 David Woodhouse <dwmw2@redhat.com> 3.5-21
- Fix ordering of VCI and VPI in pppoatm address.

* Thu Oct 07 2004 David Woodhouse <dwmw2@redhat.com> 3.5-20
- Add support for static IP with demand option.
- Add support for using PPP over ATM plugin.

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 3.5-19
- fix typo bug in adsl connect
- remove unused rp-pppoe plugin, it's now included in new ppppd

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 3.5-18
- fix adsl connect for using MTU/MRU

* Thu Sep 30 2004 Than Ngo <than@redhat.com> 3.5-17
- fix idle parameter in asdl connect

* Mon Aug 02 2004 Than Ngo <than@redhat.com> 3.5-16
- use iptables instead ipchains, thanks to Robert Scheck

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 01 2004 Than Ngo <than@redhat.com> 3.5-14
- fixed typo 

* Tue Mar 30 2004 Than Ngo <than@redhat.com> 3.5-13
- fixed reconnect problem

* Mon Mar 29 2004 Than Ngo <than@redhat.com> 3.5-12
- fixed wrong idle parameter, #119280

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 3.5-11
- fixed default route problem, #114875
- fixed restart issue, #100610
- fixed a bug in adsl status

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 10 2003 Than Ngo <than@redhat.com> 3.5-9
- better fix for nickename issue

* Wed Oct 29 2003 Than Ngo <than@redhat.com> 3.5-8
- fix a bug in connect script

* Mon Oct 27 2003 Than Ngo <than@redhat.com> 3.5-7
- fix nickename issue

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Than Ngo <than@redhat.com> 3.5-5
- add correct PPOE_TIMEOUT/LCP_INTERVAL bug #82630

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix initdir in triggerpostun

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Than Ngo <than@redhat.com> 3.5-1
- update to 3.5

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.4-8
- unpackaged files issue

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Than Ngo <than@redhat.com> 3.4-5
- Don't forcibly strip binaries

* Sun Jun 09 2002 Than Ngo <than@redhat.com> 3.4-4
- Fix up creation of first device (#64773)

* Fri Jun 07 2002 Than Ngo <than@redhat.com> 3.4-3
- set correct default value for PPPoE timeout (bug #64903)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 3.4-1
- 3.4
- added kernel plugin

* Sun Apr 14 2002 Than Ngo <than@redhat.com> 3.3-7
- add fix for neat-control

* Sat Feb 23 2002 Than Ngo <than@redhat.com> 3.3-6
- fix a bug in adsl-stop (#60138)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.3-5
- Fix up creation of first device (#59236)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Dec 16 2001 Than Ngo <than@redhat.com> 3.3-3
- fix bugs #57070, #55627, #55140
- add man pages, Docs and example scripts

* Mon Nov 05 2001 Than Ngo <than@redhat.com> 3.3-2
- fix a bug in adsl-connect

* Wed Sep 19 2001 Than Ngo <than@redhat.com> 3.3-1
- update to 3.3 (bug #53697)

* Thu Aug 16 2001 Than Ngo <than@redhat.com> 3.2-4
- don't print messages as default

* Wed Aug  8 2001 Than Ngo <than@redhat.com>
- fix softlinks

* Sun Jul 22 2001 Than Ngo <than@redhat.com>
- update to 3.2

* Thu Jul 19 2001 Than Ngo <than@redhat.com> 3.0-5
- fix bug in trigger

* Fri Jun 22 2001 Than Ngo <than@redhat.com>
- Copyright -> License
- fix activate ethernet device problem
- get rid of pppoe initscript, use ifup/ifdown
  to activate/shutdown xDSL connection
- convert old pppoe config format into new format
- remove adsl-setup, Users have to use netconf to setup xDSL connection
- excludearch s390

* Mon May 14 2001 Than Ngo <than@redhat.com>
- clean PID files when connection fails (Bug #40349)
- fix order of pppoe script (Bug #40454)

* Wed May 02 2001 Than Ngo <than@redhat.com>
- fixed a firewall bug in adsl-setup (Bug #38550)

* Sun Apr 22 2001 Than Ngo <than@redhat.com>
- update to 3.0 (bug #34075)

* Thu Mar 15 2001 Than Ngo <than@redhat.com>
- fix BOOT enviroment again, it should work fine now 

* Wed Mar 14 2001 Than Ngo <than@redhat.com>
- fix bug in adsl-setup (DEVICE enviroment)

* Thu Feb 08 2001 Than Ngo <than@redhat.com>
- fixed a problem in startup (Bug #26454)
- fixed i18n in initscript (Bug #26540)

* Sat Feb 03 2001 Than Ngo <than@redhat.com>
- updated to 2.6
- some fixes in pppoe script

* Fri Feb 02 2001 Than Ngo <than@redhat.com>
- fixed starting pppoe service at boot time. (Bug #25494)

* Sun Jan 28 2001 Than Ngo <than@redhat.com>
- fixed so that pppoe script does not kill adsl connection when
  the runlevel is changed. 
- remove excludearch ia64

* Tue Jan 23 2001 Than Ngo <than@redhat.com>
- hacked for using USEPEERDNS

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- updated to 2.5, it fixes a denial-of-service vulnerability

* Tue Aug 08 2000 Than Ngo <than@redhat.de>
- fix german configuration HOWTO to T-DSL

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- fixes for starting pppd under /usr/sbin
- added german configuration HOWTO to T-DSL

* Tue Aug 01 2000 Than Ngo <than@redhat.de>
- update to 2.2

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- fixed initscripts so that condrestart doesn't return 1 when the test fails

* Thu Jul 27 2000 Than Ngo <than@redhat.de>
- update to 2.1
- don't detect pppd for building

* Thu Jul 27 2000 Than Ngo <than@redhat.de>
- rename the rp-pppoe startup script (Bug #14734)

* Wed Jul 26 2000 Bill Nottingham <notting@redhat.com>
- don't run by default; it hangs if not configured

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- prereq /etc/init.d (it's referenced in the initscript)

* Tue Jul 18 2000 Than Ngo <than@redhat.de>
- inits back to rc.d/init.d, using service to fire them up

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul 08 2000 Than Ngo <than@redhat.de>
- add Prereq: /etc/init.d

* Fri Jun 30 2000 Than Ngo <than@redhat.de>
- turned off deamon by default

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- add condrestart directive
- fix post/preun/postun scripts
- prereq initscripts >= 5.20

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- use RPM macros
- rebuilt in the new build environment

* Wed May 31 2000 Than Ngo <than@redhat.de> 
- adopted for Winston.
