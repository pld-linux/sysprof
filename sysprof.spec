# TODO: switch to gtk4-update-icon-cache
#
# Conditional build:
%bcond_without	sysprofd	# daemon to run UI without root permissions
#
Summary:	Sampling CPU profiler for Linux
Summary(pl.UTF-8):	Próbkujący profiler procesora dla Linuksa
Name:		sysprof
Version:	45.2
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	https://download.gnome.org/sources/sysprof/45/%{name}-%{version}.tar.xz
# Source0-md5:	6c77d06d8bde15e74e9b2aaf3ea6ef9a
Patch0:		no-cache-update.patch
URL:		http://www.sysprof.com/
BuildRequires:	cairo-devel
# -std=gnu11 + C11 atomics
BuildRequires:	gcc >= 6:4.9
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.76.0
BuildRequires:	gtk4-devel >= 4.10
BuildRequires:	json-glib-devel
BuildRequires:	libadwaita-devel >= 1.2
BuildRequires:	libdex-devel >= 0.3
BuildRequires:	libpanel-devel >= 1.3.0
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libunwind-devel
BuildRequires:	meson >= 0.62.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.22
%{?with_sysprofd:BuildRequires:	polkit-devel >= 0.114}
BuildRequires:	rpmbuild(macros) >= 1.736
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
Requires:	glib2 >= 1:2.76.0
Requires:	libdex >= 0.3
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
Requires:	glib2-devel >= 1:2.76.0
Requires:	json-glib-devel
Requires:	libdex-devel >= 0.3
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
Requires(post,postun):	glib2 >= 1:2.76.0
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	gtk4 >= 4.10
Requires:	hicolor-icon-theme
Requires:	libpanel >= 1.3.0
Requires:	shared-mime-info

%description ui
The sysprof graphical user interface.

%description ui -l pl.UTF-8
Graficzny interfejs użytkownika profilera sysprof.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	--default-library=shared \
	%{!?with_sysprofd:-Dwith_sysprofd=host}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%doc AUTHORS DESIGN.md NEWS README.md
%attr(755,root,root) %{_bindir}/sysprof-agent
%attr(755,root,root) %{_bindir}/sysprof-cli
%if %{with sysprofd}
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
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Profiler.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Service.xml

%files ui -f %{name}-ui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sysprof
%{_datadir}/metainfo/org.gnome.Sysprof.appdata.xml
%{_datadir}/mime/packages/sysprof-mime.xml
%{_desktopdir}/org.gnome.Sysprof.desktop
%{_iconsdir}/hicolor/scalable/actions/sysprof-*.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Sysprof.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Sysprof-symbolic.svg
