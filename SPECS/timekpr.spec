# sitelib for noarch packages, sitearch for others (remove the unneeded one)
#%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
#%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%global debug_package %{nil}

Name:           timekpr
# Ubuntu version 0.3.6~ppa1~ubuntu11
Version:        0.3.6
Release:        6.3%{?dist}
Summary:        Keep control of computer usage

Group:    System Environment/Daemons
License:  GPLv3
URL:      https://launchpad.net/timekpr-revived
# The source of this package was pulled from upstreams's vcs.
# Use the following command to generate the tar ball:
# bzr branch lp:~mjasnik/timekpr-revived/stable
# tar cvzf %{name}-%{version}.tar.gz stable
Source0:  timekpr-0.3.6.tar.gz
Source1:  timekpr.service
Source2:  timekpr.postinst
Source3:  timekpr.postrm
Source4:  timekpr.pam
Source5:  timekpr.appdata.xml
Source6:  timekpr-gui-run
Source7:  org.freedesktop.policykit.pkexec.timekpr.policy

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

Patch0:         0001-timekpr.desktop.patch
Patch1:         0002-timekpr-client.desktop.patch
Patch2:         0003-timekpr-pythondir.patch
Patch3:         0004-timekpr-pythonfix.patch
Patch4:         0005-timekpr-cleanup-users-list.patch

BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libappstream-glib
BuildRequires:  systemd

Requires:       python
Requires:       pygtk2-libglade
Requires:       dbus-python
Requires:       notify-python

Requires(post): systemd
Requires(post): sed
Requires(preun): systemd
Requires(postun): systemd
Requires(postun): sed

%description
This program will track and control the computer usage of
your user accounts. You can limit their daily usage based
on a timed access duration and configure periods of day
when they can or cannot log in.
.
Any bugs should be reported to our bug tracker:
https://bugs.launchpad.net/timekpr-revived/+bugs

%prep
%setup -q -n stable

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# Remove CFLAGS=... for noarch packages (unneeded)
#CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#Initial mkdirs

%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_datadir}/py%{name}
%__mkdir_p %{buildroot}%{_datadir}/%{name}
%__mkdir_p %{buildroot}%{_datadir}/applications/
%__mkdir_p %{buildroot}%{_datadir}/locale/
%__mkdir_p %{buildroot}%{_datadir}/pixmaps/
%__mkdir_p %{buildroot}%{_datadir}/polkit-1/actions/
%__mkdir_p %{buildroot}/etc/xdg/autostart/
%__mkdir_p %{buildroot}%{_sysconfdir}/%{name}/
%__mkdir_p %{buildroot}%{_sysconfdir}/logrotate.d/
%__mkdir_p %{buildroot}%{_datadir}/autostart/
%__mkdir_p %{buildroot}%{_sysconfdir}/pam.d/
%__mkdir_p %{buildroot}%{_datadir}/man/man8/
%__mkdir_p %{buildroot}%{_unitdir}

#Copy files
#Config file
%__cp support/etc/timekpr.conf %{buildroot}%{_sysconfdir}/
%__cp support/etc/logrotate.d/timekpr %{buildroot}%{_sysconfdir}/logrotate.d/

#Timekpr file
%__cp src/timekpr.py %{buildroot}%{_datadir}/py%{name}/
%__cp src/timekpr-gui.py %{buildroot}%{_datadir}/py%{name}/
%__cp src/timekpr-client.py %{buildroot}%{_datadir}/py%{name}/

%__cp src/common/timekprpam.py %{buildroot}%{_datadir}/py%{name}/
%__cp src/common/timekprcommon.py %{buildroot}%{_datadir}/py%{name}/

%__cp support/bin/timekpr %{buildroot}%{_bindir}
%__cp support/bin/timekpr-gui %{buildroot}%{_bindir}
%__cp %{SOURCE6} %{buildroot}%{_bindir}
%__cp support/bin/timekpr-client %{buildroot}%{_bindir}
%__cp support/bin/users.timekpr %{buildroot}%{_bindir}

#Images files
%__cp icons/padlock-green.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/padlock-limited-green.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/padlock-limited-red.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/padlock-limited-yellow.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/padlock-red.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/padlock-unlimited-green.png %{buildroot}%{_datadir}/%{name}/

%__cp icons/timekpr32x32.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/timekpr64x64.png %{buildroot}%{_datadir}/%{name}/
%__cp icons/timekpr100x100.png %{buildroot}%{_datadir}/%{name}/

%__cp icons/timekpr.xpm %{buildroot}%{_datadir}/pixmaps/

%__cp src/gui/timekpr.glade %{buildroot}%{_datadir}/%{name}/
%__cp src/gui/about_dialog.ui %{buildroot}%{_datadir}/%{name}/
%__cp src/gui/client.ui %{buildroot}%{_datadir}/%{name}/

#PolKit policy
%__cp %{SOURCE7} %{buildroot}%{_datadir}/polkit-1/actions/

#Appdata file
install -Dpm 0644 %{SOURCE5} \
%{buildroot}%{_datadir}/appdata/timekpr.appdata.xml
appstream-util validate-relax --nonet \
%{buildroot}%{_datadir}/appdata/timekpr.appdata.xml

#Desktop files
%__cp src/launchers/timekpr.desktop %{buildroot}%{_datadir}/applications/
%__cp src/launchers/timekpr-client.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/
%__cp src/launchers/timekpr-client.desktop %{buildroot}%{_datadir}/autostart/
#Don't work: fix the dir
#desktop-file-install --vendor="" --dir=%{buildroot}%{_datadir}/applications/ %{buildroot}%{_datadir}/applications/timekpr.desktop

#Locale stuff
%__cp -r locale/da %{buildroot}%{_datadir}/locale/
%__cp -r locale/de %{buildroot}%{_datadir}/locale/
%__cp -r locale/fi %{buildroot}%{_datadir}/locale/
%__cp -r locale/fr %{buildroot}%{_datadir}/locale/
%__cp -r locale/hu %{buildroot}%{_datadir}/locale/
%__cp -r locale/lv %{buildroot}%{_datadir}/locale/
%__cp -r locale/nb %{buildroot}%{_datadir}/locale/
%__cp -r locale/ru %{buildroot}%{_datadir}/locale/
%__cp -r locale/sl %{buildroot}%{_datadir}/locale/
%__cp -r locale/sv %{buildroot}%{_datadir}/locale/
#%find_lang %{name}

#man
%__cp doc/timekpr.8 %{buildroot}%{_datadir}/man/man8/%{name}.8

#post install, post uninstall
%__cp %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/
%__cp %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/

#systemd
%__cp %{SOURCE1} %{buildroot}%{_unitdir}

#pam include
%__cp %{SOURCE4} %{buildroot}%{_sysconfdir}/pam.d/timekpr

#chmod on bin (in source : timekpr-client is not exacutable, needed)
chmod +x %{buildroot}%{_bindir}/timekpr
chmod +x %{buildroot}%{_bindir}/timekpr-gui
chmod +x %{buildroot}%{_bindir}/timekpr-gui-run
chmod +x %{buildroot}%{_bindir}/timekpr-client

%post
#service
#%systemd_post timekpr.service not in preset
if [  $1 == 1 ]
then
    %{_sysconfdir}/%{name}/timekpr.postinst
   systemctl enable timekpr.service
   systemctl start timekpr
fi

#Update icons
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%preun
%systemd_preun timekpr.service
if [  $1 == 0  ]
then
    %{_sysconfdir}/%{name}/timekpr.postrm
fi

%postun
%systemd_postun_with_restart timekpr.service

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%files
%defattr(-,root,root,-)
%doc COPYRIGHT.txt README.txt CONTRIBUTORS.txt debian/changelog
%dir %{_sysconfdir}/%{name}
%config /etc/%{name}.conf
%config %{_sysconfdir}/logrotate.d/%{name}

%{_bindir}/timekpr
%{_bindir}/timekpr-gui
%{_bindir}/timekpr-gui-run
%{_bindir}/timekpr-client
%{_bindir}/users.timekpr
%dir %{_datadir}/py%{name}
%{_datadir}/py%{name}/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/timekpr.desktop
%{_datadir}/appdata/timekpr.appdata.xml
%{_sysconfdir}/xdg/autostart/timekpr-client.desktop
%{_sysconfdir}/pam.d/%{name}
%{_datadir}/autostart/timekpr-client.desktop
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/locale/*/LC_MESSAGES/%{name}.po
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.pkexec.timekpr.policy
%{_datadir}/man/man8/%{name}.8.gz
%{_unitdir}/timekpr.service

%{_sysconfdir}/%{name}/timekpr.postinst
%{_sysconfdir}/%{name}/timekpr.postrm

%changelog
* Sun Nov 27 2016 johan.heikkila@gmail.com
- Removed beesu dependence
* Sun Nov 6 2016 johan.heikkila@gmail.com
- Update to 3.6 for Fedora
* Sat Oct 11 2014 denis@shnoulle.net
- Update to 3.5
- Use own postinst
- Use pytimekpr directory
* Fri Oct 10 2014 denis@shnoulle.net
- Enable service
- Deactivate postinst
* Sat Oct 4 2014 denis@shnoulle.net
- Try to build timekpr for fedora
