Summary:	Sampling CPU profiler for Linux
Name:		sysprof
Version:	1.2.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://sysprof.com/%{name}-%{version}.tar.gz
# Source0-md5:	a81808d847732f8dafb59d26ec2eebbf
URL:		http://sysprof.com/
BuildRequires:	binutils-devel
BuildRequires:	gtk+2-devel
BuildRequires:	rpmbuild(macros) >= 1.217
Requires:	uname(release) >= 2.6.31
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sysprof is a sampling CPU profiler for Linux that uses a kernel module
to profile the entire system, not just a single application. Sysprof
handles shared libraries and applications do not need to be
recompiled. In fact they don't even have to be restarted.

Just insert the kernel module and start sysprof.

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
%{_pixmapsdir}/*.png
%{_datadir}/%{name}
/lib/udev/rules.d/60-sysprof.rules
