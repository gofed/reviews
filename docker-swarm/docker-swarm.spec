%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

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
%global project         docker
%global repo            swarm
# https://github.com/docker/swarm
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          f947993ec0bc52378afee388bda8d63196ee4bbd
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           docker-swarm
Version:        1.1.2
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Docker-native clustering system
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# main.go
BuildRequires: golang(github.com/docker/docker/pkg/discovery/file)
BuildRequires: golang(github.com/docker/docker/pkg/discovery/kv)
BuildRequires: golang(github.com/docker/docker/pkg/discovery/nodes)

# binaries are built from devel subpackage
BuildRequires: %{name}-devel = %{version}-%{release}
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/codegangsta/cli)
BuildRequires: golang(github.com/docker/docker/pkg/discovery)
BuildRequires: golang(github.com/docker/docker/pkg/discovery/kv)
BuildRequires: golang(github.com/docker/docker/pkg/ioutils)
BuildRequires: golang(github.com/docker/docker/pkg/parsers/kernel)
BuildRequires: golang(github.com/docker/docker/pkg/stringid)
BuildRequires: golang(github.com/docker/docker/pkg/version)
BuildRequires: golang(github.com/docker/engine-api/types)
BuildRequires: golang(github.com/docker/engine-api/types/filters)
BuildRequires: golang(github.com/docker/go-units)
BuildRequires: golang(github.com/docker/leadership)
BuildRequires: golang(github.com/gogo/protobuf/proto)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/mesos/mesos-go/mesosproto)
BuildRequires: golang(github.com/mesos/mesos-go/mesosutil)
BuildRequires: golang(github.com/mesos/mesos-go/scheduler)
BuildRequires: golang(github.com/samalba/dockerclient)
BuildRequires: golang(github.com/samalba/dockerclient/nopclient)
BuildRequires: golang(github.com/skarademir/naturalsort)
BuildRequires: golang(golang.org/x/sys/unix)
%endif

Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/codegangsta/cli)
Requires:      golang(github.com/docker/docker/pkg/discovery)
Requires:      golang(github.com/docker/docker/pkg/discovery/kv)
Requires:      golang(github.com/docker/docker/pkg/ioutils)
Requires:      golang(github.com/docker/docker/pkg/parsers/kernel)
Requires:      golang(github.com/docker/docker/pkg/stringid)
Requires:      golang(github.com/docker/docker/pkg/version)
Requires:      golang(github.com/docker/engine-api/types)
Requires:      golang(github.com/docker/engine-api/types/filters)
Requires:      golang(github.com/docker/go-units)
Requires:      golang(github.com/docker/leadership)
Requires:      golang(github.com/gogo/protobuf/proto)
Requires:      golang(github.com/gorilla/mux)
Requires:      golang(github.com/mesos/mesos-go/mesosproto)
Requires:      golang(github.com/mesos/mesos-go/mesosutil)
Requires:      golang(github.com/mesos/mesos-go/scheduler)
Requires:      golang(github.com/samalba/dockerclient)
Requires:      golang(github.com/samalba/dockerclient/nopclient)
Requires:      golang(github.com/skarademir/naturalsort)
Requires:      golang(golang.org/x/sys/unix)

Provides:      golang(%{import_path}/api) = %{version}-%{release}
Provides:      golang(%{import_path}/cli) = %{version}-%{release}
Provides:      golang(%{import_path}/cluster) = %{version}-%{release}
Provides:      golang(%{import_path}/cluster/mesos) = %{version}-%{release}
Provides:      golang(%{import_path}/cluster/mesos/task) = %{version}-%{release}
Provides:      golang(%{import_path}/cluster/swarm) = %{version}-%{release}
Provides:      golang(%{import_path}/discovery/token) = %{version}-%{release}
Provides:      golang(%{import_path}/experimental) = %{version}-%{release}
Provides:      golang(%{import_path}/scheduler) = %{version}-%{release}
Provides:      golang(%{import_path}/scheduler/filter) = %{version}-%{release}
Provides:      golang(%{import_path}/scheduler/node) = %{version}-%{release}
Provides:      golang(%{import_path}/scheduler/strategy) = %{version}-%{release}
Provides:      golang(%{import_path}/version) = %{version}-%{release}

%description devel
%{summary}

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
BuildRequires: golang(github.com/samalba/dockerclient/mockclient)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/stretchr/testify/mock)
%endif

Requires:      golang(github.com/samalba/dockerclient/mockclient)
Requires:      golang(github.com/stretchr/testify/assert)
Requires:      golang(github.com/stretchr/testify/mock)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/github.com/docker
ln -s ../../../ src/github.com/docker/swarm

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

#%gobuild -o bin/ %{import_path}/

%install
install -d -p %{buildroot}%{_bindir}
#install -p -m 0755 bin/ %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
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
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/api
%gotest %{import_path}/cli
%gotest %{import_path}/cluster
%gotest %{import_path}/cluster/mesos
%gotest %{import_path}/cluster/mesos/task
%gotest %{import_path}/cluster/swarm
%gotest %{import_path}/discovery/token
%gotest %{import_path}/scheduler
%gotest %{import_path}/scheduler/filter
%gotest %{import_path}/scheduler/strategy
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE.code
%doc ROADMAP.md CHANGELOG.md CONTRIBUTING.md RELEASE-CHECKLIST.md README.md
#%{_bindir}/

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE.code
%doc ROADMAP.md CHANGELOG.md CONTRIBUTING.md RELEASE-CHECKLIST.md README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE.code
%doc ROADMAP.md CHANGELOG.md CONTRIBUTING.md RELEASE-CHECKLIST.md README.md
%endif

%changelog
* Thu Feb 25 2016 jchaloup <jchaloup@redhat.com> - 0-0.1.gitf947993
- First package for Fedora
  resolves: #1211517
