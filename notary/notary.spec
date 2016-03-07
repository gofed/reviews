%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
#FIXME? global with_bundled 0
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         docker
%global repo            notary
# https://github.com/docker/notary
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          8a5c8c04955ba32f7e1fcd66571c6a8988e251b0
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           notary
Version:        0.1
Release:        2.20160219git%{shortcommit}%{?dist}
Summary:        A server and client for running and interacting with trusted collections
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        notary-server.service
Source2:        notary-signer.service
# Edits example config files to make it easier to start with Notary, but the
# edits also (intentionally) prevent running with unmodified configuration;
# OTOH upstream wants the unmodified configuration to work in docker-compose
# setups. So, not sent upstream.
Patch0:         notary-config.patch
Patch1:         patch-notary-code-to-use-newer-commits-of-dependenci.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  libtool-ltdl-devel systemd

%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/Sirupsen/logrus/hooks/bugsnag)
BuildRequires: golang(github.com/agl/ed25519)
BuildRequires: golang(github.com/bugsnag/bugsnag-go)
BuildRequires: golang(github.com/docker/distribution/context)
BuildRequires: golang(github.com/docker/distribution/health)
BuildRequires: golang(github.com/docker/distribution/registry/api/errcode)
BuildRequires: golang(github.com/docker/distribution/registry/auth)
BuildRequires: golang(github.com/docker/distribution/registry/auth/htpasswd)
BuildRequires: golang(github.com/docker/distribution/registry/auth/token)
BuildRequires: golang(github.com/docker/distribution/registry/client/auth)
BuildRequires: golang(github.com/docker/distribution/registry/client/transport)
BuildRequires: golang(github.com/docker/distribution/uuid)
BuildRequires: golang(github.com/docker/docker/pkg/term)
BuildRequires: golang(github.com/docker/go/canonical/json)
BuildRequires: golang(github.com/docker/go-connections/tlsconfig)
BuildRequires: golang(github.com/dvsekhvalnov/jose2go)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/google/gofuzz)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/jinzhu/gorm)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/miekg/pkcs11)
BuildRequires: golang(github.com/mitchellh/go-homedir)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(golang.org/x/crypto/nacl/secretbox)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
%endif

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
%{summary}

%post
%systemd_post notary-server.service notary-signer.service

%preun
%systemd_preun notary-server.service notary-signer.service

%postun
%systemd_postun_with_restart notary-server.service notary-signer.service

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/Sirupsen/logrus/hooks/bugsnag)
BuildRequires: golang(github.com/agl/ed25519)
BuildRequires: golang(github.com/bugsnag/bugsnag-go)
BuildRequires: golang(github.com/docker/distribution/context)
BuildRequires: golang(github.com/docker/distribution/health)
BuildRequires: golang(github.com/docker/distribution/registry/api/errcode)
BuildRequires: golang(github.com/docker/distribution/registry/auth)
BuildRequires: golang(github.com/docker/distribution/uuid)
BuildRequires: golang(github.com/docker/docker/pkg/term)
BuildRequires: golang(github.com/docker/go/canonical/json)
BuildRequires: golang(github.com/docker/go-connections/tlsconfig)
BuildRequires: golang(github.com/dvsekhvalnov/jose2go)
BuildRequires: golang(github.com/go-sql-driver/mysql)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/google/gofuzz)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/jinzhu/gorm)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/miekg/pkcs11)
BuildRequires: golang(github.com/prometheus/client_golang/prometheus)
BuildRequires: golang(github.com/spf13/viper)
BuildRequires: golang(golang.org/x/crypto/nacl/secretbox)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/credentials)
%endif

Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/Sirupsen/logrus/hooks/bugsnag)
Requires:      golang(github.com/agl/ed25519)
Requires:      golang(github.com/bugsnag/bugsnag-go)
Requires:      golang(github.com/docker/distribution/context)
Requires:      golang(github.com/docker/distribution/health)
Requires:      golang(github.com/docker/distribution/registry/api/errcode)
Requires:      golang(github.com/docker/distribution/registry/auth)
Requires:      golang(github.com/docker/distribution/uuid)
Requires:      golang(github.com/docker/docker/pkg/term)
Requires:      golang(github.com/docker/go/canonical/json)
Requires:      golang(github.com/docker/go-connections/tlsconfig)
Requires:      golang(github.com/dvsekhvalnov/jose2go)
Requires:      golang(github.com/go-sql-driver/mysql)
Requires:      golang(github.com/golang/protobuf/proto)
Requires:      golang(github.com/google/gofuzz)
Requires:      golang(github.com/gorilla/mux)
Requires:      golang(github.com/jinzhu/gorm)
Requires:      golang(github.com/mattn/go-sqlite3)
Requires:      golang(github.com/miekg/pkcs11)
Requires:      golang(github.com/prometheus/client_golang/prometheus)
Requires:      golang(github.com/spf13/viper)
Requires:      golang(golang.org/x/crypto/nacl/secretbox)
Requires:      golang(golang.org/x/crypto/scrypt)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(google.golang.org/grpc)
Requires:      golang(google.golang.org/grpc/codes)
Requires:      golang(google.golang.org/grpc/credentials)

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/certs) = %{version}-%{release}
Provides:      golang(%{import_path}/client) = %{version}-%{release}
Provides:      golang(%{import_path}/client/changelist) = %{version}-%{release}
Provides:      golang(%{import_path}/cryptoservice) = %{version}-%{release}
Provides:      golang(%{import_path}/passphrase) = %{version}-%{release}
Provides:      golang(%{import_path}/proto) = %{version}-%{release}
Provides:      golang(%{import_path}/server) = %{version}-%{release}
Provides:      golang(%{import_path}/server/errors) = %{version}-%{release}
Provides:      golang(%{import_path}/server/handlers) = %{version}-%{release}
Provides:      golang(%{import_path}/server/snapshot) = %{version}-%{release}
Provides:      golang(%{import_path}/server/storage) = %{version}-%{release}
Provides:      golang(%{import_path}/server/timestamp) = %{version}-%{release}
Provides:      golang(%{import_path}/signer) = %{version}-%{release}
Provides:      golang(%{import_path}/signer/api) = %{version}-%{release}
Provides:      golang(%{import_path}/signer/client) = %{version}-%{release}
Provides:      golang(%{import_path}/signer/keydbstore) = %{version}-%{release}
Provides:      golang(%{import_path}/signer/keys) = %{version}-%{release}
Provides:      golang(%{import_path}/trustmanager) = %{version}-%{release}
Provides:      golang(%{import_path}/trustmanager/yubikey) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/client) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/data) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/encrypted) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/signed) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/store) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/testutils) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/utils) = %{version}-%{release}
Provides:      golang(%{import_path}/tuf/validation) = %{version}-%{release}
Provides:      golang(%{import_path}/utils) = %{version}-%{release}
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
BuildArch:       noarch

%if 0%{?with_check}
BuildRequires: golang(github.com/docker/distribution/registry/auth/silly)
BuildRequires: golang(github.com/spf13/cobra)
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/stretchr/testify/require)
%endif

Requires: golang(github.com/docker/distribution/registry/auth/silly)
Requires: golang(github.com/spf13/cobra)
Requires: golang(github.com/stretchr/testify/assert)
Requires: golang(github.com/stretchr/testify/require)

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}
%patch0 -p1 -b .config
%patch1 -p1

%build
mkdir -p src/$(dirname %{import_path})
ln -s ../../.. src/%{import_path}
%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%{!?gobuild:%global gobuild go build -compiler gc -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x}

export LDFLAGS="-w -X github.com/docker/notary/version.GitCommit %{commit} -X github.com/docker/notary/version.NotaryVersion $(cat NOTARY_VERSION)"
%gobuild -tags pkcs11 -o bin/notary-server ./cmd/notary-server
%gobuild -tags pkcs11 -o bin/notary-signer ./cmd/notary-signer
%gobuild -tags pkcs11 -o bin/notary ./cmd/notary


%install
install -d %{buildroot}%{_bindir} %{buildroot}%{_sysconfdir}/notary
install -p -m 755 bin/notary{,-server,-signer} %{buildroot}%{_bindir}
install -p -m 600 fixtures/server-config.json %{buildroot}%{_sysconfdir}/notary
install -p -m 600 fixtures/signer-config.json %{buildroot}%{_sysconfdir}/notary

install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_unitdir}

chmod a-x docs/opensslCertGen.sh migrations/migrate.sh

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go" | grep -v "./Godeps") ; do
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
for file in $(find . -iname "*_test.go" | grep -v "./Godeps"); do
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
%if 0%{?with_check} && 0%{?with_unit_test}
%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gotest -tags pkcs11 ./...
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%exclude %{gopath}/src/%{import_path}/cmd
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%exclude %{gopath}/src/%{import_path}/cmd
%endif

%files
%license LICENSE
%doc CONTRIBUTING.md CONTRIBUTORS MAINTAINERS README.md ROADMAP.md
%doc Godeps/Godeps.json
%doc docker-compose.yml
%doc migrations
%doc docs/[^R]*.md docs/opensslCertGen.sh
%{_bindir}/notary
%{_bindir}/notary-server
%{_bindir}/notary-signer
%dir %{_sysconfdir}/notary
%config(noreplace) %{_sysconfdir}/notary/server-config.json
%config(noreplace) %{_sysconfdir}/notary/signer-config.json
%{_unitdir}/notary-server.service
%{_unitdir}/notary-signer.service

%changelog
* Wed Feb 24 2016 Miloslav Trmač <mitr@redhat.com> - 0.1-2.20160219git8a5c8c0
- Added !with_bundled BuildRequires: golang(github.com/spf13/cobra)
- Moved test-only BuildRequires: and Requires: to the notary-unit-test-devel
  with_check section
- Dropped no longer valid Provides: golang(github.com/docker/notary/signer/keys)
- Dropped the cmd/ source subtree from notary-devel and notary-unit-test-devel

* Mon Feb 22 2016 Miloslav Trmač <mitr@redhat.com> - 0.1-1.20160219git8a5c8c0
- First package for Fedora
