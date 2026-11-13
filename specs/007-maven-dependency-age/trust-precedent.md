# Maven explicit trust precedent — 007-0018

**Existing override sufficient; local trust input required.** This repository-only
investigation follows the [reviewed AB2D stop](positive-validation.md), starting at
`83bfffb`. AB2D remains selected. No candidate was reinspected, certificate discovered,
trust material supplied or live request made. No product defect is established and
no runtime, test, policy, endpoint or dependency-age behavior changed.

## Recovered precedent and its limits

[Shared TLS policy](../../SPEC.md#tls-trust-policy),
[operational documentation](../../ECOSYSTEMS.md#tls-and-enterprise-environments),
[registry implementation](../../libyears/registry.py) and tests establish Python/npm's
common mechanism. Explicit `--ca-bundle FILE` is authoritative and validated before
scanning. Otherwise Python/OpenSSL defaults, including standard CA environment
settings, apply. Only when defaults lack a usable CA source may a bounded set of
existing interpreter-associated pip-vendored CA files supply verified fallback.
Nothing is installed/downloaded and pip/certifi are not imported as dependencies.
Certificate and hostname verification stay enabled; trust failure does not select
an insecure context. Diagnostics classify failures rather than reproduce exceptions.

History locates this Python policy in `ee064f9`, extraction into shared transport in
`490b7a0`, and explicit npm/Python TLS verification tests in `70e2dd7`. The policy
addresses an interpreter with no usable default CA source; retained artifacts do not
establish a particular certificate identity or why an initial installation lacked
trust. The [npm validation](../002-npm-support/release-validation.md) separately
records sandbox registry failures followed by successful approved network access.
It does not establish a certificate-specific cause for those initial npm failures.

A related, stronger local-procedure precedent is explicitly recorded in
[RubyGems validation](../004-rubygems-support/release-validation.md#authorized-trust-boundary-resolution-and-resumed-attempt)
and its [review chronology](../004-rubygems-support/reviews.md#environmental-chronology-retained-for-t021).
That ecosystem reused the shared Python/npm transport. Human-supplied evidence
identified a destination-specific missing issuer trust problem, distinct from later
agent DNS failure. The human approved required trust anchors and a temporary combined
CA bundle with public roots, checked verified connectivity, and authorized the existing
explicit override. Certificate bytes were outside Git; system/Python trust configuration
was not changed. This is a human-established historical procedure, not current Maven
certificate evidence or transferable authority to export/search for any certificate.

Python/npm's transport loads its selected file directly in-process. It has no Maven-style
private worker copy. A private temporary bundle in validation is an operational
procedure, not automatic product trust construction. Shared verbose trust descriptions
can include an explicit path, so raw diagnostics must not be presumed sanitized for
sensitive operational capture. Existing records use placeholders and omit certificate
material/local topology; this investigation retains mechanisms, not identity details.

## Maven comparison and exact input shape

The [approved metadata contract](metadata-contract.md) and independently reviewed
[T008 transport](reviews.md#run007-0014--t008-supervised-metadata-transport) already
support the same **kind of explicit CA file**, through a deliberately different
trust-selection boundary:

1. CLI validates the explicit file using verified Python TLS loading and passes the
   option through mixed scanning to the Maven supervisor. No Java-specific flag or
   Python resolved snapshot is needed.
2. The supervisor accepts a readable regular, non-symlink file with stable identity
   and bytes, strictly greater than zero and at most **4 MiB**. It reads bounded bytes
   with no-follow/nonblocking open and identity checks before/after reading.
3. Only that explicit material is copied into private temporary worker storage,
   with staged file permissions `0600`. The installed isolated Python worker uses
   a private cwd and empty environment. The source machine path is not sent in the
   coordinate command protocol. Normal bounded cleanup removes staged storage;
   unreaped cleanup remains deferred and prevents further worker I/O.
4. The worker loads the staged file with `SSLContext(PROTOCOL_TLS_CLIENT)` and
   `load_verify_locations(cafile=...)`. Certificate and hostname verification must
   remain enabled before any connection. The override supplies the trust anchors;
   Maven does not automatically append defaults or discover an additional bundle.

The local input is therefore a human-approved **PEM CA certificate bundle**, containing
trust anchors sufficient to verify the permitted public HTTPS chain. It may be an
already approved public-root bundle; additional roots require human approval if
actually needed. No such need or certificate identity is inferred here. It is not a
private key, Java keystore, trust-store directory, environment variable or Maven
settings file. The source should be staged privately outside Git and kept stable
through the bounded rerun. No certificate contents need to be pasted into chat.

Use the existing ordinary interface only after that material and authority exist:

```text
python3 -m libyears PUBLIC_AB2D_PATH --ca-bundle APPROVED_CA_FILE
```

JSON and verbose forms retain that explicit option. Exact source paths belong only
in the private external engineering handoff; captured output must be inspected before
retention. Maven still ignores ambient CA/proxy/auth variables, pip fallback and
Maven/home configuration. Fixed public endpoint, admission, budgets, redirect refusal
and target immutability remain unchanged. Reusing shared automatic discovery inside
Maven would change its approved trust boundary; it is unnecessary for this input.
No implementation unification or new dependency is proposed.

## Verification, sensitivity and next gate

Existing tests cover explicit-bundle precedence and verified contexts for Python/npm,
CLI forwarding, Maven forwarding, compiled-versus-explicit trust, insecure-context
refusal, safe bounded staging, refusal of links/special/empty/oversized inputs, worker
isolation/readiness and cleanup. **53 focused existing tests PASS.** The external
runner replaces ambient default trust/pip discovery with injected empty verified
contexts and denies parent socket events. Individual trust tests retain their local
mocks; worker tests use synthetic bytes and installed no-request readiness. No machine
CA file or trust inventory was inspected. This proves deterministic mechanisms, not
that any real supplied bundle loads or verifies a current endpoint. No full regression
rerun is needed for this documentation-only investigation; no new test was added.

Sensitivity review must supplement GitLeaks before staging: exclude PEM/base64 bodies,
certificate fingerprints, distinguished names, internal organization/host identities,
private trust inventories, actual CA paths, home/user topology, environment values
and secret-bearing configuration. Neither original material nor derived certificate
identity is required as durable evidence. Source/code/test citations and artifact
checksums are provenance for repository artifacts, not certificate fingerprints.

The recurring environmental lesson was recovered from durable policy/code/tests and
historical operational records without the human retransmitting a solution. The
mechanism differs across transports; a shared explicit-input pattern is reusable,
while ambient selection, staging and historical endpoint causes are not identical.
No generalized harness or portability/resource claim follows.

007-0017's handoff is appended once with supplied final telemetry (reported976s,
credits_after148), retaining its AB2D fitness, zero GET/disclosure, preconnection TLS
failure, no-product-defect and no-fallback facts. Credits_before remains blank without
direct observation or explicit continuity; no derived credit delta. Current007-0018
gets an external44-key handoff. The lost007-0014 baton remains unreconstructed.

**Smallest next human action:** stage an approved PEM CA bundle meeting the file
shape above outside Git, provide its exact path through a private local engineering
handoff, and explicitly authorize reading/private staging for the bounded AB2D rerun.
No certificate identity, export, discovery or system trust change is requested.
Until that fact/material/authority arrives, do not rerun AB2D. A valid explicit input
still cannot promise catalogue acceptance, dates or positive ages; compare any later
result with the preserved007-0017 zero-connection baseline.
