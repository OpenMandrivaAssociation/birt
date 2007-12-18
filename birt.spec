Summary:	BIRT - Batch Image Resizing Thing
Name:		birt
Version:	1.2.1
Release:	%mkrel 2
License:	GPL
Group:		Graphics

Source:		http://acherondevelopment.com/files/birt/%{name}-%{version}.tar.bz2

Url:		http://acherondevelopment.com/project.php?name=birt
BuildRequires:	libqt-devel, ImageMagick

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

perl -p -i -e 's|(INSTALL_PATH\s*=\s*).*?$|$1/usr/share/birt|g' birt.pro
perl -p -i -e 's|(target.extra\s*=\s*cp\s+\$\$TARGET\s+)\$\$INSTALL_PATH/|$1%{buildroot}%{_bindir}|g' birt.pro
qmake
%make

# Generate menu icons in required format
convert birticon.png -resize 32x32 %{name}.png
convert birticon.png -resize 16x16 %{name}_mini.png
convert birticon.png -resize 48x48 %{name}_large.png

%install

rm -rf %buildroot
install -d %{buildroot}%{_bindir}
%makeinstall INSTALL_ROOT=%{buildroot}

# install menu icon
install -d %buildroot%{_datadir}/icons
install -m 644 %{name}.png %buildroot%{_datadir}/icons/
install -d %buildroot%{_datadir}/icons/mini
install -m 644 %{name}_mini.png %buildroot%{_datadir}/icons/mini/%{name}.png
install -d %buildroot%{_datadir}/icons/large
install -m 644 %{name}_large.png %buildroot%{_datadir}/icons/large/%{name}.png

# install menu entry
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=Graphics;Viewer;
Name=BIRT - Batch Image Resizing Thing
Comment=GUI tool for easy resizing series of images
Exec=%{name}
Icon=%{name}
EOF

%post
%update_menus

%postun
%clean_menus

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc README LICENSE
%_bindir/*
%_iconsdir/*.png
%_iconsdir/*/*.png
%{_datadir}/applications/mandriva-%{name}.desktop
%_datadir/%{name}
