# LISER presentation replication package

Snapshot refreshed on 8 September 2026 of Hamid Bulut's 12-slide presentation (9 main slides and 3 appendix slides), prepared for 9 September 2026. The original files remain outside this package. All computational data inputs are bundled; no live data API is called during rebuilding.

## View or edit

- Open `LISER_Combined.html` for the self-contained interactive slides.
- Edit `LISER_Combined.qmd` for prose. Keep the named map controls intact.
- CSS, navigation and map logic are in `quarto-assets/`.
- The source is Quarto with a custom HTML template, not Beamer or Reveal.js. Print from HTML for a static snapshot; interactive controls do not survive PDF export.

## Rebuild locally

Install Python 3.12 or newer, Quarto **1.7.32**, and Node.js (the container uses **22.14.0**). Quarto installation instructions: https://quarto.org/docs/download/tarball.html

From this package directory:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install --no-index --find-links=vendor --require-hashes -r requirements.lock
python build.py
```

If tools are not on PATH:

```powershell
python build.py --quarto 'C:/Program Files/RStudio/resources/app/bin/quarto/bin/quarto.exe' --node 'C:/path/to/node.exe'
```

The rebuild verifies input checksums, recreates geometry from ACT GeoJSON, recomputes rents and CPI from raw snapshots, checks results against the original presentation, renders the presentation, and exercises map controls with a Node DOM stub. It writes `BUILD_REPORT.json`. It does not perform browser visual testing.

To render prose changes without rebuilding data: `quarto render LISER_Combined.qmd`. To change data intentionally, update the provenance and checksum manifest and replace the expected-results reference only after independently reviewing the changed results.

## Docker

With Docker Desktop's Linux engine running:

```sh
docker build --platform linux/amd64 -t liser-replication:2026-09-09 .
```

Export rebuilt HTML in PowerShell:

```powershell
New-Item -ItemType Directory -Force output
docker run --rm --network none --mount "type=bind,source=$($PWD.Path)/output,target=/output" liser-replication:2026-09-09
```

Linux/macOS:

```sh
mkdir -p output
docker run --rm --network none -v "$PWD/output:/output" liser-replication:2026-09-09
```

The first image build needs internet for the base images and Quarto release. The Python wheel is bundled and hash-locked. Subsequent container execution requires no network. Rebuild the image after editing QMD files. The image includes the full package and runs all checks when built.

Python, Node and Quarto versions are fixed in the Dockerfile. Container image tags and the Quarto download are not digest/hash-locked, so this is not a claim of fully bit-identical environment reconstruction. For long-term archival, save a successfully built image (`docker save`) and record its SHA-256. HTML bytes can also differ across platforms or Quarto environments; numerical and geometry equivalence are tested separately.

## Inputs, sources and limits

See `SOURCES.md`, `INPUT_SHA256.json` and `reference/hand_transcribed_claims.json`. Raw rent/CPI/geometry/Eurostat snapshots are computational inputs. Census, Schifflange and reproducibility-study numbers are transcribed published summaries, with source URLs and table/page identifiers. The package does not contain confidential microdata or the complete published PDFs. Those documents are not needed to rebuild the deck, but consult the linked originals to audit the transcriptions.

The 2025 baseline is 14 within-budget averages among 34 observed communes. The matched 2010–2025 comparison is 29 -> 11 among 29 communes. This is an advertised-rent scenario, not an income-based affordability measure, a count of available homes, a departure-age map or evidence of displacement. The proposed local study and engineering practices are not presented as completed interventions or as all implemented here.

`data/commune_crosswalk.json` preserves the original analyst's spelling and merger decisions. The geometry uses a local display projection, Douglas–Peucker simplification, exterior rings and removal of very small polygon components; label positions are vertex averages, not analytical centroids. Never use display geometry for area or distance estimates. Rates are offer-weighted only where every predecessor is observed. The raw GeoJSON is retained for independent geographic work.

Quarto prose is maintained manually. The separate rehearsal guide is intentionally excluded. Numerical rebuild tests detect changed inputs/results; they do not automatically update prose or validate every narrative claim. No random simulation occurs in this build, so it does not need a seed or an R targets pipeline. Historical migration scripts and unrelated house-price analyses are intentionally omitted.

## Validation status

See `VALIDATION.md` for the actual execution record and Docker limitations. A successful local build does not certify a container build or browser layout.

## Rights

Source datasets retain their providers' terms; source links are in `SOURCES.md`. No blanket relicensing of third-party data, papers, logos or the xlrd wheel is implied. The wheel contains its upstream license. Original code and presentation content by Hamid Bulut are released under the MIT License in `LICENSE`. Third-party materials are excluded from that grant and retain their own terms.
