%define confdir %{python_sitelib}/%{name}/settings

Name:       transifex
Version:    1.2.1
Release:    %mkrel 3
Summary:    A system for distributed translation submissions

Group:      Networking/WWW
License:    GPLv2
URL:        http://transifex.org
Source0:    transifex-%version.tar.gz
Source1:    django-settings.py.in
BuildArch:  noarch

BuildRequires:  python-sphinx 
BuildRequires:  gettext 
BuildRequires:  python-markdown
BuildRequires:  python-django  >= 1.2.3
BuildRequires:  python-django-contact-form 
BuildRequires:  python-django-pagination 
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
BuildRequires:	python-django-appconf
BuildRequires:	python-django-compressor
BuildRequires:	python-django-tagging
BuildRequires:	python-django-haystack
BuildRequires:	python-django-tagging-autocomplete
BuildRequires:	python-django-social-auth
BuildRequires:	python-django-easy-thumbnails
BuildRequires:	python-django-guardian
BuildRequires:	python-django-userena
BuildRequires:	python-openid
BuildRequires:	python-setuptools
BuildRequires:	python-oauth2
BuildRequires:	python-magic
BuildRequires:	python-polib
BuildRequires:	python-redis

Requires:   mercurial >= 1.3 
Requires:   python-urlgrabber 
Requires:   intltool >= 0.37.1
Requires:   python-markdown 
Requires:   python-pygments 
Requires:   python-polib >= 0.4.2
Requires:   python-django >= 1.2.0
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
Requires:   python-magic
Requires:   python-django-filter

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

%files
%{python_sitelib}/*
#--------------------------------------------------------------------

%prep
%setup -q -n indifex-transifex-stable-1af2e28982b8
sed -e 's!share/locale!.*/locale!' /usr/lib/rpm/find-lang.sh > my-find-lang.sh

%build
%{__python} setup.py build
#cd transifex
#rm -rf .hg* build-tools
#rm -r vcs/tests
#python manage.py syncdb --noinput    # Setup DB tables
#python manage.py migrate             # Setup more DB tables
#python manage.py txcreatelanguages   # Create a standard set of languages
#python manage.py txcompilemessages   # Create message catalogs for i18n

%install
#transifex now installs as a normal django application
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}
#The next part of the install process is removed 
#cd transifex
#mkdir -p %{buildroot}%{_datadir}/%{name}
#find -mindepth 1 -maxdepth 1 -type d \( \( -name .hg -o \
#    -name build-tools -o -name docs -o -name settings \) -prune -o \
#    -print \) | xargs cp -a -t %{buildroot}/%{_datadir}/%{name}
#cp -a *.py %{buildroot}%{_datadir}/%{name}
#find %{buildroot}%{_datadir}/%{name}/locale -name \*.po -exec rm {} +

#for vcs in cvs svn bzr hg git tar
#do
#    mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}/scratchdir/sources/"$vcs"
#done

mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

#install -d -m 0755 %{buildroot}/%{confdir}

#cp -a settings/*.conf %{buildroot}/%{confdir}

sed -i -e 's!^\(LOG_PATH = \).*$!\1"%{_localstatedir}/log/%{name}"!' \
    %{buildroot}/%{confdir}/10-base.conf

#sed -e 's!\[\[confpath\]\]!%{confdir}!' %{SOURCE1} > \
#    %{buildroot}%{_datadir}/%{name}/settings.py

#cd ..

#sh my-find-lang.sh %{buildroot} django transifex.lst

cat > README.urpmi <<EOF
To finish the initialization of transifex you will need to go on %{_datadir}/%{name}
./manage.py txcreatedirs
./manage.py txcreatenoticetypes
./manage.py syncdb --noinput
./manage.py migrate

to start the transifex server, you will have to use ./manage.py runserver 8088

EOF


%post
rm -rf %{_sysconfdir}/%{name}
ln -s %{python_sitelib}/%{name}/settings %{_sysconfdir}/%{name} 
# Check to see if the secret key for Django needs setting, and then set it
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
