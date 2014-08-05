#
# spec file for package icecream
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild
# icecream 0


Name:           icecream
BuildRequires:  gcc-c++
License:        GPLv2+ ; LGPLv2.1+
Group:          Development/Tools/Building
Summary:        For Distributed Compile in the Network
Requires:       /bin/tar /usr/bin/bzip2
PreReq:         /usr/sbin/useradd /usr/sbin/groupadd
Requires:       gcc-c++
Version:        0.9.7
Release:        1
Source:        ftp://ftp.suse.com/pub/projects/icecream/icecc-%{version}.tar.bz2

%description
icecream is the next generation distcc.

%package -n libicecream-devel
License:        GPLv2+ ; LGPLv2.1+
Summary:        For Distributed Compile in the Network
Group:          Development/Tools/Building
Summary:        For Distributed Compile in the Network
Requires:       libstdc++-devel

%description -n libicecream-devel
icecream is the next generation distcc.

%prep
%setup -q -n icecc-%{version}

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%configure
make %{?jobs:-j %jobs}

%install
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/opt/icecream/bin
for i in g++ gcc cc c++; do 
  ln -s /usr/bin/icecc $RPM_BUILD_ROOT/opt/icecream/bin/$i
  rm -f $RPM_BUILD_ROOT/usr/bin/$i
done
#
# Install icecream init script
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
install -m 755 suse/init.icecream $RPM_BUILD_ROOT/etc/init.d/icecream
ln -sf /etc/init.d/icecream $RPM_BUILD_ROOT%{_sbindir}/rcicecream
mkdir -p $RPM_BUILD_ROOT/var/adm/fillup-templates
install -m 644 suse/sysconfig.icecream $RPM_BUILD_ROOT/var/adm/fillup-templates/sysconfig.icecream
mkdir -p $RPM_BUILD_ROOT/var/cache/icecream
mkdir -p $RPM_BUILD_ROOT%_mandir/man{1,7}
for i in mans/*.1 mans/*.7; do
	install -m 644 $i $RPM_BUILD_ROOT%_mandir/man`echo $i | sed -e 's,.*\(.\)$,\1,'`/`basename $i`
done
install -m 644 -D suse/logrotate $RPM_BUILD_ROOT/etc/logrotate.d/icecream

%preun
%stop_on_removal icecream

%pre
/usr/sbin/groupadd -r icecream 2> /dev/null || :
/usr/sbin/useradd -r -g icecream -s /bin/false -c "Icecream Daemon" -d /var/cache/icecream icecream 2> /dev/null || :

%postun
%restart_on_update icecream
%{insserv_cleanup}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%config /etc/logrotate.d/icecream
%config /etc/init.d/icecream
%_bindir/icecc
%_bindir/icerun
%_sbindir/scheduler
%_libdir/icecc
%_sbindir/iceccd
%_sbindir/rcicecream
%_mandir/man*/*
/opt/icecream
/var/adm/fillup-templates/sysconfig.icecream
%attr(-,icecream,icecream) /var/cache/icecream

%files -n libicecream-devel
%defattr(-,root,root)
%_includedir/icecc
%_libdir/libicecc.*
%_libdir/pkgconfig/icecc.pc

%changelog
