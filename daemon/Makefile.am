INCLUDES = -I$(srcdir)/../services
# KDE_CXXFLAGS = $(USE_EXCEPTIONS)

sbin_PROGRAMS = iceccd
iceccd_SOURCES = ncpus.c main.cpp serve.cpp workit.cpp environment.cpp load.cpp
iceccd_LDADD = ../services/libicecc.la $(LIB_KINFO)
noinst_HEADERS = environment.h load.h ncpus.h serve.h workit.h

