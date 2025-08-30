# TODO: switch to gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	debuginfod	# debuginfod integration
%bcond_without	sysprofd	# daemon to run UI without root permissions
#
Summary:	Sampling CPU profiler for Linux
Summary(pl.UTF-8):	Próbkujący profiler procesora dla Linuksa
Name:		sysprof
Version:	48.1
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	https://download.gnome.org/sources/sysprof/48/%{name}-%{version}.tar.xz
# Source0-md5:	18095080186a821ac80ecebff5ab94b4
Patch0:		no-cache-update.patch
URL:		https://www.sysprof.com/
BuildRequires:	cairo-devel
# -std=gnu17
BuildRequires:	gcc >= 6:7
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.80.0
BuildRequires:	gtk4-devel >= 4.15
%{?with_debuginfod:BuildRequires:	elfutils-debuginfod-devel}
BuildRequires:	json-glib-devel
BuildRequires:	libadwaita-devel >= 1.2
BuildRequires:	libdex-devel >= 0.9
BuildRequires:	libpanel-devel >= 1.3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libunwind-devel
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	polkit-devel >= 0.114
BuildRequires:	rpmbuild(macros) >= 2.042
%{?with_sysprofd:BuildRequires:	systemd-devel >= 1:222}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
%{?with_sysprofd:Requires:	polkit >= 0.114}
%{?with_sysprofd:Requires:	systemd-units >= 1:222}
Requires:	uname(release) >= 2.6.31
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

%package libs
Summary:	The sysprof profiler library
Summary(pl.UTF-8):	Biblioteka profilera sysprof
Group:		Libraries
Requires:	glib2 >= 1:2.80.0
Requires:	libdex >= 0.9
Obsoletes:	sysprof-ui-libs < 45

%description libs
The sysprof profiler library.

%description libs -l pl.UTF-8
Biblioteka profilera sysprof.

%package devel
Summary:	Header files for sysprof library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sysprof
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.80.0
Requires:	json-glib-devel
Requires:	libdex-devel >= 0.9
%{?with_sysprofd:Requires:	polkit-devel >= 0.114}
%{?with_sysprofd:Requires:	systemd-devel >= 1:222}
Obsoletes:	sysprof-static < 3.28.0
Obsoletes:	sysprof-ui-devel < 45

%description devel
Header files for sysprof library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sysprof.

%package ui
Summary:	The sysprof graphical user interface
Summary(pl.UTF-8):	Graficzny interfejs użytkownika profilera sysprof
Group:		Applications/System
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.80.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	gtk4 >= 4.15
Requires:	hicolor-icon-theme
Requires:	libpanel >= 1.3.0
Requires:	shared-mime-info

%description ui
The sysprof graphical user interface.

%description ui -l pl.UTF-8
Graficzny interfejs użytkownika profilera sysprof.

%prep
%setup -q
%patch -P0 -p1

%build
%meson \
	--default-library=shared \
	-Ddebuginfod=%{__enabled_disabled debuginfod} \
	-Dpolkit-agent=enabled \
	%{!?with_sysprofd:-Dsysprofd=host}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%find_lang %{name} -o %{name}-ui.lang --with-gnome --without-mo
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with sysprofd}
%post
%systemd_post sysprof2.service

%preun
%systemd_preun sysprof2.service

%postun
%systemd_reload
%endif

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post ui
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%postun ui
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_bindir}/sysprof-agent
%attr(755,root,root) %{_bindir}/sysprof-cat
%attr(755,root,root) %{_bindir}/sysprof-cli
%if %{with sysprofd}
%attr(755,root,root) %{_libexecdir}/sysprof-live-unwinder
%attr(755,root,root) %{_libexecdir}/sysprofd
%{systemdunitdir}/sysprof3.service
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof3.service
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof3.conf
%{_datadir}/polkit-1/actions/org.gnome.sysprof3.policy
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-6.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsysprof-6.so.6
%attr(755,root,root) %{_libdir}/libsysprof-memory-6.so
%attr(755,root,root) %{_libdir}/libsysprof-speedtrack-6.so
%attr(755,root,root) %{_libdir}/libsysprof-tracer-6.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-6.so
%{_libdir}/libsysprof-capture-4.a
%{_includedir}/sysprof-6
%{_pkgconfigdir}/sysprof-6.pc
%{_pkgconfigdir}/sysprof-capture-4.pc
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof.Agent.xml
%if %{with sysprofd}
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Profiler.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Service.xml
%endif

%files ui -f %{name}-ui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sysprof
%{_datadir}/metainfo/org.gnome.Sysprof.appdata.xml
%{_datadir}/mime/packages/sysprof-mime.xml
%{_desktopdir}/org.gnome.Sysprof.desktop
%{_iconsdir}/hicolor/scalable/actions/sysprof-*.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Sysprof.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Sysprof-symbolic.svg
