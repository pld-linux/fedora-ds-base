%define shortname fedora-ds
%define pkgname   dirsrv

Summary:	Fedora Directory Server (base)
Name:		fedora-ds-base
Version:	1.1.0
Release:	0.1
License:	GPLv2 with exceptions
Group:		Daemons
Source0:	http://directory.fedoraproject.org/sources/%{name}-%{version}.tar.bz2
# Source0-md5:	a60d1ce51207e61c48b70aa85ae5e5a5
URL:		http://directory.fedoraproject.org/
BuildRequires:	bzip2-devel
BuildRequires:	cyrus-sasl-devel
BuildRequires:	db-devel
BuildRequires:	icu
BuildRequires:	libicu-devel
BuildRequires:	libselinux-devel
%ifnarch sparc sparc64 ppc ppc64
BuildRequires:	lm_sensors-devel
%endif
BuildRequires:	mozldap-devel
BuildRequires:	net-snmp-devel
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	svrcore-devel
BuildRequires:	zlib-devel
Requires:	apache-mod_actions
Requires:	apache-mod_cache
Requires:	apache-mod_deflate
Requires:	apache-mod_dir
Requires:	apache-mod_expires
Requires:	apache-mod_file_cache
Requires:	apache-mod_unique_id
Requires:	apache-mod_rewrite
Requires:	apache-mod_vhost_alias
Requires:	mozldap-tools
Requires:	perl-Mozilla-LDAP
Requires:	nss-tools
Requires:	cyrus-sasl-gssapi
#Requires:	cyrus-sasl-md5
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fedora Directory Server is an LDAPv3 compliant server. The base
package includes the LDAP server and command line utilities for server
administration.

%package          devel
Summary:	Development libraries for Fedora Directory Server
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description      devel
Development Libraries and headers for the Fedora Directory Server base
package.

%prep
%setup -q

%build
%configure

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	 DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/log/%{pkgname}
install -d $RPM_BUILD_ROOT/var/lib/%{pkgname}
install -d $RPM_BUILD_ROOT/var/lock/%{pkgname}
install -d $RPM_BUILD_ROOT%{_includedir}/%{pkgname}

#remove libtool and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.la

install -p ldap/servers/slapd/slapi-plugin.h $RPM_BUILD_ROOT%{_includedir}/%{pkgname}/

# make sure perl scripts have a proper shebang
sed -i -e 's|#{{PERL-EXEC}}|#!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/script-templates/template-*.pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{pkgname}
/sbin/ldconfig


%preun
if [ $1 = 0 ]; then
        %service %{pkgname} stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{pkgname}
fi

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE EXCEPTION
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/schema
%config(noreplace)%{_sysconfdir}/%{pkgname}/schema/*.ldif
%dir %{_sysconfdir}/%{pkgname}/config
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/slapd-collations.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/certmap.conf
%config(noreplace)%verify(not md5 mtime size) /etc/sysconfig/%{pkgname}
%{_datadir}/%{pkgname}
/etc/rc.d/init.d/%{pkgname}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/%{pkgname}
%attr(755,root,root) %{_libdir}/%{pkgname}/*.so.*
%{_libdir}/%{pkgname}/perl
%dir %{_libdir}/%{pkgname}/plugins
%{_libdir}/%{pkgname}/plugins/*.so
%dir %{_localstatedir}/lib/%{pkgname}
%dir %{_localstatedir}/log/%{pkgname}
%dir %{_localstatedir}/lock/%{pkgname}

%files devel
%defattr(644,root,root,755)
%doc LICENSE EXCEPTION
%{_includedir}/%{pkgname}
%{_libdir}/%{pkgname}/*.so
