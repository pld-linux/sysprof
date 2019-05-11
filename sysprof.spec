#
# Conditional build:
%bcond_without	sysprofd	# daemon to run UI without root permissions
#
Summary:	Sampling CPU profiler for Linux
Summary(pl.UTF-8):	Próbkujący profiler procesora dla Linuksa
Name:		sysprof
Version:	3.32.0
Release:	1
License:	GPL v3+
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sysprof/3.32/%{name}-%{version}.tar.xz
# Source0-md5:	d1fa9ad216419d722770ca36713ad3af
URL:		http://sysprof.com/
BuildRequires:	appstream-glib-devel
# -std=gnu11 + C11 atomics
BuildRequires:	gcc >= 6:4.9
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools >= 0.19.6
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.42.0
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	libstdc++-devel >= 6:4.3
BuildRequires:	pango-devel
BuildRequires:	pkgconfig >= 1:0.22
%{?with_sysprofd:BuildRequires:	polkit-devel}
BuildRequires:	rpmbuild(macros) >= 1.644
%{?with_sysprofd:BuildRequires:	systemd-devel >= 1:222}
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	%{name}-libs = %{version}-%{release}
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
Requires:	glib2 >= 1:2.44.0

%description libs
The sysprof profiler library.

%description libs -l pl.UTF-8
Biblioteka profilera sysprof.

%package devel
Summary:	Header files for sysprof library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki sysprof
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0

%description devel
Header files for sysprof library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sysprof.

%package ui
Summary:	The sysprof graphical user interface
Summary(pl.UTF-8):	Graficzny interfejs użytkownika profilera sysprof
Group:		Applications/System
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.44.0
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

%description ui-devel
Header files for sysprof-ui library.

%description ui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki sysprof-ui.

%prep
%setup -q

%build
%meson build \
	%{?with_sysprofd:-Dwith_sysprofd=bundled}

%meson_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install -C build

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
%doc AUTHORS NEWS TODO
%attr(755,root,root) %{_bindir}/sysprof-cli
%if %{with sysprofd}
%dir %{_libexecdir}/sysprof
%attr(755,root,root) %{_libexecdir}/sysprof/sysprofd
%{systemdunitdir}/sysprof2.service
%{_datadir}/dbus-1/system-services/org.gnome.Sysprof2.service
%{_datadir}/dbus-1/system.d/org.gnome.Sysprof2.conf
%{_datadir}/polkit-1/actions/org.gnome.sysprof2.policy
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-2.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsysprof-capture-2.a
%dir %{_includedir}/sysprof-2
%{_includedir}/sysprof-2/sp-kallsyms.h
%{_includedir}/sysprof-2/sp-address.h
%{_includedir}/sysprof-2/sp-clock.h
%{_includedir}/sysprof-2/sp-error.h
%{_includedir}/sysprof-2/sysprof.h
%{_includedir}/sysprof-2/sysprof-capture.h
%{_includedir}/sysprof-2/sysprof-version.h
%dir %{_includedir}/sysprof-2/callgraph
%{_includedir}/sysprof-2/callgraph/sp-callgraph-profile.h
%dir %{_includedir}/sysprof-2/capture
%{_includedir}/sysprof-2/capture/sp-capture-condition.h
%{_includedir}/sysprof-2/capture/sp-capture-cursor.h
%{_includedir}/sysprof-2/capture/sp-capture-reader.h
%{_includedir}/sysprof-2/capture/sp-capture-types.h
%{_includedir}/sysprof-2/capture/sp-capture-writer.h
%dir %{_includedir}/sysprof-2/profiler
%{_includedir}/sysprof-2/profiler/sp-local-profiler.h
%{_includedir}/sysprof-2/profiler/sp-profile.h
%{_includedir}/sysprof-2/profiler/sp-profiler.h
%dir %{_includedir}/sysprof-2/sources
%{_includedir}/sysprof-2/sources/sp-gjs-source.h
%{_includedir}/sysprof-2/sources/sp-hostinfo-source.h
%{_includedir}/sysprof-2/sources/sp-memory-source.h
%{_includedir}/sysprof-2/sources/sp-perf-source.h
%{_includedir}/sysprof-2/sources/sp-proc-source.h
%{_includedir}/sysprof-2/sources/sp-source.h
%dir %{_includedir}/sysprof-2/symbols
%{_includedir}/sysprof-2/symbols/sp-elf-symbol-resolver.h
%{_includedir}/sysprof-2/symbols/sp-jitmap-symbol-resolver.h
%{_includedir}/sysprof-2/symbols/sp-kernel-symbol-resolver.h
%{_includedir}/sysprof-2/symbols/sp-kernel-symbol.h
%{_includedir}/sysprof-2/symbols/sp-symbol-dirs.h
%{_includedir}/sysprof-2/symbols/sp-symbol-resolver.h
%dir %{_includedir}/sysprof-2/util
%{_includedir}/sysprof-2/util/sp-map-lookaside.h
%{_includedir}/sysprof-2/util/sp-model-filter.h
%{_includedir}/sysprof-2/util/sp-process-model-item.h
%{_includedir}/sysprof-2/util/sp-process-model.h
%{_includedir}/sysprof-2/util/sp-selection.h
%{_includedir}/sysprof-2/util/sp-zoom-manager.h
%dir %{_includedir}/sysprof-2/visualizers
%{_includedir}/sysprof-2/visualizers/sp-mark-visualizer-row.h
%{_pkgconfigdir}/sysprof-2.pc
%{_pkgconfigdir}/sysprof-capture-2.pc

%files ui -f %{name}-ui.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sysprof
%{_datadir}/glib-2.0/schemas/org.gnome.sysprof2.gschema.xml
%{_datadir}/mime/packages/sysprof-mime.xml
%{_desktopdir}/org.gnome.Sysprof2.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Sysprof.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Sysprof-symbolic.svg
%{_datadir}/metainfo/org.gnome.Sysprof2.appdata.xml

%files ui-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsysprof-ui-2.so

%files ui-devel
%defattr(644,root,root,755)
%{_includedir}/sysprof-2/sysprof-ui.h
%{_pkgconfigdir}/sysprof-ui-2.pc
%{_includedir}/sysprof-2/callgraph/sp-callgraph-view.h
%dir %{_includedir}/sysprof-2/visualizers
%{_includedir}/sysprof-2/visualizers/sp-cpu-visualizer-row.h
%{_includedir}/sysprof-2/visualizers/sp-line-visualizer-row.h
%{_includedir}/sysprof-2/visualizers/sp-visualizer-row.h
%{_includedir}/sysprof-2/visualizers/sp-visualizer-view.h
%dir %{_includedir}/sysprof-2/widgets
%{_includedir}/sysprof-2/widgets/sp-cell-renderer-percent.h
%{_includedir}/sysprof-2/widgets/sp-empty-state-view.h
%{_includedir}/sysprof-2/widgets/sp-failed-state-view.h
%{_includedir}/sysprof-2/widgets/sp-multi-paned.h
%{_includedir}/sysprof-2/widgets/sp-process-model-row.h
%{_includedir}/sysprof-2/widgets/sp-profiler-menu-button.h
%{_includedir}/sysprof-2/widgets/sp-recording-state-view.h
