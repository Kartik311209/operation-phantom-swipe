#!/usr/bin/env python3
"""
crack_zip.py - dictionary attack against evidence/protected/vault.zip
(Operation Phantom Swipe - cryptography sub-problem).

Pure-Python, no external tools required. Iterates a wordlist and tests each
candidate against the ZipCrypto-protected archive; the first candidate that
decrypts a member cleanly is the password. On success the recovered files are
written to artefacts/recovered/ (lawful post-decryption evidence handling).

This mirrors what `john`/`hashcat` would do against a `zip2john` hash - see
crack_with_john.sh for the equivalent industry-tool workflow. ZipCrypto falls
in milliseconds precisely because the password is short, lowercase and reused;
that weakness is the point of this exercise.

Usage:  python3 scripts/crack_zip.py [wordlist]
"""
from pathlib import Path
from datetime import datetime, timezone
import zipfile, sys, time

REPO = Path(__file__).resolve().parents[1]
ZIP = REPO / "evidence" / "protected" / "vault.zip"
WORDLIST = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "scripts" / "wordlist.txt"
RECOVERED = REPO / "artefacts" / "recovered"
LOGDIR = REPO / "logs"; LOGDIR.mkdir(exist_ok=True)

def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

log = []
def emit(s=""): print(s); log.append(s)

bar = "=" * 66
emit(bar)
emit(" OPERATION PHANTOM SWIPE - VAULT DICTIONARY ATTACK")
emit(f" Target : {ZIP.relative_to(REPO).as_posix()}")
emit(f" Wordlist: {WORDLIST.relative_to(REPO).as_posix()}")
emit(f" Run    : {now()}   Examiner: [Your Name]")
emit(bar)

if not ZIP.exists():
    emit("[!] vault.zip not found - run generate_evidence.py + seal_vault.sh first"); sys.exit(1)

zf = zipfile.ZipFile(ZIP)
target_member = next(n for n in zf.namelist() if not n.endswith("/"))
words = [w.rstrip("\n") for w in WORDLIST.read_text(encoding="utf-8").splitlines() if w.strip()]
emit(f"[*] {len(words)} candidate passwords loaded")
emit(f"[*] Testing against member: {target_member}\n")

found, attempts = None, 0
t0 = time.time()
for w in words:
    attempts += 1
    try:
        zf.read(target_member, pwd=w.encode())
        found = w
        break
    except (RuntimeError, zipfile.BadZipFile):
        if attempts % 10 == 0:
            emit(f"    ... {attempts} tried (last: {w})")
        continue
elapsed = time.time() - t0

emit("")
if found:
    emit(bar)
    emit(f" [+] PASSWORD RECOVERED : '{found}'")
    emit(f" [+] Attempts           : {attempts}/{len(words)}")
    emit(f" [+] Time               : {elapsed:.4f} s  ({attempts/max(elapsed,1e-9):,.0f} guesses/s)")
    emit(bar)
    RECOVERED.mkdir(parents=True, exist_ok=True)
    zf.extractall(RECOVERED, pwd=found.encode())
    emit(" [+] Recovered files -> artefacts/recovered/")
    for n in zf.namelist():
        if not n.endswith("/"):
            emit(f"       - {n}")
else:
    emit(" [-] Password NOT in wordlist. Escalate to larger list / mask attack.")

zf.close()
(LOGDIR / "cracking.log").write_text("\n".join(log) + "\n", encoding="utf-8")
emit("\n[*] Transcript saved -> logs/cracking.log")
sys.exit(0 if found else 2)
