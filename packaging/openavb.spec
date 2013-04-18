%{!?_with_debug:%{!?_without_debug:%define _without_debug 0}}

Summary: OpenAVB
Name: openavb
Version: 20130418
Release: 1
License: Other
Group: System Environment/Daemons
URL: https://github.com/intel-ethernet/Open-AVB
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: openavb-kmod-igb

BuildRequires: libstdc++-devel
BuildRequires: kernel-x86-ivi-devel
BuildRequires: pkgconfig(libpci)
BuildRequires: pkgconfig(zlib)

%package kmod-igb
Summary: OpenAVB kernel module for Intel ethernet cards.
Group: System Environment/Kernel

%package libigb
Summary: igb runtime library from the OpenAVB distribution.
Group: System Environment/Libraries

%package examples
Summary: Example clients from the OpenAVB distribution.
Group: Applications/Communications
Requires: openavb-libigb = %{version}

%package devel
Summary: Headers and libraries from the OpenAVB distribution.
Group: Development/Libraries

%package doc
Summary: Documentation from theOpenAVB distribution.
Group: Documentation

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
%if %{?_with_debug:1}%{!?_with_debug:0}
export CFLAGS="-O0 -g3"
export CXXFLAGS="-O0 -g3"
%endif

NUM_CPUS="`cat /proc/cpuinfo | tr -s '\t' ' ' | \
               grep '^processor *:' | wc -l`"
[ -z "$NUM_CPUS" ] && NUM_CPUS=1

BUILD_KERNEL=$(ls /lib/modules/ | grep ..... | head -1)

./bootstrap && \
    %configure $CONFIG_OPTIONS && \
    make clean && \
    make BUILD_KERNEL=$BUILD_KERNEL -j$(($NUM_CPUS + 1))

%install
rm -rf $RPM_BUILD_ROOT

BUILD_KERNEL=$(ls /lib/modules/ | grep ..... | head -1)

make DESTDIR=$RPM_BUILD_ROOT \
    INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
    BUILD_KERNEL=$BUILD_KERNEL install

rm -f $RPM_BUILD_ROOT%{_libdir}/libigb.la

%clean
rm -rf $RPM_BUILD_ROOT

%post libigb
ldconfig

%post kmod-igb
depmod -a

%files
%defattr(-,root,root,-)
%{_sbindir}/daemon_cl
%{_sbindir}/mrpd
%{_bindir}/mrpctl

%files kmod-igb
%defattr(-,root,root,-)
/lib/modules/*/kernel/drivers/net/igb_avb

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
%doc README.rst documents examples

%changelog
* Tue Nov 27 2012 Krisztian Litkey <krisztian.litkey@intel.com> -
- Initial build for 2.0alpha.
