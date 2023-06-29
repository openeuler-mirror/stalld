Name:		stalld
Version:	1.16
Release:	2
Summary:	Daemon that finds starving tasks and gives them a temporary boost

License:	GPLv2
URL:		https://gitlab.com/rt-linux-tools/%{name}
Source0:	https://gitlab.com/rt-linux-tools/%{name}/-/archive/v%{version}/%{name}-%{version}.tar.bz2
patch0:     fix-clang.patch
patch1:     add-riscv-support.patch
BuildRequires:	glibc-devel
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	systemd

Requires:	systemd

%description
The stalld program monitors the set of system threads,
looking for threads that are ready-to-run but have not
been given processor time for some threshold period.
When a starving thread is found, it is given a temporary
boost using the SCHED_DEADLINE policy. The default is to
allow 10 microseconds of runtime for 1 second of clock time.

%prep
%autosetup  -n %{name}-%{version} -p1

%build
%make_build CFLAGS="%{optflags} %{build_cflags} -DVERSION="\\\"%{version}\\\"""  LDFLAGS="%{build_ldflags}"

%install
%make_install DOCDIR=%{_docdir} MANDIR=%{_mandir} BINDIR=%{_bindir} DATADIR=%{_datadir} VERSION=%{version}
%make_install -C redhat UNITDIR=%{_unitdir}

%files
%{_bindir}/%{name}
%{_bindir}/throttlectl
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/stalld
%doc %{_docdir}/README.md
%doc %{_mandir}/man8/stalld.8*
%license gpl-2.0.txt

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
* Mon Jun 19 2023 zhangxiang <zhangxiang@iscas.ac.cn> - 1.16-2
- Fix clang build error & add riscv support

* Mon Nov 07 2022 duyiwei <duyiwei@kylinos.cn> - 1.16-1
- upgrade version to 1.16

* Tue Jun 7 2022 duyiwei <duyiwei@kylinos.cn> - 1.15-1
- upgrade to 1.15

* Mon Jan 24 2022 duyiwei <duyiwei@kylinos.cn> - 1.14.1-1
- Package init
