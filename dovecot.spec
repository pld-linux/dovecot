#
# Conditional build:
# _without_ldap		- without LDAP auth
# _without_pgsql	- without PostgreSQL auth
# _without_sasl		- without SASL auth
#
Summary:	IMAP and POP3 server written with security primarily in mind
Summary(pl):	Serwer IMAP i POP3 pisany g³ównie z my¶l± o bezpieczeñstwie
Name:		dovecot
Version:	0.99.10
Release:	2
License:	LGPL v2.1
Group:		Networking/Daemons
Source0:	http://dovecot.procontrol.fi/%{name}-%{version}.tar.gz
# Source0-md5:	26d8452366a28418cc8a114781a721b6
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-config.patch
URL:		http://dovecot.procontrol.fi/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_sasl:BuildRequires:	cyrus-sasl-devel >= 2.0}
BuildRequires:	libtool
%{!?_without_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.77.3
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
 - complete IMAP4rev1 support
 - supports THREAD and SORT extensions, required by many IMAP webmails
 - complete TLS/SSL support, using either GNUTLS or OpenSSL
 - IPv6 ready
 - shared mailboxes aren't yet supported
 - Maildir++ quota isn't yet supported; hard filesystem quota can also
   be problematic
 - mbox support isn't yet perfect - there's a few more or less
   theoretical problems, but nothing too bad.

%description -l pl
Dovecot to serwer IMAP i POP3 dla systemów linuksowych/uniksowych,
pisany g³ównie z my¶l± o bezpieczeñstwie. Chocia¿ jest pisany w C,
u¿ywa kilku technik kodowania zapobiegaj±cych wiêkszo¶ci popularnych
pu³apek.

Dovecot mo¿e dzia³aæ ze standardowymi formatami mbox i maildir, jest
ca³kowicie kompatybilny z serwerami UW-IMAP i Courier IMAP, a tak¿e z
klientami pocztowymi bezpo¶rednio dostaj±cymi siê do skrzynek.
Planowana jest tak¿e obs³uga przechowywania listów w bazach SQL.

Dovecot jest ³atwy do skonfigurowania i nie wymaga specjalnego
nadzoru. Wystarczy tylko doprowadziæ do dzia³ania uwierzytelnianie -
je¶li u¿ytkownicy s± w /etc/passwd, to w³a¶ciwie nie trzeba nic
zmieniaæ.

Dovecot powinien byæ w miarê szybki, g³ównie z powodu plików
indeksowych utrzymywanych przez serwer; zamiast potrzeby skanowania
wszystkich danych w skrzynce, Dovecot mo¿e ma³ym kosztem uzyskaæ
wiêkszo¶æ potrzebnych informacji z indeksu.

Stan:
 - powinien byæ gotowy do u¿ycia ze zwyk³ymi klientami IMAP
 - pe³na obs³uga IMAP4rev1
 - obs³uga rozszerzeñ THREAD i SORT, wymaganych przez wiele webmaili
   IMAP
 - obs³uga IPv6
 - jeszcze nie ma wspó³dzielonych skrzynek
 - quota Maildir++ jeszcze nie jest obs³ugiwana; twarda quota na
   systemach plików mo¿e sprawiaæ problemy
 - obs³uga mboksów jeszcze nie jest idealna - jest jeszcze kilka mniej
   lub bardziej teoretycznych problemów, ale nic strasznego.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?debug:--enable-debug} \
	%{!?_without_ldap:--with-ldap} \
	%{!?_without_pgsql:--with-pgsql} \
	%{!?_without_sasl:--with-cyrus-sasl2} \
	--with-ssl=openssl \
	--with-ssl-dir=/var/lib/openssl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,rc.d/init.d,sysconfig,security}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/{dovecot-example.conf,dovecot.conf}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

touch $RPM_BUILD_ROOT/etc/security/blacklist.imap

%clean
rm -rf $RPM_BUILD_ROOT

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

%files
%defattr(644,root,root,755)
# COPYING contains some notes, not actual LGPL text
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/*.txt doc/*.c*f
%attr(755,root,root) %{_sbindir}/%{name}
%config(noreplace) %verify(not size mtime md5) /etc/%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/pam.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/security/blacklist.imap
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_libdir}/%{name}
