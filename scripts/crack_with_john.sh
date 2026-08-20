#!/usr/bin/env bash
# crack_with_john.sh - INDUSTRY-TOOL equivalent of the dictionary attack.
#
# This is the standard John the Ripper workflow a real examiner would run. It is
# provided as the reference method required by the assignment ("e.g. with John the
# Ripper or hashcat"). If john/zip2john are not installed the script prints the
# exact commands and defers to the portable Python cracker (scripts/crack_zip.py),
# which performs the identical dictionary attack with no external dependencies.
#
# Install (Debian/Ubuntu):  sudo apt-get install -y john   # provides zip2john + john
set -uo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
ZIP="$REPO/evidence/protected/vault.zip"
WORDLIST="$REPO/scripts/wordlist.txt"
HASHFILE="$REPO/logs/vault.hash"

echo "=================================================================="
echo " OPERATION PHANTOM SWIPE - John the Ripper workflow"
echo "=================================================================="
echo " Target   : $ZIP"
echo " Wordlist : $WORDLIST"
echo

if command -v zip2john >/dev/null 2>&1 && command -v john >/dev/null 2>&1; then
    echo "[*] Step 1 - extract crackable hash from the zip:"
    echo "    zip2john \"$ZIP\" > \"$HASHFILE\""
    zip2john "$ZIP" > "$HASHFILE"
    echo "[*] Step 2 - dictionary attack:"
    echo "    john --wordlist=\"$WORDLIST\" \"$HASHFILE\""
    john --wordlist="$WORDLIST" "$HASHFILE"
    echo "[*] Step 3 - show recovered password:"
    echo "    john --show \"$HASHFILE\""
    john --show "$HASHFILE"
else
    echo "[!] john/zip2john not installed on this host."
    echo "[!] The commands that WOULD be run are:"
    echo "        zip2john \"$ZIP\" > \"$HASHFILE\""
    echo "        john --wordlist=\"$WORDLIST\" \"$HASHFILE\""
    echo "        john --show \"$HASHFILE\""
    echo
    echo "[*] Falling back to the portable Python cracker (identical attack):"
    echo "        python3 \"$REPO/scripts/crack_zip.py\""
    echo "------------------------------------------------------------------"
    python3 "$REPO/scripts/crack_zip.py"
fi
