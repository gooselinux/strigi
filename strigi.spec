
Name:		strigi
Version:	0.7.0
Release:	2%{?dist}
Summary:	A desktop search program
Group:		Applications/Productivity
License:	LGPLv2+
#URL:           http://strigi.sf.net/
URL:            http://www.vandenoever.info/software/strigi/
Source0:	http://www.vandenoever.info/software/strigi/strigi-%{version}%{?pre:-%{pre}}.tar.bz2
Source1:	strigiclient.desktop
Source2:	strigi-daemon.desktop
Patch0:		strigi-0.6.2-multilib.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake >= 2.4.5
BuildRequires:	clucene-core-devel qt4-devel dbus-devel
BuildRequires:	libxml2-devel expat-devel bzip2-devel zlib-devel
BuildRequires:	cppunit-devel exiv2-devel
BuildRequires:  bison
BuildRequires:	desktop-file-utils

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Strigi is a fast and light desktop search engine. It can handle a large range
of file formats such as emails, office documents, media files, and file
archives. It can index files that are embedded in other files. This means email
attachments and files in zip files are searchable as if they were normal files
on your harddisk.

Strigi is normally run as a background daemon that can be accessed by many
other programs at once. In addition to the daemon, Strigi comes with powerful
replacements for the popular unix commands 'find' and 'grep'. These are called
'deepfind' and 'deepgrep' and can search inside files just like the strigi
daemon can.

%package	devel
Summary:	Development files for the strigi desktop search engine
Group:		Development/Libraries
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
Development files for the strigi desktop search engine

%package	libs
Summary:	Strigi libraries
Group:		Development/Libraries

%description	libs
Strigi search engine libraries

%prep
%setup -q -n %{name}-%{version}%{?pre:-%{pre}}
%patch0 -p1 -b .multilib

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%cmake \
  -DLIB_DESTINATION=%{_libdir} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf %{buildroot}
make install/fast -C %{_target_platform}  DESTDIR=%{buildroot}

desktop-file-install					\
	--vendor="fedora"				\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{SOURCE1}

# Add an autostart desktop file for the strigi daemon
install -p -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop

%check
make -C %{_target_platform}/tests

%clean
rm -rf %{buildroot}

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/*
%{_datadir}/applications/*strigiclient.desktop
%{_datadir}/dbus-1/services/*.service
%{_sysconfdir}/xdg/autostart/strigi-daemon.desktop

%files devel
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libstream*.pc
%{_libdir}/strigi/*.cmake
%{_includedir}/strigi/

%files libs
%defattr(-,root,root,-)
%{_datadir}/strigi/
%{_libdir}/libsearchclient.so.0*
%{_libdir}/libstreamanalyzer.so.0*
%{_libdir}/libstreams.so.0*
%{_libdir}/libstrigihtmlgui.so.0*
%{_libdir}/libstrigiqtdbusclient.so.0*
%dir %{_libdir}/strigi/
%{_libdir}/strigi/strigi*.so

%changelog
* Tue May 18 2010 Lukas Tinkl <ltinkl@redhat.com> - 0.7.0-2
- Resolves: #587907 - strigi does not have a menu icon

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.7.0-1.1
- Rebuilt for RHEL 6

* Tue Aug 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.7.0-1
- strigi-0.7.0 (final)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-0.2.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Rex Dieter <rdieter@fedoraproject.org> 0.7-0.1.RC1
- strigi-0.7-RC1
- use %%_isa where appropriate
- %%files: track lib sonames
- strigi-daemon.desktop: +Hidden=true (ie, disable autostart by default)

* Mon Jun 29 2009 Lukáš Tinkl <ltinkl@redhat.com> - 0.6.5-2
- don't start strigi daemon unconditionally (#487322)

* Fri May 29 2009 Lukáš Tinkl <ltinkl@redhat.com> - 0.6.5-1
- Strigi 0.6.5

* Tue Apr 21 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.6.4-4
- fix crash with / char in path (#496620, kde#185551)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Deji Akingunola <dakingun@gmail.com> - 0.6.4-2
- Add patch to build with gcc-4.4

* Mon Feb 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.4-1
- strigi-0.6.4
- Summary: s/for KDE//
- *.desktop: validate, remove OnlyShowIn=KDE
- -devel: move *.cmake here

* Mon Jan 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.3-1
- strigi-0.6.3

* Tue Jan 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.6.2-1
- strigi-0.6.2
- use %%cmake macro

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.5.11.1-2 
- respin (exiv2)

* Thu Nov 27 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 0.5.11.1-1
- drop _default_patch_fuzz
- rebase strigi-multilib patch
- No official 0.5.11.1 tarballs were released but we need 0.5.11.1, apply a
  diff between 0.5.11 and 0.5.11.1 svn tags

* Sun Jul 20 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.11-1
- Update to 0.5.11
- Drop compile-fix and lucenetest_fix patches (fixed upstream)

* Sat May 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.9-2
- Disable 'make test' for now, seems the buildroot cannot find java

* Sat May 03 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.9-1
- Update to 0.5.9 (bugfix release)

* Thu Mar 06 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.8-2
- Use upstream's default build options (disable inotify support, #436096)

* Thu Feb 21 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.8-1
- Update to 0.5.8
- Fix LIB_DESTINATION (#433627)
- Drop GCC 4.3 patch (fixed upstream)

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.7-4
- Rebuild for GCC 4.3

* Fri Jan 11 2008 Deji Akingunola <dakingun@gmail.com> - 0.5.7-3
- Fix build failure with gcc-4.3

* Tue Nov 13 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.5.7-2
- Rebuild for new exiv2

* Tue Oct 30 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.7-1
- Update to 0.5.7 release
- Fix multilibs conflict (Bug #343221, patch by Kevin Kofler)

* Sun Sep 09 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.5-2
- Rebuild for BuildID changes

* Sat Aug 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.5-1
- Update to 0.5.5 release

* Mon Aug 06 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-1
- Update to 0.5.4 proper
- License tag update

* Sun Jul 29 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.4-0.1.svn20070729
- New KDE SVN snapshot version for KDE 4.0 beta 1 (bz#20015)

* Wed May 16 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-5
- Split out a strigi-libs subpackage as suggested in BZ#223586
_ Include a strigidaemon autostart desktop file

* Sat May 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-4
- Add dbus-devel BR.

* Sat May 05 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-3
- Misc. fixes from package review

* Fri May 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-2
- Updates from reviews:
-	Have the -devel subpackage require pkgconfig
-	Add a versioned dependency on cmake and remove dbus-qt buildrequire

* Fri May 04 2007 Deji Akingunola <dakingun@gmail.com> - 0.5.1-1
- New release

* Wed May 02 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-3
- Allow building on FC6

* Thu Feb 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-2
- Assorted fixed arising from reviews

* Wed Jan 17 2007 Deji Akingunola <dakingun@gmail.com> - 0.3.11-1
- Initial packaging for Fedora Extras
