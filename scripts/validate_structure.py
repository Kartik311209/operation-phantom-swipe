#!/usr/bin/env python3
"""
validate_structure.py - repo-structure & deliverable validator.
Used by the GitHub Action (.github/workflows/validate-structure.yml) and runnable
locally. Exits non-zero if any required deliverable is missing or malformed.
"""
from pathlib import Path
import csv, sys

REPO = Path(__file__).resolve().parents[1]
ok, fail = [], []

def check(cond, label):
    (ok if cond else fail).append(label)

REQUIRED_FILES = [
    "README.md",
    "AUTHORSHIP.md",
    "requirements.txt",
    ".github/workflows/validate-structure.yml",
    "docs/01_Cybercrime_Taxonomy_and_Legal_Mapping.md",
    "docs/Legal_Technical_Report.pdf",
    "docs/Chain_of_Custody_Form.pdf",
    "docs/Execution_Guide.md",
    "evidence/device01_skimmer/captured_tracks.log",
    "evidence/device01_skimmer/skimmer_firmware.bin",
    "evidence/device02_phone/apps/carderpro_config.json",
    "evidence/device02_phone/mail/buyer_deal.eml",
    "evidence/protected/vault.zip",
    "hashes/SHA256SUMS.txt",
    "artefacts/extracted_artefacts.md",
    "artefacts/evidence_log.csv",
    "logs/hashing.log",
    "logs/search.log",
    "logs/cracking.log",
    "scripts/generate_evidence.py",
    "scripts/hash_files.py",
    "scripts/search_media.py",
    "scripts/crack_zip.py",
    "scripts/crack_with_john.sh",
    "scripts/seal_vault.sh",
    "screenshots/01_hash_generation.png",
    "screenshots/03_password_crack.png",
]
REQUIRED_DIRS = ["docs","evidence","artefacts","hashes","logs","scripts","screenshots",".github/workflows"]

print("=" * 60)
print(" OPERATION PHANTOM SWIPE - REPO STRUCTURE VALIDATION")
print("=" * 60)

for d in REQUIRED_DIRS:
    check((REPO / d).is_dir(), f"dir  {d}/")
for fpath in REQUIRED_FILES:
    p = REPO / fpath
    check(p.is_file() and p.stat().st_size > 0, f"file {fpath}")

# artefact count >= 5
try:
    n = sum(1 for _ in csv.reader((REPO/"artefacts"/"evidence_log.csv").read_text().splitlines())) - 1
    check(n >= 5, f"artefacts >= 5 (found {n})")
except Exception as e:
    check(False, f"artefacts >= 5 (error: {e})")

# hash manifest >= 5 files
try:
    h = len((REPO/"hashes"/"SHA256SUMS.txt").read_text().splitlines())
    check(h >= 5, f"hashed files >= 5 (found {h})")
except Exception as e:
    check(False, f"hashed files >= 5 (error: {e})")

# vault must still be encrypted (i.e., present as a zip)
try:
    import zipfile
    zf = zipfile.ZipFile(REPO/"evidence"/"protected"/"vault.zip")
    member = next(n for n in zf.namelist() if not n.endswith("/"))
    encrypted = False
    try:
        zf.read(member)              # no password -> should fail if encrypted
    except RuntimeError:
        encrypted = True
    check(encrypted, "vault.zip is password-protected")
except Exception as e:
    check(False, f"vault.zip check (error: {e})")

for label in ok:
    print(f"  [PASS] {label}")
for label in fail:
    print(f"  [FAIL] {label}")

print("-" * 60)
print(f" {len(ok)} passed, {len(fail)} failed")
print("=" * 60)
sys.exit(1 if fail else 0)
