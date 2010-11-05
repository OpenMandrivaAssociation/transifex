%define confdir %{_sysconfdir}/%{name}

Name:       transifex
Version:    1.0.0
Release:    %mkrel 2
Summary:    A system for distributed translation submissions

Group:      Networking/WWW
License:    GPLv2
URL:        http://transifex.org
Source0:    transifex-%version.tar.gz
Source1:    django-settings.py.in
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:  noarch

BuildRequires:  python-sphinx 
BuildRequires:  gettext 
BuildRequires:  python-markdown
BuildRequires:  python-django 
BuildRequires:  python-django-contact-form 
BuildRequires:  python-django-pagination 
BuildRequires:  python-django-tagging
BuildRequires:  python-django-notification 
BuildRequires:  python-django-profile 
BuildRequires:  python-django-south > 0.7
BuildRequires:  python-django-piston
BuildRequires:  python-django-authority 
BuildRequires:  python-django-ajax-selects
BuildRequires:	python-django-filter
BuildRequires:	python-django-sorting
BuildRequires:	python-django-tagging
BuildRequires:	python-django-piston
BuildRequires:	python-django-threadedcomments
BuildRequires:	python-django-staticfiles
BuildRequires:	python-django-addons
BuildRequires:	python-markdown
BuildRequires:	python-magic
BuildRequires:	python-polib

Requires:   mercurial >= 1.3 
Requires:   python-urlgrabber 
Requires:   intltool >= 0.37.1
Requires:   python-markdown 
Requires:   python-pygments 
Requires:   python-polib >= 0.4.2
Requires:   python-django 
Requires:   python-django-contact-form 
Requires:   python-django-pagination 
Requires:   python-django-tagging
Requires:   python-django-notification 
Requires:   python-django-profile 
Requires:   python-django-south 
Requires:   python-django-piston
Requires:   python-django-authority 
Requires:   python-django-ajax-selects
Requires:   python-django-staticfiles
Requires:   python-django-addons
Requires:   python-django-threadedcomments
Requires:   python-django-sorting
Requires:   python-googlechart

%description
Transifex is a web-system that facilitates the process of submitting
translations in remote and disparate version control systems (VCS).

%package extras
Summary:    Additional support for Transifex
Group:      Networking/WWW
Requires:   transifex = %{version}
Requires:   cvs 
Requires:   python-svn 
Requires:   bzrtools 
Requires:   git

%files -f transifex.lst
%defattr(-,root,root,-)
%doc LICENSE README 
%doc README.urpmi
%dir %{confdir}
%config(noreplace) %{confdir}/10-base.conf
%config(noreplace) %{confdir}/20-engines.conf
%config(noreplace) %{confdir}/30-site.conf
%config(noreplace) %{confdir}/40-apps.conf
%config(noreplace) %{confdir}/50-project.conf
%config(noreplace) %{confdir}/60-file-checks.conf
%config(noreplace) %{confdir}/70-translation.conf
%config(noreplace) %{confdir}/80-storage.conf
%config(noreplace) %{confdir}/89-addons.conf
%config(noreplace) %{confdir}/95-methods.conf
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/logs
%{_datadir}/%{name}/logs/transifex.log
%{_datadir}/%{name}/__init__.py
%{_datadir}/%{name}/manage.py
%{_datadir}/%{name}/settings.py
%{_datadir}/%{name}/urls.py
%{_datadir}/%{name}/views.py
%{_datadir}/%{name}/actionlog
%{_datadir}/%{name}/languages
%dir %{_datadir}/%{name}/locale
%{_datadir}/%{name}/locale/LINGUAS
%{_datadir}/%{name}/projects
%{_datadir}/%{name}/releases
%{_datadir}/%{name}/simpleauth
%{_datadir}/%{name}/site_media
%{_datadir}/%{name}/templates
%{_datadir}/%{name}/txcommon
%{_datadir}/%{name}/txpermissions
%dir %{_localstatedir}/lib/%{name}
%dir %{_localstatedir}/lib/%{name}/scratchdir
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/hg
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/tar
%{_datadir}/%{name}/addons/
%{_datadir}/%{name}/api/
%{_datadir}/%{name}/media/
%{_datadir}/%{name}/resources/
%{_datadir}/%{name}/storage/
%{_datadir}/%{name}/teams/

#--------------------------------------------------------------------


%description extras
This package adds extra options to Transifex.

  * cvs support
  * svn support
  * bzr support
  * git support

%files extras
%defattr(-,root,root,-)
%doc LICENSE README
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/cvs
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/svn
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/bzr
%dir %{_localstatedir}/lib/%{name}/scratchdir/sources/git

#--------------------------------------------------------------------

%prep
%setup -q
sed -e 's!share/locale!.*/locale!' /usr/lib/rpm/find-lang.sh > my-find-lang.sh

%build
cd transifex
rm -rf .hg* build-tools
python manage.py txcreatedirs
python manage.py txcompilemessages   # Create message catalogs for i18n

%install
rm -rf $RPM_BUILD_ROOT
cd transifex
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}

find -mindepth 1 -maxdepth 1 -type d \( \( -name .hg -o \
           -name build-tools -o -name docs -o -name settings \) -prune -o \
               -print \) | xargs cp -a -t $RPM_BUILD_ROOT/%{_datadir}/%{name}
               cp -a *.py $RPM_BUILD_ROOT%{_datadir}/%{name}

find $RPM_BUILD_ROOT%{_datadir}/%{name}/locale -name \*.po -exec rm {} +

for vcs in cvs svn bzr hg git tar
do
    mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}/scratchdir/sources/"$vcs"
done

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}

install -d -m 0755 $RPM_BUILD_ROOT/%{confdir}

cp -a settings/*.conf $RPM_BUILD_ROOT/%{confdir}

sed -i -e 's!^\(LOG_PATH = \).*$!\1"%{_localstatedir}/log/%{name}"!' \
    $RPM_BUILD_ROOT/%{confdir}/10-base.conf

sed -e 's!\[\[confpath\]\]!%{confdir}!' %{SOURCE1} > \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/settings.py

cd ..

sh my-find-lang.sh $RPM_BUILD_ROOT django transifex.lst

cat > README.urpmi <<EOF
To finish the initialization of transifex you will need to go on %{_datadir}/%{name}
./manage.py txcreatedirs
./manage.py syncdb --noinput
./manage.py migrate

to start the transifex server, you will have to use ./manage.py runserver 8088

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
if grep -q '\[\[SECRETKEY\]\]' %{confdir}/10-base.conf
then
    key=$(python << EOF
import random
print ''.join(chr(random.randint(35, 126)) for x in xrange(40)).replace('&',
    '\&')
EOF
)
    sed -i -e "s!\[\[SECRETKEY\]\]!$key!" \
        %{confdir}/10-base.conf
fi
