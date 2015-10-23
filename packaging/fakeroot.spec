
Name:       fakeroot
Summary:    Gives a fake root environment
Version:    1.12.4
Release:    %{?release_prefix:%{release_prefix}.}19.37.%{?dist}%{!?dist:tizen}
VCS:        external/fakeroot#submit/trunk/20121019.092126-0-gc39aff3bda075955b1237bd4af825445db57659d
Group:      Development/Tools
License:    GPL+
URL:        http://fakeroot.alioth.debian.org/
Source0:    http://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}_%{version}.tar.gz
Requires:   util-linux
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires:  gcc-c++
BuildRequires:  util-linux
BuildRequires:  sharutils

BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.




%prep
%setup -q -n %{name}-%{version}

%build
for file in ./doc/*/*.1; do
  iconv -f latin1 -t utf8 < $file > $file.new
  mv -f $file.new $file
done





# all build scripts in origin specfile as the following:
for type in sysv tcp; do
mkdir obj-$type
cd obj-$type
cat >> configure << 'EOF'
#! /bin/sh
exec ../configure "$@"
EOF
chmod +x configure
%configure \
  --disable-dependency-tracking \
  --disable-static \
  --libdir=%{_libdir}/libfakeroot \
  --with-ipc=$type \
  --program-suffix=-$type
make %{?jobs:-j%jobs}
cd ..
done

%install
rm -rf %{buildroot}
# Please write install script under ">> install post"

# all install scripts in origin specfile as the following:
rm -rf %{buildroot}
for type in sysv tcp; do
  make -C obj-$type install libdir=%{_libdir}/libfakeroot DESTDIR=%{buildroot}
  chmod 644 %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so 
  mv %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so \
     %{buildroot}%{_libdir}/libfakeroot/libfakeroot-$type.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.so
  rm -f %{buildroot}%{_libdir}/libfakeroot/libfakeroot.*a*
done

ln -s faked-tcp %{buildroot}%{_bindir}/faked
ln -s fakeroot-tcp %{buildroot}%{_bindir}/fakeroot
ln -s libfakeroot-tcp.so %{buildroot}%{_libdir}/libfakeroot/libfakeroot-0.so

%check
for type in sysv tcp; do
  echo 'Bypassing check '$type
#  make -C obj-$type check
done



%clean
rm -rf %{buildroot}



%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING DEBUG debian/changelog doc/README.saving
%{_bindir}/faked-*
%{_bindir}/faked
%{_bindir}/fakeroot-*
%{_bindir}/fakeroot
%{_mandir}/man1/faked-*.1*
%{_mandir}/man1/fakeroot-*.1*
%lang(es) %{_mandir}/es/man1/faked-*.1*
%lang(es) %{_mandir}/es/man1/fakeroot-*.1*
%lang(fr) %{_mandir}/fr/man1/faked-*.1*
%lang(fr) %{_mandir}/fr/man1/fakeroot-*.1*
%lang(sv) %{_mandir}/sv/man1/faked-*.1*
%lang(sv) %{_mandir}/sv/man1/fakeroot-*.1*
%lang(nl) %{_mandir}/nl/man1/faked-*.1*
%lang(nl) %{_mandir}/nl/man1/fakeroot-*.1*
%dir %{_libdir}/libfakeroot
%{_libdir}/libfakeroot/libfakeroot-*.so
%{_libdir}/libfakeroot/libfakeroot-0.so


%changelog
* Mon Sep 16 2013 UkJung Kim <ujkim@samsung.com> - submit/trunk/20121019.092126 
- PROJECT: external/fakeroot
- COMMIT_ID: c39aff3bda075955b1237bd4af825445db57659d
- PATCHSET_REVISION: c39aff3bda075955b1237bd4af825445db57659d
- CHANGE_OWNER: \"UkJung Kim\" <ujkim@samsung.com>
- PATCHSET_UPLOADER: \"UkJung Kim\" <ujkim@samsung.com>
- CHANGE_URL: http://slp-info.sec.samsung.net/gerrit/103390
- PATCHSET_REVISION: c39aff3bda075955b1237bd4af825445db57659d
- TAGGER: UkJung Kim <ujkim@samsung.com>
- Gerrit patchset approval info:
- UkJung Kim <ujkim@samsung.com> Verified : 1
- Newton Lee <newton.lee@samsung.com> Code Review : 2
- CHANGE_SUBJECT: Initial commit
- [Version] 1.12.4
- [Project] GT-I8800
- [Title] Initial commit
- [BinType] PDA
- [Customer] Open
- [Issue#] N/A
- [Problem] N/A
- [Cause] N/A
- [Solution]
- [Team] SCM
- [Developer] UkJung Kim <ujkim@samsung.com>
- [Request] N/A
- [Horizontal expansion] N/A
- [SCMRequest] N/A
* Wed Jun 22 2011 Chris Ferron <chris.e.ferron@linux.intel.com> - 1.12.4
- removed util-linux-ng as it has been replaced by util-linux.
* Sat Jan 30 2010 Zhang, Qiang Z<qiang.z.zhang@intel.com> 1.12.4
- Update to 1.12.4
* Thu Feb 19 2009 Zhang, Qiang Z<qiang.z.zhang@intel.com> 1.12.1
- Update to 1.12.1
* Tue Jan  6 2009 Anas Nashif <anas.nashif@intel.com> 1.11
- Initial import into Moblin
