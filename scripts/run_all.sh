#!/usr/bin/env bash
# run_all.sh - reproduce the entire investigation end-to-end.
#   1. generate simulated evidence      4. search media & extract artefacts
#   2. seal the password-protected vault 5. crack the vault (dictionary attack)
#   3. hash all acquired media (SHA-256)  6. render tool-usage screenshots + docs
set -euo pipefail
cd "$(dirname "$0")/.."
echo "==> [1/7] Generating simulated evidence";      python3 scripts/generate_evidence.py
echo "==> [2/7] Sealing password-protected vault";   bash   scripts/seal_vault.sh
echo "==> [3/7] Hashing acquired media (SHA-256)";   python3 scripts/hash_files.py
echo "==> [4/7] Verifying integrity manifest";       sha256sum -c hashes/SHA256SUMS.txt
echo "==> [5/7] Searching media & extracting artefacts"; python3 scripts/search_media.py
echo "==> [6/7] Cracking the protected vault";       python3 scripts/crack_zip.py || true
echo "==> [7/7] Rendering screenshots + PDFs (needs reportlab, Pillow)"
python3 scripts/make_screenshots.py || echo "   (skipped screenshots - Pillow missing)"
python3 scripts/make_coc_pdf.py     || echo "   (skipped CoC PDF - reportlab missing)"
python3 scripts/make_report_pdf.py  || echo "   (skipped report PDF - reportlab missing)"
echo "==> DONE. Validate with: python3 scripts/validate_structure.py"
