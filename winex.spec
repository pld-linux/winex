Summary:	Program that lets you launch Win applications
Summary(es):	Ejecuta programas Windows en Linux
Summary(pl):	Program pozwalaj�cy uruchamia� aplikacje Windows
Summary(pt_BR):	Executa programas Windows no Linux
Name:		winex
Version:	20020718
Release:	1
License:	GPL
Group:		Applications/Emulators
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.init
Source2:	%{name}.reg
Source3:	%{name}.systemreg
Source4:	%{name}.userreg
Patch0:		%{name}-fontcache.patch
#Patch1:		%{name}-rc_fix.patch
URL:		http://www.winehq.com/
ExclusiveArch:	%{ix86}
BuildRequires:	arts-devel
BuildRequires:	bison
BuildRequires:	chpax
BuildRequires:	cups-devel
BuildRequires:	docbook-dtd31-sgml
BuildRequires:	docbook-utils
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.5
BuildRequires:	libjpeg-devel
BuildRequires:	ncurses-devel
#BuildRequires:	OpenGL-devel
BuildRequires:	openjade
BuildRequires:	XFree86-devel
Requires:	OpenGL
Requires(post): ldconfig
Requires(post,preun): chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep		libGL.so.1 libGLU.so.1
%define		no_install_post_strip	1

%define		_prefix			/usr/X11R6
%define		_mandir			%{_prefix}/man
%define		_winexdir		%{_datadir}/%{name}

%description
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix. It
consists of a program loader which loads and executes a Microsoft
Windows binary, and a library that implements Windows API calls using
their Unix or X11 equivalents. The library may also be used for
porting Win32 code into native Unix executables.

%description -l es
Ejecuta programas Windows en Linux.

%description -l pl
Wine jest programem dzi�ki kt�remu mo�na uruchamia� programy napisane
dla Microsoft Windows pod systemami unixowymi. Sk�ada si� on z
loadera, kt�ry pozwala wczytywa� i uruchamia� programy w formacie
Microsoft Windows oraz z biblioteki, kt�ra implementuje API Windows
przy u�yciu odpowiednik�w Unixowych oraz z X11. Biblioteka mo�e by�
tak�e wykorzystana do przenoszenia aplikacji Win32 do Unixa.

%description -l pt_BR
O Wine � um programa que permite rodar programas MS-Windows no X11.
Ele consiste de um carregador de programa, que carrega e executa um
bin�rio MS-Windows, e de uma biblioteca de emula��o que traduz as
chamadas da API para as equivalentes Unix/X11.

%package devel
Summary:	Wine - header files
Summary(es):	Biblioteca de desarrollo de wine
Summary(pl):	Wine - pliki nag�owkowe
Summary(pt_BR):	Biblioteca de desenvolvimento do wine
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Wine - header files.

%description devel -l es
Biblioteca de desarrollo de wine.

%description devel -l pl
Wine - pliki nag��wkowe.

%description devel -l pt_BR
Arquivos de inclus�o e bibliotecas para desenvolver aplica��es com o
WINE.

%prep
%setup -q -n wine
%patch0 -p1
#%patch1

# turn off compilation of some tools
#sed -e "s|winetest \\\|\\\|;s|avitools||;" \
#	programs/Makefile.in > .tmp
#mv -f .tmp programs/Makefile.in

%build
#aclocal
#autoconf
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
CFLAGS="%{rpmcflags} $CPPFLAGS"
%configure \
%{!?debug:	--disable-debug} \
%{!?debug:	--disable-trace} \
	--enable-curses \
	--disable-opengl \
	--with-x

%{__make} depend
%{__make}

#(cd documentation
#./db2html-winehq wine-user.sgml
#./db2html-winehq wine-devel.sgml
#./db2html-winehq winelib-user.sgml)

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec-prefix=$RPM_BUILD_ROOT%{_exec_prefix} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	datadir=$RPM_BUILD_ROOT%{_datadir} \
	includedir=$RPM_BUILD_ROOT%{_includedir}/winex \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
	localstatedir=$RPM_BUILD_ROOT%{_localstatedir} \
	sharedstatedir=$RPM_BUILD_ROOT%{_sharedstatedir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
#	dlldir=$RPM_BUILD_ROOT%{_libdir}/winex


(cd $RPM_BUILD_ROOT%{_bindir}
find -name '*.so' | sed 's|^.|%attr(755,root,root) %{_bindir}|; s|.so$||') > programs.list

#install programs/winhelp/hlp2sgml	$RPM_BUILD_ROOT%{_bindir}
#install tools/fnt2bdf			$RPM_BUILD_ROOT%{_bindir}

install -d \
        $RPM_BUILD_ROOT%{_winexdir}/windows/{system,Desktop,Favorites,Fonts} \
        "$RPM_BUILD_ROOT%{_winexdir}/windows/Start Menu/Programs/Startup" \
	$RPM_BUILD_ROOT%{_winexdir}/windows/{SendTo,ShellNew,system32,NetHood} \
	$RPM_BUILD_ROOT%{_winexdir}/windows/{Profiles/Administrator,Recent} \
	$RPM_BUILD_ROOT%{_winexdir}/{"Program Files/Common Files","My Documents"}

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/winex
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}

touch $RPM_BUILD_ROOT%{_winexdir}/{autoexec.bat,config.sys,windows/win.ini}
touch $RPM_BUILD_ROOT%{_winexdir}/windows/system/{shell.dll,shell32.dll}
touch $RPM_BUILD_ROOT%{_winexdir}/windows/system/{winsock.dll,wsock32.dll}

cat >$RPM_BUILD_ROOT%{_winexdir}/windows/system.ini <<EOF
[mci]
cdaudio=mcicda.drv
sequencer=mciseq.drv
waveaudio=mciwave.drv
avivideo=mciavi.drv
videodisc=mcipionr.drv
vcr=mciviscd.drv
MPEGVideo=mciqtz.drv
EOF

%if %{?debug:0}%{!?debug:1}
echo "Strip executable binaries and shared object files."
filelist=`find $RPM_BUILD_ROOT -type f ! -regex ".*ld-[0-9.]*so.*"`
elfexelist=`echo $filelist | xargs -r file | \
	awk '/ELF.*executable/ {print $1}' | cut -d: -f1`
elfsharedlist=`echo $filelist | xargs -r file | \
	awk '/LF.*shared object/ {print $1}' | cut -d: -f1`; \
if [ -n "$elfexelist" ]; then \
	strip -R .note -R .comment $elfexelist
fi
if [ -n "$elfsharedlist" ]; then
	strip --strip-unneeded -R .note  -R .comment $elfsharedlist
fi
%endif

/sbin/chpax -p $RPM_BUILD_ROOT%{_bindir}/wine

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

#%preun

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README DEVELOPERS-HINTS ChangeLog BUGS AUTHORS ANNOUNCE
#%doc documentation/wine-user
%attr(755,root,root) %{_bindir}/wine
%attr(755,root,root) %{_bindir}/winebuild
%attr(755,root,root) %{_bindir}/winemaker
%attr(755,root,root) %{_bindir}/wineserver
%attr(755,root,root) %{_bindir}/wineclipsrv
%attr(755,root,root) %{_bindir}/winelauncher
%attr(755,root,root) %{_bindir}/wineshelllink
%attr(755,root,root) %{_bindir}/winedump
%attr(755,root,root) %{_bindir}/wrc
%attr(755,root,root) %{_bindir}/wmc
%attr(755,root,root) %{_bindir}/fnt2bdf
%attr(755,root,root) %{_bindir}/function_grep.pl
%attr(755,root,root) %{_libdir}/*.so*
#%{_libdir}/winex
%{_mandir}/man[15]/*
%config(noreplace) %{_sysconfdir}/winex.reg
%config(missingok) %{_sysconfdir}/winex.systemreg
%config(missingok) %{_sysconfdir}/winex.userreg
%{_winexdir}

%files devel
%defattr(644,root,root,755)
#%doc documentation/{wine-devel,winelib-user,HOWTO-winelib}
%{_includedir}/winex
%{_libdir}/*.a