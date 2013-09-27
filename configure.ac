#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.68])
AC_INIT([openavb],
        m4_esyscmd([build-aux/git-version-gen .tarball-version]),
        [foo at bar.com])

AC_CONFIG_SRCDIR([daemons])
AC_CONFIG_HEADER([daemons/config.h])
AM_INIT_AUTOMAKE(AC_PACKAGE_NAME, AC_PACKAGE_VERSION)

# Disable static libraries.
AC_DISABLE_STATIC

# Pull AC_COMPILE_IFELSE & co.
AC_USE_SYSTEM_EXTENSIONS

# Checks for programs.
AC_PROG_CXX
AC_PROG_AWK
AC_PROG_CC
AM_PROG_CC_C_O
AM_PROG_LIBTOOL
AC_PROG_INSTALL

# Checks for libraries.
AC_CHECK_LIB([m], [sin])
# FIXME: Replace `main' with a function in `-lpthread':
AC_CHECK_LIB([pthread], [pthread_exit])

PKG_CHECK_MODULES(PCIUTILS, libpci)
AC_SUBST(PCIUTILS_CFLAGS)
AC_SUBST(PCIUTILS_LIBS)

PKG_CHECK_MODULES(ZLIB, zlib)
AC_SUBST(ZLIB_CFLAGS)
AC_SUBST(ZLIB_LIBS)

# Checks for header files.
AC_CHECK_HEADERS([arpa/inet.h fcntl.h inttypes.h netinet/in.h stddef.h stdint.h stdlib.h string.h sys/ioctl.h sys/socket.h sys/time.h syslog.h unistd.h])

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL
AC_C_INLINE
AC_TYPE_INT16_T
AC_TYPE_INT32_T
AC_TYPE_INT64_T
AC_TYPE_INT8_T
AC_TYPE_OFF_T
AC_TYPE_SIZE_T
AC_TYPE_SSIZE_T
AC_TYPE_UINT16_T
AC_TYPE_UINT32_T
AC_TYPE_UINT64_T
AC_TYPE_UINT8_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_MMAP
AC_FUNC_REALLOC
AC_FUNC_STRNLEN
AC_CHECK_FUNCS([ftruncate gettimeofday isascii memset munmap pow select socket strchr strdup strerror strstr strtol])

# Check if any flags need to be passed on to the kernel module build.
AC_ARG_ENABLE(kmod-flags,
              [  --enable-kmod-flags      pass the given flags to the module build process],
	      [IGB_KMOD_BUILD_FLAGS="$enableval"], [])

AC_SUBST(IGB_KMOD_BUILD_FLAGS)


AC_CONFIG_FILES([Makefile
                 kmod/Makefile
                 igb.pc])
AC_OUTPUT
