%define		plugin	check_megaraid_sas
Summary:	Nagios plugin to check the state of disk and logical drives attached to LSI megaraid SAS controllers
Name:		nagios-plugin-%{plugin}
# revision from download page
Version:	12
Release:	5
License:	GPL v2
Group:		Networking
# http://exchange.nagios.org/components/com_mtree/attachment.php?link_id=680&cf_id=24
Source0:	check_megaraid_sas
Patch0:		bbu.patch
Patch1:		check_megaraid_sas-size.patch
Patch2:		check_megaraid_sas-JBOD.patch
URL:		http://exchange.nagios.org/directory/Plugins/Hardware/Storage-Systems/RAID-Controllers/check_megaraid_sas/details
Requires:	megacli-sas
Requires:	nagios-core
Requires:	nagios-plugins-libs
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		_sysconfdir	/etc/nagios/plugins

%description
A plugin to check the health and status of disk and logical drives
attached to LSI megaraid SAS controllers. This plugin calls LSI's
MegaCli utility to determine the health of disks and logical drive
units attached to Megraid SAS controllers. It has been tested by the
author on Dell PERC 5 & 6 controllers, but should work well with any
controller supported by the MegaCli tool.

%prep
%setup -qcT

install %{SOURCE0} %{plugin}
%{__sed} -i -e 's#/usr/sbin/MegaCli#/sbin/MegaCli#g' %{plugin}

%patch -P0 -p0
%patch -P1 -p1
%patch -P2 -p1

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin}
}

define service {
	use                     generic-service
	name                    megaraid_sas
	service_description     megaraid_sas
	register                0

	normal_check_interval   15
	notification_interval   300

	check_command           check_megaraid_sas
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}

install %{plugin} $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
