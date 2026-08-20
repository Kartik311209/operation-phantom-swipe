#!/usr/bin/env python3
"""
hash_files.py - forensic hashing of acquired media (Operation Phantom Swipe).

Walks evidence/ and computes SHA-256 (chunked, so large images are never fully
loaded into RAM) plus size + acquisition time for every acquired file. Emits:
  * hashes/SHA256SUMS.txt   - verifiable with `sha256sum -c SHA256SUMS.txt`
  * logs/hashing.log        - timestamped acquisition log

Hashing at acquisition is what lets us later PROVE the evidence was not altered:
re-hashing any file and comparing to this baseline is the integrity check that
underpins the chain of custody.

Usage:  python3 scripts/hash_files.py
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib

REPO = Path(__file__).resolve().parents[1]
EVID = REPO / "evidence"
HASHDIR = REPO / "hashes"; HASHDIR.mkdir(exist_ok=True)
LOGDIR = REPO / "logs"; LOGDIR.mkdir(exist_ok=True)

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

files = sorted(p for p in EVID.rglob("*") if p.is_file())
sums_lines, log_lines = [], []
banner = "=" * 68
log_lines.append(banner)
log_lines.append(" OPERATION PHANTOM SWIPE - EVIDENCE HASHING LOG (SHA-256)")
log_lines.append(f" Generated: {now()}   Examiner: [Your Name]")
log_lines.append(f" Tool: hash_files.py (Python {__import__('sys').version.split()[0]}, hashlib)")
log_lines.append(banner)

print(banner)
print(" SHA-256 ACQUISITION HASHING")
print(banner)
for i, p in enumerate(files, 1):
    digest = sha256(p)
    rel = p.relative_to(REPO).as_posix()
    size = p.stat().st_size
    sums_lines.append(f"{digest}  {rel}")
    line = f"[{i:02d}] {digest}  {size:>7} B  {rel}"
    log_lines.append(line)
    print(line)

(HASHDIR / "SHA256SUMS.txt").write_text("\n".join(sums_lines) + "\n", encoding="utf-8")
log_lines.append(banner)
log_lines.append(f" TOTAL FILES HASHED: {len(files)}")
log_lines.append(banner)
(LOGDIR / "hashing.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

print(banner)
print(f" {len(files)} files hashed -> hashes/SHA256SUMS.txt")
print(f" Verify anytime with:  sha256sum -c hashes/SHA256SUMS.txt")
print(banner)
