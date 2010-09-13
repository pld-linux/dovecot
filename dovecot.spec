#
# Conditional build:
%bcond_without	gssapi	# without GSSAPI support
%bcond_without	ldap	# without LDAP auth
%bcond_without	mysql	# without MySQL auth
%bcond_without	pgsql	# without PostgreSQL auth
%bcond_without	sqlite	# without SQLite3 auth
%bcond_without	sasl	# without SASL auth
#
Summary:	IMAP and POP3 server written with security primarily in mind
Summary(pl.UTF-8):	Serwer IMAP i POP3 pisany głównie z myślą o bezpieczeństwie
Name:		dovecot
Version:	2.0.2
Release:	0.1
Epoch:		1
License:	MIT (libraries), LGPL v2.1 (the rest)
Group:		Networking/Daemons
Source0:	http://dovecot.org/releases/2.0/%{name}-%{version}.tar.gz
# Source0-md5:	e6386f44d027bd3f3f21400e162cf4f6
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-config.patch
URL:		http://dovecot.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_sasl:BuildRequires:	cyrus-sasl-devel >= 2.0}
BuildRequires:	gettext-devel
%{?with_gssapi:BuildRequires:	heimdal-devel}
BuildRequires:	libcap-devel
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.3}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite3-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	pam >= 0.79.0
Provides:	group(dovecot)
Provides:	imapdaemon
Provides:	user(dovecot)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems,
written with security primarily in mind. Although it's written with C,
it uses several coding techniques to avoid most of the common
pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail
clients accessing the mailboxes directly. It's also planned to support
storing mails in SQL databases.

Dovecot is easy to set up and doesn't require special maintenance.
Only thing you need is to get the authentication working properly - if
your users are in /etc/passwd there's hardly anything you have to do.

Dovecot should be pretty fast, mostly because of index files that
Dovecot maintains; instead of having to scan through all the data in
mailbox, Dovecot can get most of the wanted information from index
with little effort.

Status:
- should be quite ready for use with normal IMAP clients
- complete IMAP4rev1 and POP3 support
- supports THREAD, SORT and IDLE extensions, required by many IMAP
  webmails
- complete TLS/SSL support
- IPv6 ready
- shared mailboxes aren't yet supported
- Maildir++ quota is supported, bad hard filesystem quota can be
  problematic

%description -l pl.UTF-8
Dovecot to serwer IMAP i POP3 dla systemów linuksowych/uniksowych,
pisany głównie z myślą o bezpieczeństwie. Chociaż jest pisany w C,
używa kilku technik kodowania zapobiegających większości popularnych
pułapek.

Dovecot może działać ze standardowymi formatami mbox i maildir, jest
całkowicie kompatybilny z serwerami UW-IMAP i Courier IMAP, a także z
klientami pocztowymi bezpośrednio dostającymi się do skrzynek.
Planowana jest także obsługa przechowywania listów w bazach SQL.

Dovecot jest łatwy do skonfigurowania i nie wymaga specjalnego
nadzoru. Wystarczy tylko doprowadzić do działania uwierzytelnianie -
jeśli użytkownicy są w /etc/passwd, to właściwie nie trzeba nic
zmieniać.

Dovecot powinien być w miarę szybki, głównie z powodu plików
indeksowych utrzymywanych przez serwer; zamiast potrzeby skanowania
wszystkich danych w skrzynce, Dovecot może małym kosztem uzyskać
większość potrzebnych informacji z indeksu.

Stan:
- powinien być gotowy do użycia ze zwykłymi klientami IMAP
- pełna obsługa IMAP4rev1 i POP3
- obsługa rozszerzeń THREAD, SORT i IDLE, wymaganych przez wiele
  webmaili IMAP
- obsługa IPv6
- pełna obsługa TLS/SSL
- quota Maildir++ jest obsługiwana, ale twarda quota na systemach
  plików może być problematyczna

%package devel
Summary:	Development package for dovecot plugins
Summary(pl.UTF-8):	Pakiet programistyczny do tworzenia wtyczek dla dovecota
Group:		Development/Libraries
# doesn't require base

%description devel
Development package for dovecot plugins.

%description devel -l pl.UTF-8
Pakiet programistyczny do tworzenia wtyczek dla dovecota.

%prep
%setup -q
%patch0 -p1

%{__sed} -i 's,/usr/lib/dovecot,%{_libdir}/dovecot,g' doc/example-config/*.conf doc/example-config/conf.d/*.conf

%build
touch config.rpath
%{__libtoolize}
%{__aclocal} -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	%{?debug:--enable-debug} \
	%{?with_ldap:--with-ldap=yes} \
	%{?with_mysql:--with-mysql} \
	%{?with_pgsql:--with-pgsql} \
	%{?with_sqlite:--with-sqlite} \
	%{?with_gssapi:--with-gssapi} \
	--with-zlib \
	--with-bzlib \
	--with-libcap \
	--with-ssl=openssl \
	--with-moduledir=%{_libdir}/%{name}/plugins \
	--with-ssldir=/var/lib/openssl \
	--sysconfdir=/etc/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig,security}
install -d $RPM_BUILD_ROOT{/var/lib/dovecot,/var/run/dovecot/login}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/example-config/* $RPM_BUILD_ROOT%{_sysconfdir}/dovecot

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT/etc/security/blacklist.imap

rm $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins{,/*}/*.la

mv $RPM_BUILD_ROOT%{_libdir}/%{name}/dovecot-config $RPM_BUILD_ROOT%{_libdir}/%{name}-devel

rm -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 172 dovecot
%useradd -u 172 -d /usr/share/empty -s /bin/false -c "Dovecot server" -g dovecot dovecot

%post
/sbin/chkconfig --add dovecot
if [ -f /var/lock/subsys/dovecot ]; then
	/etc/rc.d/init.d/dovecot restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dovecot start\" to start dovecot daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dovecot ]; then
		/etc/rc.d/init.d/dovecot stop >&2
	fi
	/sbin/chkconfig --del dovecot
fi

%postun
if [ "$1" = "0" ]; then
	%userremove dovecot
	%groupremove dovecot
fi

%triggerpostun -- dovecot < 1:1.1
echo "Configuration change default_mail_env -> mail_location"
%{__sed} -i -e "s/^default_mail_env/mail_location/" /etc/dovecot/dovecot.conf

%files
%defattr(644,root,root,755)
# COPYING contains some notes, not actual LGPL text
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/*.txt doc/*.c*f doc/wiki/*.txt
%attr(755,root,root) %{_bindir}/doveadm
%attr(755,root,root) %{_bindir}/doveconf
%attr(755,root,root) %{_bindir}/dsync
%attr(755,root,root) %{_sbindir}/%{name}
%attr(751,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.ext
%attr(751,root,root) %dir %{_sysconfdir}/%{name}/conf.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/*.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/*.ext
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/anvil
%attr(755,root,root) %{_libdir}/%{name}/auth
%attr(755,root,root) %{_libdir}/%{name}/checkpassword-reply
%attr(755,root,root) %{_libdir}/%{name}/config
%attr(755,root,root) %{_libdir}/%{name}/deliver
%attr(755,root,root) %{_libdir}/%{name}/dict
%attr(755,root,root) %{_libdir}/%{name}/director
%attr(755,root,root) %{_libdir}/%{name}/dns-client
%attr(755,root,root) %{_libdir}/%{name}/doveadm-server
%attr(755,root,root) %{_libdir}/%{name}/dovecot-lda
%attr(755,root,root) %{_libdir}/%{name}/gdbhelper
%attr(755,root,root) %{_libdir}/%{name}/imap
%attr(755,root,root) %{_libdir}/%{name}/imap-login
%attr(755,root,root) %{_libdir}/%{name}/listview
%attr(755,root,root) %{_libdir}/%{name}/lmtp
%attr(755,root,root) %{_libdir}/%{name}/log
%attr(755,root,root) %{_libdir}/%{name}/maildirlock
%attr(755,root,root) %{_libdir}/%{name}/pop3
%attr(755,root,root) %{_libdir}/%{name}/pop3-login
%attr(755,root,root) %{_libdir}/%{name}/rawlog
%attr(755,root,root) %{_libdir}/%{name}/script
%attr(755,root,root) %{_libdir}/%{name}/script-login
%attr(755,root,root) %{_libdir}/%{name}/ssl-params
%attr(755,root,root)%{_libdir}/%{name}/lib*.so*
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%dir %{_libdir}/%{name}/plugins/doveadm
%attr(755,root,root)%{_libdir}/%{name}/plugins/doveadm/*.so
%dir /var/lib/dovecot
%dir /var/run/dovecot
%attr(750,root,dovecot) %dir /var/run/dovecot/login

%{_mandir}/man1/deliver.1*
%{_mandir}/man1/dove*.1*
%{_mandir}/man1/dsync.1*
%{_mandir}/man7/doveadm-search-query.7*

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}-devel
%{_includedir}/%{name}
%{_aclocaldir}/dovecot.m4
