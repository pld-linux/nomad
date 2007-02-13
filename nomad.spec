Summary:	A network mapping and monitoring program
Summary(pl.UTF-8):	Program analizujący oraz monitorujący sieci
Name:		nomad
Version:	0.3.2
Release:	1
License:	GPL
Group:		Networking
Source0:	ftp://ftp.ncl.ac.uk/pub/local/npac/%{name}-%{version}.tar.gz
# Source0-md5:	905c638d103a9c00ba5b0401e97d3772
Patch0:		%{name}-desktop.patch
URL:		http://netmon.ncl.ac.uk/
BuildRequires:	ORBit-devel
BuildRequires:	GConf-devel >= 1.0.4
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdk-pixbuf-devel >= 0.10.1
BuildRequires:	gnome-libs-devel >= 1.0.4
BuildRequires:	libglade-devel
BuildRequires:	libglade-gnome-devel
BuildRequires:	libstdc++-devel
Requires:	fping
Requires:	net-snmp-utils
Requires(post):	/usr/X11R6/bin/gconftool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _sysconfdir     /etc/X11/GNOME

%description
Nomad is a network mapping program designed to automatically discover
a local network, using SNMP to identify network devices and work out
how they are physically connected together. The network is then
presented as a topology dia gram with simple integrated monitoring.

%description -l pl.UTF-8
Nomad to program zaprojektowany do automatycznego odkrywania sieci
lokalnej, używający SNMP do identyfikacji urządzeń sieciowych oraz
sprawdzania w jaki sposób są one fizycznie połączone. Sieć jest
prezentowana w postaci topologicznego diagramu dia z prostym
zintegrowanym monitorowaniem.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing aclocal.m4
%{__aclocal} -I macros
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-gnome
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	internetdir=%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
GCONF_CONFIG_SOURCE=`%{_bindir}/gconftool --get-default-source`; export GCONF_CONFIG_SOURCE
%{_bindir}/gconftool --shutdown
%{_bindir}/gconftool --makefile-install-rule %{_sysconfdir}/gconf/schemas/nomad.schemas
%{_bindir}/gconftool --shutdown

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/*/*.schemas
%{_desktopdir}/*.desktop
%{_datadir}/%{name}
%{_pixmapsdir}/*
