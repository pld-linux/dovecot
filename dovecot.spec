#
# Conditional build:
%bcond_without	ldap	# without LDAP auth
%bcond_without	mysql	# without MySQL auth
%bcond_without	pgsql	# without PostgreSQL auth
%bcond_without	sqlite	# without SQLite3 auth
%bcond_without	sasl	# without SASL auth
#
Summary:	IMAP and POP3 server written with security primarily in mind
Summary(pl.UTF-8):	Serwer IMAP i POP3 pisany głównie z myślą o bezpieczeństwie
Name:		dovecot
Version:	1.1.beta5
Release:	1
License:	LGPL v2.1 and MIT
Group:		Networking/Daemons
Source0:	http://dovecot.org/releases/1.1/beta/%{name}-%{version}.tar.gz
# Source0-md5:	5d3709c82bc9adc52f7d3ff62c86c706
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-config.patch
#Patch1:		%{name}-dspam-plugin.patch
Patch1:	%{name}-sort-assert.patch
URL:		http://dovecot.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_sasl:BuildRequires:	cyrus-sasl-devel >= 2.0}
#BuildRequires:	krb5-devel
BuildRequires:	gettext-devel
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	sed >= 4.0
%{?with_sqlite:BuildRequires:	sqlite3-devel}
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	pam >= 0.79.0
Provides:	group(dovecot)
Provides:	user(dovecot)
Provides:	imapdaemon
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
Summary: Libraries and headers for Dovecot
Group: Development/Libraries
Requires: %name = %{version}-%{release}

%description devel
This package contains development files for linking against %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%{__sed} -i 's,/usr/lib/dovecot,%{_libdir}/dovecot,g' dovecot-example.conf

%build
touch config.rpath
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	%{?with_ldap:--with-ldap} \
	%{?with_mysql:--with-mysql} \
	%{?with_pgsql:--with-pgsql} \
	%{?with_sasl:--with-cyrus-sasl2} \
	%{?with_sqlite:--with-sqlite} \
	--with-gssapi \
	--with-ssl=openssl \
	--with-ssl-dir=/var/lib/openssl \
	--sysconfdir=/etc/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig,security}
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}
install -d $RPM_BUILD_ROOT{/var/lib/dovecot,/var/run/dovecot/login}

%{__make} install \
	moduledir=%{_libdir}/%{name}/plugins \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{dovecot-example.conf,dovecot.conf}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT/etc/security/blacklist.imap

# devel 
for folder in deliver imap lib lib-imap lib-mail lib-storage; do
    mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}/$folder
    install -p -m644 src/$folder/*.h $RPM_BUILD_ROOT%{_includedir}/%{name}/$folder/
done

for folder in lib lib-imap lib-mail lib-storage; do
    mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/$folder
    install -p -m644 src/$folder/*.a $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/$folder/
done
		
for f in dovecot-config config.h stamp.h; do
    install -p -m644 $f $RPM_BUILD_ROOT%{_includedir}/%{name}
done
		    

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

%files
%defattr(644,root,root,755)
# COPYING contains some notes, not actual LGPL text
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/*.txt doc/*.c*f doc/wiki/*.txt
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}pw
%attr(750,root,root) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
#Files :P
%dir %{_libdir}/%{name}/
%attr(755,root,root) %{_libdir}/%{name}/checkpassword-reply
%attr(755,root,root) %{_libdir}/%{name}/deliver
%attr(755,root,root) %{_libdir}/%{name}/dict
%attr(755,root,root) %{_libdir}/%{name}/dovecot-auth
%attr(755,root,root) %{_libdir}/%{name}/gdbhelper
%attr(755,root,root) %{_libdir}/%{name}/idxview
%attr(755,root,root) %{_libdir}/%{name}/imap
%attr(755,root,root) %{_libdir}/%{name}/imap-login
%attr(755,root,root) %{_libdir}/%{name}/logview
%attr(755,root,root) %{_libdir}/%{name}/pop3
%attr(755,root,root) %{_libdir}/%{name}/pop3-login
%attr(755,root,root) %{_libdir}/%{name}/rawlog
%attr(755,root,root) %{_libdir}/%{name}/ssl-build-param
%dir %{_libdir}/%{name}/plugins/
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%dir %{_libdir}/%{name}/plugins/imap
%attr(755,root,root)%{_libdir}/%{name}/plugins/imap/*.so
%dir %{_libdir}/%{name}/plugins/lda
%attr(755,root,root) %{_libdir}/%{name}/plugins/lda/*.so
%dir %{_libdir}/%{name}/plugins/pop3
%attr(755,root,root) %{_libdir}/%{name}/plugins/pop3/*.so
%dir /var/lib/dovecot
%dir /var/run/dovecot
%attr(750,root,dovecot) %dir /var/run/dovecot/login

%files devel
%defattr(644,root,root,755)
%{_libdir}/%{name}/plugins/*.a
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.la
%{_libdir}/%{name}/plugins/imap/*.a
%attr(755,root,root) %{_libdir}/%{name}/plugins/imap/*.la
%{_libdir}/%{name}/plugins/lib/*.a
%{_libdir}/%{name}/plugins/lib-imap/*.a
%{_libdir}/%{name}/plugins/lib-mail/*.a
%{_libdir}/%{name}/plugins/lib-storage/*.a
%{_includedir}/%{name}
