# Feature 002 Release Validation: Local npm Dogfood

## Target and environment

- Repository: `<authorized-checkout>/medicare_monthly_enrollment_dashboard`
- Date: 2026-10-08
- Host: macOS 25.3.0, arm64
- Python: 3.11.0
- Libyears revision: `a053123`
- `package-lock.json` version: 3
- Target repository working tree: clean after the scan (baseline status was not recorded before it)

The scan used only the root `package.json`, root `package-lock.json`, and
public npm registry metadata. The root manifest yielded 10 in-scope production
dependencies, and all 10 had corresponding root lock entries. No unsupported
dependency source forms were found.

## Commands and registry outcome

Both required CLI modes were run:

```text
python3 -B -m libyears <authorized-checkout>/medicare_monthly_enrollment_dashboard --json
python3 -B -m libyears <authorized-checkout>/medicare_monthly_enrollment_dashboard
```

The first sandboxed attempt could not reach the registry and reported
`registry_error` for every dependency. Repeating both commands with approved
network access reached the public npm registry successfully. These initial
transport errors were environmental and did not persist in the network-enabled
validation.

No npm or Node command, dependency installation, resolver, or target repository
code was run. The target repository was not modified.

## Results

- Discovered: 10
- Measured: 10
- Coverage: 100%
- Total: 15.56462144602251 libyears
- Mean: 1.556462144602251 libyears
- Median: 1.8123617210434255 libyears
- Maximum: 2.740530464420615 libyears
- Unmeasurable: none

| Package | Used | Latest stable | Libyears |
|---|---:|---:|---:|
| `@11ty/eleventy-img` | 3.1.8 | 7.0.0 | 2.740530464420615 |
| `@uswds/uswds` | 3.9.0 | 3.14.0 | 1.869529751280199 |
| `autoprefixer` | 10.4.20 | 10.6.1 | 2.1182534288095423 |
| `d3` | 7.9.0 | 7.9.0 | 0.0 |
| `esbuild` | 0.24.2 | 0.28.2 | 1.631993270495855 |
| `esbuild-sass-plugin` | 3.3.1 | 3.7.0 | 1.755193690806652 |
| `luxon` | 2.5.2 | 3.7.2 | 2.6682156900081124 |
| `markdown-it-footnote` | 3.0.3 | 4.0.0 | 2.5455566876758686 |
| `simple-statistics` | 7.9.3 | 7.12.1 | 0.23534846252566735 |
| `topojson-client` | 3.1.0 | 3.1.0 | 0.0 |

Every measured dependency reported `version_source: package_lock` in JSON.
The human and JSON outputs agreed on 10/10 coverage and the aggregate values
(with the human report rounded to two decimal places). `d3` and
`topojson-client` were already at their latest stable release and measured
exactly 0.0 libyears.

## Spec and plan review

The observed behavior matched Feature 002's root production dependency scope,
supported v3 lock evidence, public registry source, and aggregate/output
requirements. No product discrepancy against `spec.md` or `plan.md` was found.
The sandbox-only transport failures are recorded above as an environment
limitation; the approved network-enabled run completed successfully.

T015 acceptance criteria are satisfied.
