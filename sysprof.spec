Summary:	Sampling CPU profiler for Linux
Summary(pl.UTF-8):	Próbkujący profiler procesora dla Linuksa
Name:		sysprof
Version:	1.2.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://sysprof.com/%{name}-%{version}.tar.gz
# Source0-md5:	a81808d847732f8dafb59d26ec2eebbf
URL:		http://sysprof.com/
BuildRequires:	binutils-devel
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 1:2.6.0
BuildRequires:	gtk+2-devel >= 1:2.6.1
BuildRequires:	libglade2-devel >= 2.0
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.217
Requires:	glib2 >= 1:2.6.0
Requires:	gtk+2 >= 1:2.6.1
Requires:	uname(release) >= 2.6.31
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sysprof is a sampling CPU profiler for Linux that uses a kernel module
to profile the entire system, not just a single application. Sysprof
handles shared libraries and applications do not need to be
recompiled. In fact they don't even have to be restarted.

Just insert the kernel module and start sysprof.

%description -l pl.UTF-8
Sysprof to próbkujący profiler procesora dla Linuksa wykorzystujący
moduł jądra do profilowania całego systemu, nie tylko pojedynczej
aplikacji. Sysprof obsługuje biblioteki współdzielone, a aplikacje nie
wymagają rekompilacji. Właściwie nawet nie trzeba ich restartować.

Wystarczy załadować moduł jądra i uruchomić sysprof.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	udevdir=/lib/udev/rules.d \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/sysprof
%attr(755,root,root) %{_bindir}/sysprof-cli
%{_pixmapsdir}/sysprof-icon-*.png
%{_datadir}/%{name}
/lib/udev/rules.d/60-sysprof.rules
