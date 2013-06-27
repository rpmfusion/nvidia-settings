# We use the driver version as a snapshot internal number
# The real version of the package remains 1.0
# This will prevent missunderstanding and versioning changes on the nvidia driver
%global nversion  319.32
%global npriority $(echo %{nversion} | cut -f 1 -d ".")
%global nserie    current

Name:           nvidia-settings
Version:        1.0
Release:        33%{?dist}
Summary:        Configure the NVIDIA graphics driver

Group:          Applications/System
License:        GPLv2+
URL:            ftp://download.nvidia.com/XFree86/nvidia-settings/
Source0:        ftp://download.nvidia.com/XFree86/nvidia-settings/nvidia-settings-%{nversion}.tar.bz2
Patch0:         nvidia-settings-256.35-validate.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora} > 11 || 0%{?rhel} > 5
ExclusiveArch: i686 x86_64
%else 0%{?fedora} == 11
ExclusiveArch: i586 x86_64
%else
ExclusiveArch: i386 x86_64
%endif

BuildRequires:  desktop-file-utils

BuildRequires:  gtk2-devel
#BuildRequires:  libXNVCtrl-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  libvdpau-devel
BuildRequires:  m4
#Needed for FBConfig table - Uneeded if GLX_VERSION_1_3
#BuildRequires: xorg-x11-drv-nvidia-devel
BuildRequires:  mesa-libGL-devel

Requires: nvidia-settings-desktop
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

Provides: nvidia-settings-nversion = %{nversion}
Provides: nvidia-304xx-settings = %{nversion}



%description
The nvidia-settings utility is a tool for configuring the NVIDIA graphics
driver.  It operates by communicating with the NVIDIA X driver, querying
and updating state as appropriate.

This communication is done with the NV-CONTROL X extension.
nvidia-settings is compatible with driver up to %{nversion}.

%package desktop
Summary:         Desktop file for %{name}
Group:           Applications/System

%description desktop
This package provides the desktop file of the %{name} package.


%prep
%setup -q -n nvidia-settings-%{nversion}
%patch0 -p1 -b .validate
rm -rf src/libXNVCtrl/libXNVCtrl.a

sed -i -e 's|/usr/local|%{_prefix}|g' utils.mk
sed -i -e 's|-lXxf86vm|-lXxf86vm -ldl -lm|g' Makefile

%build
# no job control
export CFLAGS="$RPM_OPT_FLAGS"
pushd src/libXNVCtrl
  make
popd
make  \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="$RPM_OPT_FLAGS" || :


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

# Desktop entry for nvidia-settings
desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    doc/nvidia-settings.desktop

#Move the binary elsewhere
mv $RPM_BUILD_ROOT%{_bindir}/nvidia-settings \
    $RPM_BUILD_ROOT%{_bindir}/nvidia-settings-%{nserie}
touch $RPM_BUILD_ROOT%{_bindir}/nvidia-settings
chmod 0755 $RPM_BUILD_ROOT%{_bindir}/nvidia-settings*

#Move the manpage elsewhere
mv $RPM_BUILD_ROOT%{_mandir}/man1/nvidia-settings.1.gz \
    $RPM_BUILD_ROOT%{_mandir}/man1/nvidia-settings-%{nserie}.1.gz
touch $RPM_BUILD_ROOT%{_mandir}/man1/nvidia-settings.1.gz
chmod 0644 $RPM_BUILD_ROOT%{_mandir}/man1/nvidia-settings*


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/alternatives \
  --install %{_bindir}/nvidia-settings nvidia-settings %{_bindir}/nvidia-settings-%{nserie} %{npriority} \
  --slave %{_mandir}/man1/nvidia-settings.1.gz nvidia-settings.1.gz %{_mandir}/man1/nvidia-settings-%{nserie}.1.gz || :

%postun
if [ $1 -eq 0 ]; then
  %{_sbindir}/alternatives --remove nvidia-settings %{_bindir}/%{name}-%{nserie}
fi || :

%files
%defattr(-,root,root,-)
%doc doc/*.txt
%ghost %{_bindir}/nvidia-settings
%{_bindir}/nvidia-settings-%{nserie}
%ghost %{_mandir}/man1/nvidia-settings.1.gz
%{_mandir}/man1/nvidia-settings-%{nserie}.1.gz

%files desktop
%defattr(-,root,root,-)
%{_datadir}/applications/*nvidia-settings.desktop

%changelog
* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0-33
- Update to 319.32

* Fri May 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0-32
- Update to 319.23

* Mon May 13 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0-31
- Update to 319.17
- add build requires m4

* Mon Mar 11 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0-30
- Update to 313.26
- Add Alternatives support
- Drop patch needed for older 173xx/96xx series.
  Thoses will use nvidia-settings-legacy instead
- Build libXNVCtrl with our %%optflags
- Split the desktop file in a sub-package

* Wed Jan 16 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0-29
- Update to 313.18

* Sat Dec 01 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-28
- Update to 310.19

* Tue Oct 16 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-27
- Update to 310.14

* Mon Sep 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-26
- Update to 304.51

* Sat Sep 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-25
- Update to 304.48

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-24
- Update to 304.43
- Add BR libXrandr-devel
- Add missing files

* Tue Aug 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-23
- Update to 304.37

* Tue Jul 31 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-22
- Update to 304.30

* Sat Jul 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0-21
- Update to 304.22

* Sun Jun 17 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-20
- Update to 302.17

* Tue May 22 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-19
- Update to 302.11

* Tue May 22 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-18
- Update to 295.53

* Thu May 03 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-17
- Update to 295.49

* Wed Apr 11 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-16
- Update to 295.40
- Fix source url

* Thu Mar 22 2012 leigh scott <leigh123linux@googlemail.com> - 1.0-15
- Update internal 295.33

* Mon Feb 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-14
- Update internal 295.20

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-13
- Update internal 290.10

* Thu Oct 13 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-12
- Update internal 285.05.09

* Sun Jul 31 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-11
- Update internal to 280.11

* Sun May 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-10
- Update internal to 270.41.06

* Thu Dec 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-9
- Update internal to 260.19.29

* Thu Oct 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-8
- Update internal to 260.19.12

* Sun Oct 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-7
- Update internal to 260.19.06
- Restore noscanout patch

* Mon Sep 06 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-6
- Update internal to 256.53

* Sat Jul 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0-5
- Update internal to 256.35
- Use upstream desktop file (completed)
- Provides %%{name}-nversion internal

* Wed Apr 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-4
- Update internal to 195.36.24
- Avoid failure on NV_CTRL_NO_SCANOUT when not supported in legacy drivers. 

* Sun Feb 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-3.4
- Update internal version to 195.36.08
- Add patch for -lm

* Wed Oct 21 2009 kwizart < kwizart at gmail.com > - 1.0-3.1
- Update internal to 190.42

* Wed Jul 15 2009 kwizart < kwizart at gmail.com > - 1.0-3
- Update internal to 185.18.14

* Tue Mar  3 2009 kwizart < kwizart at gmail.com > - 1.0-2.1
- Update internal to 180.35

* Tue Jun 17 2008 kwizart < kwizart at gmail.com > - 1.0-2
- Update to 173.14.09
- Remove the locale patch

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.0-1
- First Package for Fedora.

