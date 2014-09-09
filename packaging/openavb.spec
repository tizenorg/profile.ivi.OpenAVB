%{!?_with_debug:%{!?_without_debug:%define _without_debug 0}}

%define kernel kernel-x86-ivi
%define kernel_relstr "%(/bin/rpm -q --queryformat '%{VERSION}-%{RELEASE}' %{kernel})"
%define kernel_release %(echo %{kernel_relstr})
%define kernel_modstr "%(/bin/rpm -ql %{kernel} | sort | grep /lib/modules/%{kernel_release} | head -1 | sed 's#/*$##g')"
%define kernel_modpath %(echo %{kernel_modstr})
%define kernel_moddir  %(echo %{kernel_modstr} | sed 's#.*/##g')

Summary: OpenAVB
Name: openavb
Version: 20140731
Release: 1
License: Intel and GPL-2.0
Group: Automotive/Ethernet AVB
URL: https://github.com/intel-ethernet/Open-AVB
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: openavb-kmod-igb
ExclusiveArch:  %ix86

BuildRequires: libstdc++-devel
BuildRequires: kernel-x86-ivi-devel
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(zlib)

%package kmod-igb
Summary: kernel module for Intel ethernet cards
Group: System/Kernel
Requires: %{kernel} = %{kernel_release}

%package libigb
Summary: IGB runtime library
Group: System/Libraries

%package examples
Summary: Example clients
Group: Applications/System
Requires: openavb-libigb = %{version}

%package devel
Summary: Headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}

%package doc
Summary: Documentation
Group: Development/Tools

%description
This package contains the basic OpenAVB userspace daemons.

%description kmod-igb
This package contains the kernel module required by OpenAVB for Intel
ethernet cards.

%description libigb
This package contains the libigb runtime library from the OpenAVB
distribution.

%description examples
This package contains various test and example utilities for OpenAVB.

%description devel
This package contains header files and libraries for OpenAVB.

%description doc
This package contains some documentation from the OpenAVB distribution.

%prep
%setup -q

%build
# For now, always compile for debugging...
#%if %{?_with_debug:1}%{!?_with_debug:0}
export CFLAGS="-O0 -g3"
export CXXFLAGS="-O0 -g3"
#%endif

NUM_CPUS="`cat /proc/cpuinfo | tr -s '\t' ' ' | \
               grep '^processor *:' | wc -l`"
[ -z "$NUM_CPUS" ] && NUM_CPUS=1

CONFIG_OPTIONS="--enable-kmod-flags=EXTRA_CFLAGS=-DIGB_PTP"

./bootstrap && \
    %configure $CONFIG_OPTIONS  && \
    make BUILD_KERNEL=%{kernel_moddir} clean && \
    make BUILD_KERNEL=%{kernel_moddir} -j$(($NUM_CPUS + 1))

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT \
    INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
    BUILD_KERNEL=%{kernel_moddir} install

rm -f $RPM_BUILD_ROOT%{_libdir}/libigb.la

# Install systemd and sample 'configuration' files.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig \
    $RPM_BUILD_ROOT/lib/systemd/system \
    %{buildroot}/%{_sysconfdir}/modprobe.d
/usr/bin/install -m 644 packaging/openavb.env \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/openavb
/usr/bin/install -m 644 -t $RPM_BUILD_ROOT/lib/systemd/system \
    packaging/mrpd.service packaging/gptp.service
/usr/bin/install -m 644 packaging/igb_avb.conf \
    %{buildroot}/%{_sysconfdir}/modprobe.d

%clean
rm -rf $RPM_BUILD_ROOT

%post libigb
ldconfig

%postun libigb
ldconfig

%post kmod-igb
depmod -a %{kernel_moddir}

%files
%defattr(-,root,root,-)
%{_sbindir}/daemon_cl
%{_sbindir}/mrpd
%{_bindir}/mrpctl
%{_sysconfdir}/sysconfig/openavb
/lib/systemd/system/mrpd.service
/lib/systemd/system/gptp.service

%files kmod-igb
%defattr(-,root,root,-)
%{kernel_modpath}/kernel/drivers/net/igb_avb
%config(noreplace)%{_sysconfdir}/modprobe.d/igb_avb.conf

%files libigb
%defattr(-,root,root,-)
%{_libdir}/libigb.so.*

%files examples
%defattr(-,root,root,-)
%{_bindir}/mrpl
%{_bindir}/mrpq
%{_bindir}/simple_talker

%files devel
%defattr(-,root,root,-)
%{_includedir}/igb
%{_libdir}/libigb.so
%{_libdir}/pkgconfig/igb.pc

%files doc
%defattr(-,root,root,-)
%doc README.rst documents
%license examples/LICENSE
%doc examples/mrp_client examples/simple_listener examples/simple_talker
