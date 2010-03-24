Summary:	BIRT - Batch Image Resizing Thing
Name:		birt
Version:	1.2.2
Release:	%mkrel 3
License:	GPLv2+
Group:		Graphics
Source:		http://vrai.net/files/software_projects/birt/%name-%{version}.tar.bz2
URL:		http://vrai.net/project.php?project=birt
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	qt3-devel
BuildRequires:	imagemagick

%description
BIRT, the Batch Image Resizing Thing, is a simple application that
allows a large number of images to be resized in one go. Obviously
this is possible by scripting ImageMagick but it's usually somewhat
easier with a GUI. It was created in order to learn how to develop
using the Qt library, and to facilitate the maintenance of an online
photo album where each hi-res photo needs a low-res copy and a
thumbnail.

%prep
%setup -q

%build
sed -i -e 's,/usr/local/birt,/usr/share/birt,g' birt.pro
sed -i -e 's,$$INSTALL_PATH/,%{buildroot}%{_bindir},g' birt.pro
%{qt3bin}/qmake QMAKE_CXXFLAGS="%{optflags}"
make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
%makeinstall INSTALL_ROOT=%{buildroot}

# install menu icon
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -scale 16x16 birticon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32x32 birticon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 48x48 birticon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# install menu entry
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=Qt;Graphics;2DGraphics;Viewer;
Name=BIRT - Batch Image Resizing Thing
Comment=GUI tool for easy resizing series of images
Exec=%{_bindir}/%{name}
Icon=%{name}
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
