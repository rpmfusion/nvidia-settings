Name:           nvidia-settings
Epoch:          3
Version:        418.43
Release:        1%{?dist}
Summary:        Configure the NVIDIA graphics driver

License:        GPLv2+
URL:            https://download.nvidia.com/XFree86/nvidia-settings/
Source0:        %{url}/nvidia-settings-%{version}.tar.bz2
Source1:        %{name}-user.desktop
Source2:        %{name}.appdata.xml

ExclusiveArch:  x86_64

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  hostname

BuildRequires:  gtk2-devel
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires:  gtk3-devel
BuildRequires:  libappstream-glib
%endif
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  libvdpau-devel
BuildRequires:  m4
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(dbus-1)


%description
The nvidia-settings utility is a tool for configuring the NVIDIA graphics
driver.  It operates by communicating with the NVIDIA X driver, querying
and updating state as appropriate.

This communication is done with the NV-CONTROL X extension.
nvidia-settings is compatible with driver %{version}.


%prep
%setup -q
# We are building from source
rm -rf src/libXNVCtrl/libXNVCtrl.a

sed -i -e 's|/usr/local|%{_prefix}|g' utils.mk
sed -i -e 's|/lib$|/%{_lib}|g' utils.mk
sed -i -e 's|-lXxf86vm|-lXxf86vm -ldl -lm|g' Makefile

%build
# no job control
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
pushd src/libXNVCtrl
  make \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  X_CFLAGS="${CFLAGS}"

popd
make  \
  NVDEBUG=1 \
  NV_VERBOSE=1 \
  STRIP_CMD=true NV_KEEP_UNSTRIPPED_BINARIES=1 \
  X_LDFLAGS="-L%{_libdir}" \
  CC_ONLY_CFLAGS="%{optflags}"
(cd src/_out/Linux_*/ ; for i in %{name} libnvidia-gtk{2,3}.so ; do cp $i.unstripped $i; done ; cd -)


%install
%make_install

# Desktop entry for nvidia-settings
mkdir -p %{buildroot}%{_datadir}/applications
install -m 0644 doc/nvidia-settings.desktop \
  %{buildroot}%{_datadir}/applications

sed -i -e 's|__UTILS_PATH__/||' -e 's|__PIXMAP_PATH__/||' \
  -e 's|nvidia-settings.png|nvidia-settings|' \
  -e 's|__NVIDIA_SETTINGS_DESKTOP_CATEGORIES__|System;Settings;|' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-validate \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Pixmap installation
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -pm 0644 doc/nvidia-settings.png \
  %{buildroot}%{_datadir}/pixmaps

# User settings installation
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
install -pm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-user.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-user.desktop

%if 0%{?fedora}
# AppData installation
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/appdata/
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
%endif

%ldconfig_scriptlets

%files
%doc doc/*.txt
%config %{_sysconfdir}/xdg/autostart/%{name}-user.desktop
%{_bindir}/nvidia-settings
%{_libdir}/libnvidia-gtk?.so.*
%if 0%{?fedora} || 0%{?rhel} > 6
%exclude %{_libdir}/libnvidia-gtk2.so.*
%endif
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%if 0%{?fedora}
%{_datadir}/appdata/%{name}.appdata.xml
%endif
%{_mandir}/man1/nvidia-settings.1.*


%changelog
* Fri Feb 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:418.43-1
- Update to 418.43 release

* Fri Feb 08 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:418.30-1
- Update to 418.30 beta

* Wed Jan 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 3:415.27-1
- Update to 415.27 release

* Wed Dec 26 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.25-1
- Update to 415.25 release

* Fri Dec 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.23-1
- Update to 415.23 release

* Fri Dec 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.22-1
- Update to 415.22 release

* Wed Nov 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:415.18-1
- Update to 415.18 release

* Fri Nov 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.78-1
- Update to 410.78 release

* Thu Oct 25 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.73-1
- Update to 410.73 release

* Tue Oct 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.66-1
- Update to 410.66 release

* Fri Sep 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 3:410.57-2
- Match the cuda repo epoch

* Thu Sep 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 410.57-1
- Update to 410.57 beta

* Wed Aug 22 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.54-1
- Update to 396.54

* Sat Aug 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.51-1
- Update to 396.51

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 396.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.45-1
- Update to 396.45

* Tue Jul 10 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.24-2
- Add build requires mesa-libEGL-devel

* Fri May 04 2018 Leigh Scott <leigh123linux@googlemail.com> - 396.24-1
- Update to 396.24

* Tue Apr 10 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.48-3
- Validate appdata file

* Mon Apr 09 2018 Nicolas Chauvet <kwizart@gmail.com> - 390.48-2
- Fix typo on icon directory
- Add appdata file
- Bundle user desktop settings here.

* Thu Mar 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.48-1
- Update to 390.48

* Tue Mar 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.42-1
- Update to 390.42

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 390.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.25-1
- Update to 390.25

* Thu Jan 11 2018 Leigh Scott <leigh123linux@googlemail.com> - 390.12-1
- Update to 390.12

* Sat Dec 02 2017 Leigh Scott <leigh123linux@googlemail.com> - 387.34-1
- Update to 387.34

* Mon Oct 30 2017 Leigh Scott <leigh123linux@googlemail.com> - 387.22-1
- Update to 387.22

* Fri Sep 22 2017 Leigh Scott <leigh123linux@googlemail.com> - 384.90-1
- Update to 384.90

* Thu Aug 03 2017 Nicolas Chauvet <kwizart@gmail.com> - 384.59-1
- Update to 384.59

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 319.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jul 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 319.32-1
- Build an empty package to workaround yum issue with obsoletes
  using nvidia-settings-current build from sources binary

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

