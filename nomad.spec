Summary:	A network mapping and monitoring program
Summary(pl):	Program analizuj±cy oraz monitoruj±cy sieci
Name:		nomad
Version:	0.3.1
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.ncl.ac.uk/pub/local/npac/%{name}-%{version}.tar.gz
Patch0:		%{name}-path.patch
URL:		http://netmon.ncl.ac.uk/
BuildRequires:	ORBit-devel
BuildRequires:	GConf-devel >= 1.0.4
BuildRequires:	gdk-pixbuf-devel >= 0.10.1
BuildRequires:	libglade-devel
BuildRequires:	gnome-libs-devel >= 1.0.4
BuildRequires:	libstdc++-devel
Requires:	fping
Requires:	ucd-snmp-utils
Requires(post):	/usr/X11R6/bin/gconftool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define         _sysconfdir     /etc/X11/GNOME

%description
Nomad is a network mapping program designed to automatically discover
a local network, using SNMP to identify network devices and work out
how they are physically connected together. The network is then
presented as a topology dia gram with simple integrated monitoring.

%description -l pl
Nomad to program zaprojektowany do automatycznego odkrywania sieci
lokalnej, u¿ywaj±cy SNMP do indentyfikacji urz±dzeñ sieciowych oraz
sprawdzania w jaki sposób s± one fizycznie po³aczone. Sieæ jest
prezentowana w postaci topologicznego diagramu dia z prostym
zintegroawnym monitorowaniem.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-gnome
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	internetdir=%{_applnkdir}/Network/Misc

gzip -9nf AUTHORS README

%clean
rm -rf $RPM_BUILD_ROOT

%post
GCONF_CONFIG_SOURCE=`%{_bindir}/gconftool --get-default-source`; export GCONF_CONFIG_SOURCE
%{_bindir}/gconftool --shutdown
%{_bindir}/gconftool --makefile-install-rule %{_sysconfdir}/gconf/schemas/nomad.schemas
%{_bindir}/gconftool --shutdown                                                            

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/*/*.schemas
%{_applnkdir}/Network/Misc/*.desktop
%{_datadir}/%{name}
%{_pixmapsdir}/*
