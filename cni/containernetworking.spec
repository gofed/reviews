# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 1
# Run tests in check section
# Some tests needs additional configuration, e.g. run as a root
%global with_check 0
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         containernetworking
%global repo            cni
# https://github.com/containernetworking/cni
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          0799f5732f2a11b329d9e3d51b9c8f2e3759f2ff
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           containernetworking
Version:        0.5.1
Release:        1%{?dist}
Summary:        Libraries for writing CNI plugin
# Detected licences
# - *No copyright* Apache (v2.0) GENERATED FILE at 'LICENSE'
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# plugins/main/ipvlan/ipvlan.go
BuildRequires: golang(github.com/vishvananda/netlink)

# plugins/main/bridge/bridge.go
BuildRequires: golang(github.com/vishvananda/netlink)

# plugins/ipam/dhcp/daemon.go
BuildRequires: golang(github.com/coreos/go-systemd/activation)

# plugins/main/ptp/ptp.go
BuildRequires: golang(github.com/vishvananda/netlink)

# plugins/main/macvlan/macvlan.go
BuildRequires: golang(github.com/vishvananda/netlink)

# plugins/main/loopback/loopback.go
BuildRequires: golang(github.com/vishvananda/netlink)

# plugins/ipam/dhcp/options.go
BuildRequires: golang(github.com/d2g/dhcp4)

# plugins/ipam/dhcp/lease.go
BuildRequires: golang(github.com/d2g/dhcp4)
BuildRequires: golang(github.com/d2g/dhcp4client)
BuildRequires: golang(github.com/vishvananda/netlink)

# Remaining dependencies not included in main packages
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(github.com/coreos/go-iptables/iptables)
%endif

BuildRequires: go-md2man
BuildRequires: go-bindata

# packaged by upstream under kubernetes-cni
Provides: kubernetes-cni

%description
The CNI (Container Network Interface) project consists of a specification
and libraries for writing plugins to configure network interfaces in Linux
containers, along with a number of supported plugins. CNI concerns itself
only with network connectivity of containers and removing allocated resources
when the container is deleted.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/coreos/go-iptables/iptables)
BuildRequires: golang(github.com/vishvananda/netlink)
BuildRequires: golang(golang.org/x/sys/unix)
%endif

Requires:      golang(github.com/coreos/go-iptables/iptables)
Requires:      golang(github.com/vishvananda/netlink)
Requires:      golang(golang.org/x/sys/unix)

Provides:      golang(%{import_path}/libcni) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/invoke) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/invoke/fakes) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/ip) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/ipam) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/ns) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/skel) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/types) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/types/020) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/types/current) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/utils) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/utils/hwaddr) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/utils/sysctl) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/version) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/version/legacy_examples) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/version/testhelpers) = %{version}-%{release}
Provides:      golang(%{import_path}/plugins/ipam/host-local/backend) = %{version}-%{release}
Provides:      golang(%{import_path}/plugins/ipam/host-local/backend/allocator) = %{version}-%{release}
Provides:      golang(%{import_path}/plugins/ipam/host-local/backend/disk) = %{version}-%{release}
Provides:      golang(%{import_path}/plugins/ipam/host-local/backend/testing) = %{version}-%{release}
Provides:      golang(%{import_path}/plugins/test/noop/debug) = %{version}-%{release}

%description devel
This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/d2g/dhcp4)
BuildRequires: golang(github.com/onsi/ginkgo)
BuildRequires: golang(github.com/onsi/ginkgo/config)
BuildRequires: golang(github.com/onsi/ginkgo/extensions/table)
BuildRequires: golang(github.com/onsi/gomega)
BuildRequires: golang(github.com/onsi/gomega/gbytes)
BuildRequires: golang(github.com/onsi/gomega/gexec)
BuildRequires: golang(github.com/vishvananda/netlink/nl)
%endif

Requires:      golang(github.com/d2g/dhcp4)
Requires:      golang(github.com/onsi/ginkgo)
Requires:      golang(github.com/onsi/ginkgo/config)
Requires:      golang(github.com/onsi/ginkgo/extensions/table)
Requires:      golang(github.com/onsi/gomega)
Requires:      golang(github.com/onsi/gomega/gbytes)
Requires:      golang(github.com/onsi/gomega/gexec)
Requires:      golang(github.com/vishvananda/netlink/nl)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
# No dependency directories so far
export GOPATH=$(pwd):%{gopath}
%endif

%gobuild -o bin/cnitool %{import_path}/cnitool
%gobuild -o bin/plugins/dhcp %{import_path}/plugins/ipam/dhcp
%gobuild -o bin/plugins/host-local %{import_path}/plugins/ipam/host-local
%gobuild -o bin/plugins/bridge %{import_path}/plugins/main/bridge
%gobuild -o bin/plugins/ipvlan %{import_path}/plugins/main/ipvlan
%gobuild -o bin/plugins/loopback %{import_path}/plugins/main/loopback
%gobuild -o bin/plugins/macvlan %{import_path}/plugins/main/macvlan
%gobuild -o bin/plugins/ptp %{import_path}/plugins/main/ptp
%gobuild -o bin/plugins/flannel %{import_path}/plugins/meta/flannel
%gobuild -o bin/plugins/tuning %{import_path}/plugins/meta/tuning
%gobuild -o bin/plugins/noop %{import_path}/plugins/test/noop

%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/cnitool %{buildroot}%{_bindir}

install -d -p %{buildroot}%{_libexecdir}/cni/
install -p -m 755 -t %{buildroot}%{_libexecdir}/cni/ bin/plugins/*

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/libcni
%gotest %{import_path}/pkg/invoke
%gotest %{import_path}/pkg/ip
%gotest %{import_path}/pkg/ipam
%gotest %{import_path}/pkg/ns
%gotest %{import_path}/pkg/skel
%gotest %{import_path}/pkg/types
%gotest %{import_path}/pkg/types/020
%gotest %{import_path}/pkg/types/current
%gotest %{import_path}/pkg/utils
%gotest %{import_path}/pkg/utils/hwaddr
%gotest %{import_path}/pkg/version
%gotest %{import_path}/pkg/version/legacy_examples
%gotest %{import_path}/pkg/version/testhelpers
%gotest %{import_path}/plugins/ipam/dhcp
%gotest %{import_path}/plugins/ipam/host-local
%gotest %{import_path}/plugins/ipam/host-local/backend/allocator
%gotest %{import_path}/plugins/main/bridge
%gotest %{import_path}/plugins/main/ipvlan
%gotest %{import_path}/plugins/main/loopback
%gotest %{import_path}/plugins/main/macvlan
%gotest %{import_path}/plugins/main/ptp
%gotest %{import_path}/plugins/meta/flannel
%gotest %{import_path}/plugins/test/noop
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%{_bindir}/cnitool
%{_libexecdir}/cni/*

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md CONVENTIONS.md SPEC.md CONTRIBUTING.md ROADMAP.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md CONVENTIONS.md SPEC.md CONTRIBUTING.md ROADMAP.md
%endif

%changelog
* Tue May 16 2017 Jan Chaloupka <jchaloup@redhat.com> - 0-0.1.git0799f57
- First package for Fedora

