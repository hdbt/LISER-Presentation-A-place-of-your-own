# Validation record — 7 September 2026

## Executed successfully

The complete `build.py` workflow was run from the separate replication-package directory on Windows, using Python 3.14, xlrd 2.0.2, Quarto 1.7.32 and Node 24.19.0. Exact runtime strings are recorded in `BUILD_REPORT.json`.

- Input snapshot and bundled wheel SHA-256 checks passed.
- ACT raw GeoJSON regenerated 100 commune display shapes (11,019 points).
- Shapes, label coordinates, view box, rent panel and CPI values exactly matched the pre-packaging presentation snapshot under canonical JSON hashing.
- Rental rates and CPI were regenerated from the XLS/CSV snapshots.
- 2025 baseline: 14 within-budget averages among 34 observed communes.
- Matched 2010–2025 baseline: 29 -> 11 among the same 29 communes.
- Eurostat 2025 figure and manually transcribed census/Schifflange arithmetic checks passed.
- Presentation HTML rendered successfully. The build no longer requires or exports the separately maintained speaker guide.
- Node DOM-stub checks passed for 14 slide states, calculations, control changes, reset, selection, zoom and absence of external asset dependencies.

## Not validated here

Docker CLI 29.2.0 was found, but the Docker Desktop Linux engine pipe was unavailable. The Docker image was **not built or run**. Its fixed Python/Node versions differ from the locally tested runtime and must pass the included checks when first built. The container's `RUN python build.py` makes validation part of image creation.

No fresh browser visual review was performed as part of packaging. Review the slides at the actual presentation resolution. The tests establish computation and control behaviour, not visual layout or the truth of every narrative statement.

The local test used the installed xlrd 2.0.2. A wheel of the same version is bundled and hash-locked for clean installation; a fresh virtual-environment installation was not separately exercised here.
