# We use the driver version as a snapshot internal number
# The real version of the package remains 1.0
# This will prevent missunderstanding and versioning changes on the nvidia driver
%global nversion 195.36.08
#Possible replacement/complement:
#http://willem.engen.nl/projects/disper/

Name:           nvidia-settings
Version:        1.0
Release:        3.4%{?dist}
Summary:        Configure the NVIDIA graphics driver

Group:          Applications/System
License:        MIT
URL:            ftp://download.nvidia.com/XFree86/nvidia-settings/
Source0:        ftp://download.nvidia.com/XFree86/nvidia-settings/nvidia-settings-%{nversion}.tar.gz
Source1:        nvidia-settings.desktop
Patch0:         nvidia-settings-1.0-default.patch
Patch1:         nvidia-settings-1.0-lm.patch
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
BuildRequires:  libXv-devel
#Needed for FBConfig table
BuildRequires:  xorg-x11-drv-nvidia-devel
#BuildRequires:   mesa-libGL-devel



%description
The nvidia-settings utility is a tool for configuring the NVIDIA graphics
driver.  It operates by communicating with the NVIDIA X driver, querying
and updating state as appropriate.

This communication is done with the NV-CONTROL X extension.
nvidia-settings is compatible with driver up to %{nversion}.

%prep
%setup -q
%patch0 -p1 -b .default
%patch1 -p1 -b .lm
rm -rf src/libXNVCtrl/libXNVCtrl.a

sed -i -e 's|# CFLAGS = -Wall|CFLAGS = $(INIT_CFLAGS)|' Makefile
sed -i -e 's|# X11R6_DIR = /usr/X11R6|X11R6_DIR = %{_prefix}|' Makefile
sed -i -e 's|CFLAGS = -Wall -g|CFLAGS = $(RPM_OPT_FLAGS)|' src/XF86Config-parser/Makefile

%build
# no job control
make NVDEBUG=1 INIT_CFLAGS="$RPM_OPT_FLAGS -I/usr/include/nvidia -DX_XF86VidModeGetGammaRampSize"


%install
rm -rf $RPM_BUILD_ROOT
make install ROOT=$RPM_BUILD_ROOT INSTALL="install -p"

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
# Desktop entry for nvidia-settings
desktop-file-install --vendor "" \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
    %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*.txt
%{_bindir}/nvidia-settings
%{_datadir}/applications/*nvidia-settings.desktop
%{_mandir}/man1/nvidia-settings.1.gz


%changelog
* Sun Feb 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-3.4
- Update internal version to 195.36.08
- Built using xorg-x11-drv-nvidia-devel

* Wed Oct 21 2009 kwizart < kwizart at gmail.com > - 1.0-3.1
- Update internal to 190.42

* Thu Jul 15 2009 kwizart < kwizart at gmail.com > - 1.0-3
- Update internal to 185.18.14

* Tue Mar  3 2009 kwizart < kwizart at gmail.com > - 1.0-2.1
- Update internal to 180.35

* Tue Jun 17 2008 kwizart < kwizart at gmail.com > - 1.0-2
- Update to 173.14.09
- Remove the locale patch

* Wed May 28 2008 kwizart < kwizart at gmail.com > - 1.0-1
- First Package for Fedora.

