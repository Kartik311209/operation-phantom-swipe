# Execution Guide — Operation Phantom Swipe

This guide reproduces the entire investigation from a clean checkout. The **core
forensic pipeline requires only Python 3** (standard library) and common Unix tools
(`zip`, `unzip`, `sha256sum`). ReportLab/Pillow are needed **only** to rebuild the
PDFs and screenshots.

## 0. Prerequisites

```bash
python3 --version        # 3.8+
zip -v ; unzip -v ; sha256sum --version
# Optional, for PDFs & screenshots:
pip install -r requirements.txt
# Optional, for the John the Ripper reference workflow:
sudo apt-get install -y john      # provides zip2john + john
```

## 1. One-shot reproduction

```bash
bash scripts/run_all.sh
python3 scripts/validate_structure.py   # should print "N passed, 0 failed"
```

## 2. Step-by-step

### Step 1 — Generate simulated evidence
```bash
python3 scripts/generate_evidence.py
```
Creates the two seized-device file sets under `evidence/` and stages the vault
plaintext in `_build_src/` (git-ignored).

### Step 2 — Seal the password-protected vault
```bash
bash scripts/seal_vault.sh
```
Zips the staged plaintext into `evidence/protected/vault.zip` (ZipCrypto, password
withheld) and **deletes** the plaintext, so the vault ships genuinely locked.

### Step 3 — Hash all acquired media (SHA-256)
```bash
python3 scripts/hash_files.py
```
Writes `hashes/SHA256SUMS.txt` and `logs/hashing.log`. Verify integrity anytime:
```bash
sha256sum -c hashes/SHA256SUMS.txt      # every line should read "OK"
```

### Step 4 — Search media & extract artefacts
```bash
python3 scripts/search_media.py
```
Regex string-search + binary string-carving + EXIF metadata + e-mail parsing.
Produces `artefacts/extracted_artefacts.md`, `artefacts/evidence_log.csv`,
`logs/search.log`. Recovered card numbers are Luhn-validated.

### Step 5 — Crack the protected vault
```bash
python3 scripts/crack_zip.py                    # portable, pure-Python dictionary attack
# — or the industry-tool equivalent —
bash   scripts/crack_with_john.sh               # zip2john → john (falls back to the above)
```
Recovers the password, logs the attempt to `logs/cracking.log`, and extracts the
dumps to `artefacts/recovered/`.

### Step 6 — Rebuild documents & screenshots (optional)
```bash
python3 scripts/make_report_pdf.py     # docs/Legal_Technical_Report.pdf
python3 scripts/make_coc_pdf.py        # docs/Chain_of_Custody_Form.pdf
python3 scripts/make_screenshots.py    # screenshots/*.png
```

## 3. Continuous integration

`.github/workflows/validate-structure.yml` runs on every push:

1. **structure** — `validate_structure.py` asserts every deliverable exists and the
   vault is still encrypted.
2. **reproducibility** — regenerates evidence, re-seals the vault, hashes, verifies
   `sha256sum -c`, runs the search, cracks the vault, and asserts the password was
   recovered; run logs are uploaded as a build artefact.

## 4. Expected headline results

| Step | Expected |
|---|---|
| Hashing | 14 files hashed; `sha256sum -c` all **OK** |
| Search | **19** artefacts catalogued; 5 unique Luhn-valid PANs |
| Crack | password **`cashout2024`** recovered in ~41 guesses (<0.01 s) |
| Report | `Legal_Technical_Report.pdf`, 5 pages |
| Validate | `N passed, 0 failed` |

## 5. Tools used
Python 3 stdlib (`hashlib`, `zipfile`, `re`, `csv`, `struct`); coreutils
`sha256sum`; Info-ZIP `zip`/`unzip`; John the Ripper / hashcat (reference);
ReportLab; Pillow; GitHub Actions.
