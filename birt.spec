Summary:	- Batch Image Resizing Thing
Name:		birt
Version:	1.2.2
Release:	%mkrel 4
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


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-4mdv2011.0
+ Revision: 610072
- rebuild

* Wed Mar 24 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.2.2-3mdv2010.1
+ Revision: 527252
- New url, source
- fix license

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 1.2.2-2mdv2010.0
+ Revision: 424625
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Thu Jul 31 2008 Adam Williamson <awilliamson@mandriva.org> 1.2.2-1mdv2009.0
+ Revision: 258483
- br qt3-devel, not libqt3-devel (for x86-64)
- don't package LICENSE
- simplify the sed commands (and make them work)
- specifically buildrequre libqt3-devel and call qt3's qmake
- new release 1.2.2 (fixes build)
- rebuild for new era
- fd.o icons
- new license policy
- spec clean

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix extra spacing at top of description
    - auto-convert XDG menu entry
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - Import birt



* Wed Dec  7 2005 Till Kamppeter <till@mandriva.com> 1.2.1-1mdk
- initial release.
