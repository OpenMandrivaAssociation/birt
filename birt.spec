Summary:	BIRT - Batch Image Resizing Thing
Name:		birt
Version:	1.2.1
Release:	%mkrel 3
License:	GPL+
Group:		Graphics
Source:		http://acherondevelopment.com/files/birt/%{name}-%{version}.tar.bz2
URL:		http://acherondevelopment.com/project.php?name=birt
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	libqt-devel
BuildRequires:	ImageMagick

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
sed -i -e 's|(INSTALL_PATH\s*=\s*).*?$|$1/usr/share/birt|g' birt.pro
sed -i -e 's|(target.extra\s*=\s*cp\s+\$\$TARGET\s+)\$\$INSTALL_PATH/|$1%{buildroot}%{_bindir}|g' birt.pro
qmake
%make

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
Categories=QT;Graphics;Viewer;
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
%doc README LICENSE
%{_bindir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
