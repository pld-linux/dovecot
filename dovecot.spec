Summary:	IMAP and POP3 server written with security primarily in mind
Name:		dovecot
Version:	0.99.10
Release:	0.1
License:	LGPL v2.1
Group:		Networking/Daemons
Source0:	http://dovecot.procontrol.fi/%{name}-%{version}.tar.gz
# Source0-md5:	26d8452366a28418cc8a114781a721b6
URL:		http://dovecot.procontrol.fi/
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
 - Maildir++ quota isn't yet supported. Hard filesystem quota can also
   be problematic.
 - mbox support isn't yet perfect - there's a few more or less
   theoretical problems, but nothing too bad.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

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
