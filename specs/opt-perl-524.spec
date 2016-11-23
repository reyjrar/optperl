%define perl_version    5.24.0
%define perl_epoch      1
%define perl_admin      brad@divisionbyzero.net
%define opt_prefix 	/opt/perl/%{perl_version}

Name:           opt-perl-524
Version:        %{perl_version}
Release:        1
Epoch:          %{perl_epoch}
Summary:        The Perl programming language
Group:          Development/Languages
License:        (GPL+ or Artistic) and (GPLv2+ or Artistic)
Url:            http://www.perl.org/
Source0:        perl-%{perl_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{perl_version}-root-%(%{__id_u} -n)
BuildRequires:  tcsh, dos2unix, man, groff
BuildRequires:  gdbm-devel, db4-devel, zlib-devel
BuildRequires:  procps
BuildRequires:  gawk
Provides: opt-perl
# USE THIS WITH CAUTION #
AutoReqProv: 0

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications are system
administration utilities and web programming.  A large proportion of
the CGI scripts on the web are written in Perl.  You need the perl
package installed on your system so that your system can handle Perl
scripts.

Install this package if you want to program in Perl or enable your
system to handle Perl scripts.

%prep
%setup -q -n perl-%{perl_version}

%build
echo "RPM Build arch: %{_arch}"

# yes; don't use %_libdir so that noarch packages from other OSs
# arches work correctly :\ the Configure lines below hardcode lib for
# similar reasons.

/bin/sh Configure -des -Doptimize="$RPM_OPT_FLAGS" \
        -Dversion=%{perl_version} \
        -Dmyhostname=localhost \
        -Dperladmin=%{perl_admin}\
        -Dcc='%{__cc}' \
        -Dcf_by='Off-System Perl' \
        -Dinstallprefix=%{opt_prefix} \
        -Dprefix=%{opt_prefix} \
        -Darchname=%{_arch}-%{_os} \
        -Dvendorprefix=%{opt_prefix} \
        -Dsiteprefix=%{opt_prefix} \
        -Duseshrplib \
        -Dusethreads \
        -Duseithreads \
        -Duselargefiles \
        -Dd_dosuid=n \
        -Dd_semctl_semun \
        -Di_db \
        -Ui_ndbm \
        -Di_gdbm \
        -Di_shadow \
        -Di_syslog \
        -Dman3ext=3pm \
        -Duseperlio \
        -Dinstallusrbinperl=n \
        -Ubincompat5005 \
        -Uversiononly \
        -Dotherlibdirs=/opt/perl/lib \
        -Dpager='/usr/bin/less -isr' \
        -Dd_gethostent_r_proto -Ud_endhostent_r_proto -Ud_sethostent_r_proto \
        -Ud_endprotoent_r_proto -Ud_setprotoent_r_proto \
        -Ud_endservent_r_proto -Ud_setservent_r_proto \
        -Dscriptdir='%{opt_prefix}/bin'

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*NDBM*' | xargs rm -rfv

find $RPM_BUILD_ROOT -type f -name '*.bs' -a -empty -exec rm -f {} ';'

chmod -R u+w $RPM_BUILD_ROOT/*

# Compress Changes* to save space
%{__gzip} Changes*

%clean
rm -rf $RPM_BUILD_ROOT

#%check
#make test

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{opt_prefix}/
# Old changelog entries are preserved in CVS.
%changelog


