#
# Conditional build:
# _without_ldap		- without LDAP auth
# _without_pgsql	- without PostgreSQL auth
# _without_sasl		- without SASL auth
#
Summary:	IMAP and POP3 server written with security primarily in mind
Summary(pl):	Serwer IMAP i POP3 pisany g��wnie z my�l� o bezpiecze�stwie
Name:		dovecot
Version:	0.99.10
Release:	0.1
License:	LGPL v2.1
Group:		Networking/Daemons
Source0:	http://dovecot.procontrol.fi/%{name}-%{version}.tar.gz
# Source0-md5:	26d8452366a28418cc8a114781a721b6
URL:		http://dovecot.procontrol.fi/
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_sasl:BuildRequires:	cyrus-sasl-devel >= 2.0}
BuildRequires:	libtool
%{!?_without_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
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
mailbox, Dovecot can get most of the wanted information from index with
little effort.

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
 - pe�na obs�uga IMAP4rev1
 - obs�uga rozszerze� THREAD i SORT, wymaganych przez wiele webmaili
   IMAP
 - obs�uga IPv6
 - jeszcze nie ma wsp�dzielonych skrzynek
 - quota Maildir++ jeszcze nie jest obs�ugiwana; twarda quota na
   systemach plik�w mo�e sprawia� problemy
 - obs�uga mboks�w jeszcze nie jest idealna - jest jeszcze kilka
   mniej lub bardziej teoretycznych problem�w, ale nic strasznego.

%prep
%setup -q

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/{dovecot-example.conf,dovecot.conf}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# COPYING contains some notes, not actual LGPL text
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/*.txt doc/*.c*f
%attr(755,root,root) %{_sbindir}/dovecot
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dovecot.conf
%attr(755,root,root) %{_libdir}/dovecot
