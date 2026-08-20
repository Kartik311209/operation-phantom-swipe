#!/usr/bin/env bash
# seal_vault.sh - seal the staged vault plaintext into a password-protected zip.
# The plaintext (_build_src/) is deleted afterwards so ONLY the encrypted
# evidence/protected/vault.zip ships in the repo - exactly what an investigator
# receives at seizure. Standard ZipCrypto is used deliberately: it is weak and
# crackable, which is the point of the cryptography sub-problem.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/_build_src/vault"
OUT="$REPO/evidence/protected/vault.zip"
PASSWORD="cashout2024"          # weak, human-chosen, reused (see notes.txt / firmware)

if [ ! -d "$SRC" ]; then
  echo "[!] $SRC missing - run scripts/generate_evidence.py first" >&2
  exit 1
fi

# Build in a scratch dir, then copy the finished archive into place. This keeps
# the operation atomic and portable across filesystems.
TMP="$(mktemp -d)"
( cd "$REPO/_build_src" && zip -P "$PASSWORD" -r "$TMP/vault.zip" vault >/dev/null )
rm -f "$OUT" 2>/dev/null || true
cp "$TMP/vault.zip" "$OUT"
rm -rf "$TMP"
echo "[+] Sealed vault -> ${OUT#$REPO/}  (ZipCrypto, password withheld from repo)"

# Destroy the plaintext so the vault is genuinely locked in the repo.
rm -rf "$REPO/_build_src"
echo "[+] Removed plaintext staging dir (_build_src/)"
echo "[*] Contents (names only; extraction still needs the password):"
unzip -l "$OUT"
