#
# Conditional build:
%bcond_without	ldap	# without LDAP auth
%bcond_without	mysql	# without MySQL auth
%bcond_without	pgsql	# without PostgreSQL auth
%bcond_without	sqlite	# without  SQLite3 auth
%bcond_without	sasl	# without SASL auth
#
Summary:	IMAP and POP3 server written with security primarily in mind
Summary(pl):	Serwer IMAP i POP3 pisany g��wnie z my�l� o bezpiecze�stwie
Name:		dovecot
Version:	1.0.1
Release:	2
License:	LGPL v2.1 and MIT
Group:		Networking/Daemons
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0878f744382417fce09d83f5b1c14030
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-config.patch
Patch1:		%{name}-branch.diff
URL:		http://dovecot.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_sasl:BuildRequires:	cyrus-sasl-devel >= 2.0}
BuildRequires:	heimdal-devel
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

%description -l pl
Dovecot to serwer IMAP i POP3 dla system�w linuksowych/uniksowych,
pisany g��wnie z my�l� o bezpiecze�stwie. Chocia� jest pisany w C,
u�ywa kilku technik kodowania zapobiegaj�cych wi�kszo�ci popularnych
pu�apek.

Dovecot mo�e dzia�a� ze standardowymi formatami mbox i maildir, jest
ca�kowicie kompatybilny z serwerami UW-IMAP i Courier IMAP, a tak�e z
klientami pocztowymi bezpo�rednio dostaj�cymi si� do skrzynek.
Planowana jest tak�e obs�uga przechowywania list�w w bazach SQL.

Dovecot jest �atwy do skonfigurowania i nie wymaga specjalnego
nadzoru. Wystarczy tylko doprowadzi� do dzia�ania uwierzytelnianie -
je�li u�ytkownicy s� w /etc/passwd, to w�a�ciwie nie trzeba nic
zmienia�.

Dovecot powinien by� w miar� szybki, g��wnie z powodu plik�w
indeksowych utrzymywanych przez serwer; zamiast potrzeby skanowania
wszystkich danych w skrzynce, Dovecot mo�e ma�ym kosztem uzyska�
wi�kszo�� potrzebnych informacji z indeksu.

Stan:
- powinien by� gotowy do u�ycia ze zwyk�ymi klientami IMAP
- pe�na obs�uga IMAP4rev1 i POP3
- obs�uga rozszerze� THREAD, SORT i IDLE, wymaganych przez wiele
  webmaili IMAP
- obs�uga IPv6
- pe�na obs�uga TLS/SSL
- quota Maildir++ jest obs�ugiwana, ale twarda quota na systemach
  plik�w mo�e by� problematyczna

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
%attr(755,root,root) %{_libdir}/%{name}
%dir /var/lib/dovecot
%dir /var/run/dovecot
%attr(750,root,dovecot) %dir /var/run/dovecot/login
