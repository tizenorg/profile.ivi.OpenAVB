SUBDIRS         = . kmod
lib_LTLIBRARIES =
sbin_PROGRAMS   =
bin_PROGRAMS    =
pkgconfigdir    = ${libdir}/pkgconfig
pkgconfig_DATA  =

INCLUDES        =
EXTRA_DIST      =

#########################
# igb library
lib_LTLIBRARIES += libigb.la

libigb_ladir     = $(includedir)/igb

libigb_la_HEADERS = 			\
		lib/igb/e1000_82575.h   \
		lib/igb/e1000_osdep.h   \
		lib/igb/igb_internal.h  \
		lib/igb/e1000_defines.h \
		lib/igb/e1000_regs.h	\
		lib/igb/e1000_hw.h	\
		lib/igb/igb.h

libigb_la_SOURCES = lib/igb/igb.c

libigb_la_LIBADD  =

pkgconfig_DATA  += igb.pc
EXTRA_DIST      += igb.pc

#########################
# PTP daemon
sbin_PROGRAMS += daemon_cl

daemon_cl_SOURCES = 					\
		daemons/gptp/common/ieee1588port.cpp	\
		daemons/gptp/common/ieee1588clock.cpp	\
		daemons/gptp/common/ptp_message.cpp	\
		daemons/gptp/common/avbts_osnet.cpp	\
		daemons/gptp/linux/src/daemon_cl.cpp

daemon_cl_CXXFLAGS = 					\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		-Idaemons/gptp/common 			\
		-Idaemons/gptp/linux/src

daemon_cl_LDADD = -lpthread -lrt

#########################
# MRP daemon
sbin_PROGRAMS += mrpd

mrpd_SOURCES   =					\
		daemons/common/parse.c			\
		daemons/mrpd/mvrp.c			\
		daemons/mrpd/msrp.c			\
		daemons/mrpd/mmrp.c			\
		daemons/mrpd/mrp.c			\
		daemons/mrpd/mrpd.c

mrpd_CFLAGS =	 					\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		-Idaemons/common

mrpd_LDADD =

#########################
# MRP client
bin_PROGRAMS  += mrpctl

mrpctl_SOURCES = daemons/mrpd/mrpctl.c

mrpctl_CFLAGS =	 					\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		-Idaemons/common

#########################
# mrpq example client
bin_PROGRAMS += mrpq

mrpq_SOURCES = 						\
		examples/mrp_client/mrpq.c		\
		examples/mrp_client/mrpdclient.c

mrpq_CFLAGS  =						\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		-Idaemons/mrpd

#########################
# mrql example client
bin_PROGRAMS += mrpl

mrpl_SOURCES =						\
		examples/mrp_client/mrpq.c		\
		examples/mrp_client/mrpdclient.c

mrpl_CFLAGS  =						\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		-Idaemons/mrpd

#########################
# simple_talker example client
bin_PROGRAMS += simple_talker

simple_talker_SOURCES = 				\
		examples/simple_talker/simple_talker.c

simple_talker_CFLAGS  =					\
		$(AM_CFLAGS)				\
		$(INCLUDES)				\
		$(PCIUTILS_CFLAGS)			\
		$(ZLIB_CFLAGS)				\
		-Ilib/igb				\
		-Idaemons/mrpd

simple_talker_LDADD = 					\
		libigb.la				\
		$(PCIUTILS_LIBS)			\
		$(ZLIB_LIBS)				\
		-lrt -lm -lpthread
