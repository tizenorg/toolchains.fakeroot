Name:       fakeroot
Summary:    Gives a fake root environment
Version:    1.12.4
Release:    19
Group:      Development/Tools
License:    GPL+
URL:        http://fakeroot.alioth.debian.org/
Source0:    http://ftp.debian.org/debian/pool/main/f/fakeroot/%{name}-%{version}.tar.gz
Source1001: packaging/fakeroot.manifest 
Requires:   util-linux
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig
BuildRequires:  gcc-c++
BuildRequires:  util-linux-ng
BuildRequires:  sharutils


%description
fakeroot runs a command in an environment wherein it appears to have
root privileges for file manipulation. fakeroot works by replacing the
file manipulation library functions (chmod(2), stat(2) etc.) by ones
that simulate the effect the real library functions would have had,
had the user really been root.




%prep
%setup -q 

%build
cp %{SOURCE1001} .
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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest fakeroot.manifest
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


