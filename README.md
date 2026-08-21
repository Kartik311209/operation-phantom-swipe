# Operation Phantom Swipe
### Investigating a Cross-Border ATM & Credit-Card Fraud Ring
**Assignment 1 — Unit 1: Foundations of Digital Forensics**

> ⚠️ **Academic simulation.** Every artefact in this repository is fabricated for a
> teaching exercise. All card numbers are the **publicly published network *test*
> PANs**; all names, e-mails, phone numbers, wallets, IPs and GPS points are
> fictitious. Nothing here is real data, and the tooling is provided strictly for
> lawful, educational forensic practice.

---

## 1. Author

| | |
|---|---|
| **Name** |Kartik Kumar|
| **Roll No.** | 2301730205 |
| **Course / Subject** |B.Tech CSE AIML (Section - 3) |
| **Institution** |K.R Mangalam University |
| **Submission date** |21-08-2026 |

---

## 2. Scenario

An organised ring installs **ATM skimmers** with PIN-pad overlays in New Delhi and
Dubai, **clones** the harvested cards, commits **online / card-not-present fraud**,
and **sells the stolen "dumps"** to an overseas buyer with proceeds moved in
cryptocurrency. Two exhibits were seized — a **skimmer** (`EXH-01`) and an
**operator's phone** (`EXH-02`) — and examined in this early-phase investigation.

## 3. Repository structure

```
operation-phantom-swipe/
├── README.md                      ← you are here (overview + execution guide)
├── AUTHORSHIP.md                  ← authorship declaration
├── requirements.txt               ← Python deps (only for PDFs/screenshots)
├── .github/workflows/
│   └── validate-structure.yml     ← CI: structure check + reproducibility
├── docs/
│   ├── 01_Cybercrime_Taxonomy_and_Legal_Mapping.md   ← Sub-problem 1
│   ├── Legal_Technical_Report.pdf                     ← Sub-problem 5 (main report)
│   ├── Chain_of_Custody_Form.pdf                      ← Sub-problem 2
│   └── Execution_Guide.md                             ← how to run everything
├── evidence/
│   ├── device01_skimmer/          ← EXH-01: tracks, config, BT pairing, firmware
│   ├── device02_phone/            ← EXH-02: SMS, WhatsApp, apps, mail, media, notes
│   └── protected/vault.zip        ← password-protected dumps (Sub-problem 4)
├── artefacts/
│   ├── extracted_artefacts.md     ← catalogue of recovered artefacts (Sub-problem 3)
│   ├── evidence_log.csv           ← machine-readable evidence log
│   └── recovered/                 ← files recovered AFTER cracking the vault
├── hashes/SHA256SUMS.txt          ← SHA-256 of every acquired file
├── logs/                          ← real run transcripts (hashing/search/cracking)
├── screenshots/                   ← tool-usage screenshots (PNG)
└── scripts/                       ← all Python/Bash tooling
    ├── generate_evidence.py  hash_files.py  search_media.py  crack_zip.py
    ├── seal_vault.sh  crack_with_john.sh  run_all.sh  validate_structure.py
    ├── make_report_pdf.py  make_coc_pdf.py  make_screenshots.py
    └── wordlist.txt
```

## 4. Quick start

```bash
# Core forensic pipeline uses ONLY the Python standard library:
bash scripts/run_all.sh              # generate → seal → hash → verify → search → crack

# To regenerate the PDFs and screenshots as well:
pip install -r requirements.txt
python3 scripts/make_report_pdf.py && python3 scripts/make_coc_pdf.py && python3 scripts/make_screenshots.py

# Validate the submission the same way CI does:
python3 scripts/validate_structure.py
```
See **`docs/Execution_Guide.md`** for step-by-step details and expected output.

## 5. How each sub-problem is addressed

| # | Sub-problem | Where to look |
|---|---|---|
| 1 | Cybercrime classification & legal mapping | `docs/01_Cybercrime_Taxonomy_and_Legal_Mapping.md` (IT Act 2000, IPC 1860, Budapest) + Appendix A of the report |
| 2 | Evidence collection simulation + chain of custody + SHA-256 | `scripts/generate_evidence.py`, `scripts/hash_files.py`, `hashes/SHA256SUMS.txt`, `docs/Chain_of_Custody_Form.pdf` |
| 3 | Media search & artefact extraction (5+) | `scripts/search_media.py`, `artefacts/extracted_artefacts.md`, `artefacts/evidence_log.csv`, `logs/search.log` |
| 4 | Cryptography — crack the protected folder | `evidence/protected/vault.zip`, `scripts/crack_zip.py`, `scripts/crack_with_john.sh`, `logs/cracking.log` |
| 5 | Legal-ethical report (4–6 pages) | `docs/Legal_Technical_Report.pdf` |

## 6. Mapping to the evaluation criteria (10 marks)

| Marks | Criterion | Evidence in this repo |
|---|---|---|
| 1.5 | Cybercrime taxonomy & legal mapping | `docs/01_Cybercrime_Taxonomy_and_Legal_Mapping.md` |
| 2.0 | Evidence acquisition + chain of custody | `hashes/SHA256SUMS.txt`, `logs/hashing.log`, `docs/Chain_of_Custody_Form.pdf` |
| 2.0 | File/media analysis & artefact extraction | `artefacts/`, `logs/search.log`, `screenshots/02_string_search.png` |
| 1.5 | Cryptography simulation & discussion | `logs/cracking.log`, report §3.2–3.4, `screenshots/03_password_crack.png` |
| 2.0 | Final legal-technical report quality | `docs/Legal_Technical_Report.pdf` |
| 1.0 | GitHub structure, documentation, CI | this README, `docs/Execution_Guide.md`, `.github/workflows/validate-structure.yml` |

## 7. Tools used

Python 3 standard library (`hashlib`, `zipfile`, `re`, `csv`, `struct`) · GNU
coreutils `sha256sum` · Info-ZIP `zip`/`unzip` · **John the Ripper / hashcat**
(reference cracking workflow in `scripts/crack_with_john.sh`) · **ReportLab** (PDF
typesetting) · **Pillow** (screenshots) · **GitHub Actions** (CI).

## 8. Ethics & safety

This project simulates criminal tooling only to teach lawful investigation. The
cracking utilities operate exclusively on the bundled dummy `vault.zip`. Do not use
them against data you are not authorised to access — unauthorised access is itself
an offence under §§43/66 of the IT Act, 2000. See report §3.3 for the discussion of
brute-force vs. lawful decryption requests.

## 9. Authorship declaration

See **`AUTHORSHIP.md`**. In short: this is my own original work for the course named
above; all case data is simulated; external tools are credited in §7.
