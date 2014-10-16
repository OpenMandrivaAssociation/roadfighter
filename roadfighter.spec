Name:		roadfighter
Version:	1.0.1269
Release:	2
Summary:	Konami's Road Fighter remake
Group:		Games/Arcade
# http://www.braingames.getput.com/forum/forum_posts.asp?TID=678&PN=1
License:	Distributable
URL:		http://roadfighter.jorito.net/
Source0:	http://braingames.jorito.net/roadfighter/downloads/%{name}.src_%{version}.tgz
Patch0:		roadfighter-1.0.1269-Makefile.patch
Patch1:		roadfighter-1.0.1269-sformat.patch
Patch2:		roadfighter-1.0.1269-datapath.patch
Patch3:		roadfighter-1.0.1269-desktop.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_sound-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils

%description
This is a remake of a car-based arcade game developed by Konami and released
in 1984. The goal is to reach the finish line within the stages without
running out of time, hitting other cars or running out of fuel.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Fix char encondig
iconv --from=ISO-8859-1 --to=UTF-8 readme.txt > readme.txt.utf8
touch -r readme.txt readme.txt.utf8
mv readme.txt.utf8 readme.txt

%build
export CFLAGS="%{optflags}"
%make

%install
rm -rf %{buildroot}

# Install game and data
install -d %{buildroot}%{_gamesbindir}
install -m 755 -p %{name} %{buildroot}%{_gamesbindir}/
install -d %{buildroot}%{_gamesdatadir}/%{name}
cp -pr fonts graphics maps sound %{buildroot}%{_gamesdatadir}/%{name}/

# Install icon
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
convert -resize 32x32 \
  -frame 0x3 \
  -mattecolor '#dfdfdf' \
  -transparent '#dfdfdf' \
  build/linux/roadfighter.png \
  %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  build/linux/%{name}.desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc readme.txt
%{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

