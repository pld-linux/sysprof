# Conditional build:
%bcond_without  dist_kernel     # without distribution kernel
%bcond_without  kernel          # don't build kernel modules
%bcond_without  userspace       # don't build userspace tools
#
%define	rel	1
Summary:	Sampling CPU profiler for Linux
Name:		sysprof
Version:	1.0.12
Release:	%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://www.daimi.au.dk/~sandmann/sysprof/%{name}-%{version}.tar.gz
# Source0-md5:	9566040f3175678e75133b1c52a473f8
URL:		http://www.daimi.au.dk/~sandmann/sysprof/
BuildRequires:	binutils-devel
BuildRequires:	gtk+2-devel
BuildRequires:	rpmbuild(macros) >= 1.217
Requires:	uname(release) >= 2.6
Conflicts:	kernel < 2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sysprof is a sampling CPU profiler for Linux that uses a kernel module
to profile the entire system, not just a single application. Sysprof
handles shared libraries and applications do not need to be
recompiled. In fact they don't even have to be restarted.

Just insert the kernel module and start sysprof.

%package -n kernel%{_alt_kernel}-sysprof
Summary:	sysprof kernel driver
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-sysprof
sysprof Linux kernel driver.

%prep
%setup -q

%build
%configure \
	--disable-kernel-module
%if %{with userspace}
%{__make}
%endif

%if %{with kernel}
cd module
%build_kernel_modules SUBDIRS=$PWD -m sysprof-module
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with kernel}
cd module
%install_kernel_modules -m sysprof-module -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-sysprof
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-sysprof
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_bindir}/*
%{_pixmapsdir}/*.png
%{_datadir}/%{name}
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-sysprof
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif
