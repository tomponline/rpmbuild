%global major 0
%global minor 044

Name:               peervpn
Version:            %{major}.%{minor}
Release:            1
Summary:            A VPN software using full mesh network topology

Group:              Applications/Internet
License:            GPLv3+
URL:                http://www.peervpn.net/
Source0:            http://www.peervpn.net/files/peervpn-%{major}-%{minor}.tar.gz

BuildRequires:      openssl-devel
BuildRequires:      upstart
# for /usr/sbin/ip
Requires:           iproute
# for /usr/sbin/ifconfig
Requires:           net-tools

%description
PeerVPN is software that builds virtual Ethernet networks between multiple
computers. It uses full mesh network topology and can automatically build
tunnels through firewalls and NATs. It supports shared key encryption and
authentication.

%prep
%setup -q -n peervpn-%{major}-%{minor}

%build
make

%install
rm -rf %{buildroot}
install -D -m 0755 peervpn %{buildroot}%{_sbindir}/%{name}
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}
install -D -m 0600 peervpn.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

%files
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
