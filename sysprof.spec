#
# Conditional build:
%bcond_without	sysprofd	# daemon to run UI without root permissions
#
Summary:	Sampling CPU profiler for Linux
Summary(pl.UTF-8):	Próbkujący profiler procesora dla Linuksa
Name:		sysprof
Version:	3.36.0
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sysprof/3.36/%{name}-%{version}.tar.xz
# Source0-md5:	3956e82b8744715006dde59e0ce8910b
Patch0:		%{name}-types.patch
URL:		http://sysprof.com/
# -std=gnu11 + C11 atomics
BuildRequires:	gcc >= 6:4.9
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.61.3
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libdazzle-devel >= 3.30.0
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	meson >= 0.50.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.22
%{?with_sysprofd:BuildRequires:	polkit-devel >= 0.114}
BuildRequires:	rpmbuild(macros) >= 1.736
%{?with_sysprofd:BuildRequires:	systemd-devel >= 1:222}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
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
Requires:	glib2 >= 1:2.61.3

%description libs
The sysprof profiler library.

%description libs -l pl.UTF-8
Biblioteka profilera sysprof.

%package devel
Summary:	Header files for sysprof library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sysprof
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.61.3
Obsoletes:	sysprof-static < 3.28.0

%description devel
Header files for sysprof library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sysprof.

%package ui
Summary:	The sysprof graphical user interface
Summary(pl.UTF-8):	Graficzny interfejs użytkownika profilera sysprof
Group:		Applications/System
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.61.3
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-ui-libs = %{version}-%{release}
Requires:	hicolor-icon-theme
Requires:	shared-mime-info

%description ui
The sysprof graphical user interface.

%description ui -l pl.UTF-8
Graficzny interfejs użytkownika profilera sysprof.

%package ui-libs
Summary:	The sysprof library containing reusable GTK+ widgets
Summary(pl.UTF-8):	Biblioteka sysprofa zawierająca widgety GTK+ wielokrotnego użytku
Group:		X11/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3 >= 3.22
Requires:	libdazzle >= 3.30.0

%description ui-libs
The sysprof library containing reusable GTK+ widgets.

%description ui-libs -l pl.UTF-8
Biblioteka sysprofa zawierająca widgety GTK+ wielokrotnego użytku.

%package ui-devel
Summary:	Header files for sysprof-ui library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sysprof-ui
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-ui-libs = %{version}-%{release}
Requires:	gtk+3-devel >= 3.22
Obsoletes:	sysprof-ui-static < 3.28.0

%description ui-devel
Header files for sysprof-ui library.

%description ui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sysprof-ui.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
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
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%postun ui
%glib_compile_schemas
%update_icon_cache hicolor
%update_mime_database
%update_desktop_database

%post	ui-libs -p /sbin/ldconfig
%postun	ui-libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS DESIGN.md NEWS README.md
%attr(755,root,root) %{_bindir}/sysprof-cli
%if %{with sysprofd}
%attr(755,root,root) %{_libexecdir}/sysprofd
%{systemdunitdir}/sysprof2.service
%{systemdunitdir}/sysprof3.service
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof2.service
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof3.service
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof2.conf
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof3.conf
%{_datadir}/polkit-1/actions/org.gnome.sysprof3.policy
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-3.so
%attr(755,root,root) %{_libdir}/libsysprof-memory-3.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsysprof-capture-3.a
%dir %{_includedir}/sysprof-3
%{_includedir}/sysprof-3/sysprof.h
%{_includedir}/sysprof-3/sysprof-address.h
%{_includedir}/sysprof-3/sysprof-battery-source.h
%{_includedir}/sysprof-3/sysprof-callgraph-profile.h
%{_includedir}/sysprof-3/sysprof-capture*.h
%{_includedir}/sysprof-3/sysprof-check.h
%{_includedir}/sysprof-3/sysprof-clock.h
%{_includedir}/sysprof-3/sysprof-collector.h
%{_includedir}/sysprof-3/sysprof-control-source.h
%{_includedir}/sysprof-3/sysprof-diskstat-source.h
%{_includedir}/sysprof-3/sysprof-elf-symbol-resolver.h
%{_includedir}/sysprof-3/sysprof-gjs-source.h
%{_includedir}/sysprof-3/sysprof-governor-source.h
%{_includedir}/sysprof-3/sysprof-hostinfo-source.h
%{_includedir}/sysprof-3/sysprof-jitmap-symbol-resolver.h
%{_includedir}/sysprof-3/sysprof-kernel-symbol.h
%{_includedir}/sysprof-3/sysprof-kernel-symbol-resolver.h
%{_includedir}/sysprof-3/sysprof-local-profiler.h
%{_includedir}/sysprof-3/sysprof-memory-source.h
%{_includedir}/sysprof-3/sysprof-memprof-profile.h
%{_includedir}/sysprof-3/sysprof-memprof-source.h
%{_includedir}/sysprof-3/sysprof-model-filter.h
%{_includedir}/sysprof-3/sysprof-netdev-source.h
%{_includedir}/sysprof-3/sysprof-perf-counter.h
%{_includedir}/sysprof-3/sysprof-perf-source.h
%{_includedir}/sysprof-3/sysprof-platform.h
%{_includedir}/sysprof-3/sysprof-proc-source.h
%{_includedir}/sysprof-3/sysprof-process-model.h
%{_includedir}/sysprof-3/sysprof-process-model-item.h
%{_includedir}/sysprof-3/sysprof-profile.h
%{_includedir}/sysprof-3/sysprof-profiler.h
%{_includedir}/sysprof-3/sysprof-proxy-source.h
%{_includedir}/sysprof-3/sysprof-selection.h
%{_includedir}/sysprof-3/sysprof-source.h
%{_includedir}/sysprof-3/sysprof-spawnable.h
%{_includedir}/sysprof-3/sysprof-symbol-resolver.h
%{_includedir}/sysprof-3/sysprof-symbols-source.h
%{_includedir}/sysprof-3/sysprof-tracefd-source.h
%{_includedir}/sysprof-3/sysprof-version.h
%{_includedir}/sysprof-3/sysprof-version-macros.h
%{_pkgconfigdir}/sysprof-3.pc
%{_pkgconfigdir}/sysprof-capture-3.pc
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof2.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Profiler.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Sysprof3.Service.xml

%files ui -f %{name}-ui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sysprof
%{_datadir}/glib-2.0/schemas/org.gnome.sysprof3.gschema.xml
%{_datadir}/metainfo/org.gnome.Sysprof3.appdata.xml
%{_datadir}/mime/packages/sysprof-mime.xml
%{_desktopdir}/org.gnome.Sysprof3.desktop
%{_iconsdir}/hicolor/scalable/actions/sysprof-*.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Sysprof.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Sysprof-symbolic.svg

%files ui-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-ui-3.so

%files ui-devel
%defattr(644,root,root,755)
%{_includedir}/sysprof-3/sysprof-display.h
%{_includedir}/sysprof-3/sysprof-notebook.h
%{_includedir}/sysprof-3/sysprof-page.h
%{_includedir}/sysprof-3/sysprof-process-model-row.h
%{_includedir}/sysprof-3/sysprof-ui.h
%{_includedir}/sysprof-3/sysprof-visualizer.h
%{_includedir}/sysprof-3/sysprof-visualizer-group.h
%{_includedir}/sysprof-3/sysprof-zoom-manager.h
%{_pkgconfigdir}/sysprof-ui-3.pc
