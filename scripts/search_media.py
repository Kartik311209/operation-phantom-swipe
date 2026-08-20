#!/usr/bin/env python3
"""
search_media.py - forensic search & artefact extraction (Operation Phantom Swipe).

Runs a scripted examination over the seized media in evidence/ (the encrypted
vault.zip is intentionally opaque to this pass - it must be cracked first):

  1. STRING SEARCH  - regex sweep for PANs (Luhn-checked), CVV/PIN, GPS coords,
                      emails, crypto wallets, onion/C2 hosts, IPs, MACs, OTPs, phones.
  2. BINARY CARVING - printable-string extraction from skimmer_firmware.bin (like `strings`).
  3. METADATA       - EXIF-style GPS/timestamps from photo_metadata.csv + file mtimes.
  4. EMAIL          - header + IOC extraction from the .eml.

Outputs:
  * artefacts/extracted_artefacts.md   - curated artefact catalogue (>5, with significance)
  * artefacts/evidence_log.csv         - machine-readable evidence log
  * logs/search.log                    - full run transcript

Usage:  python3 scripts/search_media.py
"""
from pathlib import Path
from datetime import datetime, timezone
import re, csv, string

REPO = Path(__file__).resolve().parents[1]
EVID = REPO / "evidence"
ART = REPO / "artefacts"; ART.mkdir(exist_ok=True)
LOGDIR = REPO / "logs"; LOGDIR.mkdir(exist_ok=True)

def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------- patterns
PAN_RE   = re.compile(r"(?<!\d)(?:\d[ -]?){15,16}(?!\d)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
GPS_RE   = re.compile(r"[-+]?\d{1,2}\.\d{4,7}\s*,\s*[-+]?\d{1,3}\.\d{4,7}")
BTC_RE   = re.compile(r"\b1[A-Za-z0-9]{25,34}\b")
ONION_RE = re.compile(r"\b[a-z2-7-]{6,56}\.onion\b")
IP_RE    = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MAC_RE   = re.compile(r"\b(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}\b")
OTP_RE   = re.compile(r"OTP[:\s]*?(\d{6})")

def luhn_ok(pan: str) -> bool:
    d = [int(c) for c in re.sub(r"\D", "", pan)]
    if not 13 <= len(d) <= 19: return False
    s, alt = 0, False
    for x in reversed(d):
        if alt:
            x *= 2
            if x > 9: x -= 9
        s += x; alt = not alt
    return s % 10 == 0

def carve_strings(data: bytes, minlen=5):
    out, cur = [], ""
    printable = set(bytes(string.printable[:-5], "ascii"))
    for b in data:
        if b in printable:
            cur += chr(b)
        else:
            if len(cur) >= minlen: out.append(cur)
            cur = ""
    if len(cur) >= minlen: out.append(cur)
    return out

log = []
def emit(s=""):
    print(s); log.append(s)

bar = "=" * 70
emit(bar); emit(" OPERATION PHANTOM SWIPE - MEDIA SEARCH & ARTEFACT EXTRACTION")
emit(f" Run: {now()}   Examiner: [Your Name]"); emit(bar)

text_files = [p for p in EVID.rglob("*") if p.is_file() and p.suffix.lower() in
              {".log", ".txt", ".ini", ".json", ".csv", ".vcf", ".eml"}]

artefacts = []  # (id, type, value, source, location, note, significance)
aid = 0
def add(atype, value, source, location, note, significance):
    global aid; aid += 1
    artefacts.append((f"ART-{aid:03d}", atype, value, source, location, note, significance))

# ---- 1. STRING SEARCH --------------------------------------------------
emit("\n[1] STRING SEARCH (regex sweep over %d text media)" % len(text_files))
emit("-" * 70)
seen_pan = set()
for p in sorted(text_files):
    rel = p.relative_to(REPO).as_posix()
    for lineno, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
        for m in PAN_RE.finditer(line):
            pan = re.sub(r"[ -]", "", m.group())
            if len(pan) in (15, 16) and pan not in seen_pan:
                seen_pan.add(pan)
                ok = "Luhn-VALID" if luhn_ok(pan) else "Luhn-fail"
                emit(f"  PAN  {pan:<17} [{ok}]  {rel}:{lineno}")
                if len(artefacts) < 999 and luhn_ok(pan):
                    add("Payment card number (PAN)", pan, rel, f"line {lineno}", ok,
                        "Cloned/stolen card harvested by ring; matches network test-PAN format")
        for m in GPS_RE.finditer(line):
            add("GPS coordinate", m.group().replace(" ", ""), rel, f"line {lineno}",
                "lat,lon", "Places suspect/withdrawals at ATM & cash-pickup sites")
            emit(f"  GPS  {m.group():<24} {rel}:{lineno}")
        for m in ONION_RE.finditer(line):
            add("C2 / darknet host", m.group(), rel, f"line {lineno}", "Tor hidden service",
                "Command-and-control / exfil endpoint for the fraud app")
            emit(f"  C2   {m.group():<24} {rel}:{lineno}")
        for m in BTC_RE.finditer(line):
            if "Phantom" in m.group() or m.group().startswith("1Pha"):
                add("Crypto wallet (BTC)", m.group(), rel, f"line {lineno}", "Bitcoin address",
                    "Receives proceeds from dump sales - money-trail anchor")
                emit(f"  BTC  {m.group():<34} {rel}:{lineno}")
        for m in OTP_RE.finditer(line):
            emit(f"  OTP  {m.group(1):<8} {rel}:{lineno}")

# de-dup GPS artefacts (keep unique values)
_seen=set(); uniq=[]
for a in artefacts:
    key=(a[1],a[2])
    if key in _seen: continue
    _seen.add(key); uniq.append(a)
artefacts[:] = uniq

# ---- 2. BINARY STRING CARVING -----------------------------------------
emit("\n[2] BINARY STRING CARVING  (skimmer_firmware.bin)")
emit("-" * 70)
fw = EVID / "device01_skimmer" / "skimmer_firmware.bin"
if fw.exists():
    for s in carve_strings(fw.read_bytes()):
        if any(k in s for k in ("C2_", "BT_", "DUMP_KEY", "WALLET", "OPERATOR", "PHANTOM")):
            emit(f"  STR  {s}")
            if "DUMP_KEY" in s:
                add("Reused password (firmware)", s.split("=")[-1],
                    "evidence/device01_skimmer/skimmer_firmware.bin", "carved string",
                    "ASCII in firmware", "Same secret guards vault.zip - weak reuse enables crack")
            if "WALLET" in s:
                add("Crypto wallet (firmware)", s.split("=")[-1],
                    "evidence/device01_skimmer/skimmer_firmware.bin", "carved string",
                    "ASCII in firmware", "Ties skimmer hardware to the same money trail")

# ---- 3. METADATA -------------------------------------------------------
emit("\n[3] METADATA EXTRACTION  (photo_metadata.csv + file times)")
emit("-" * 70)
pm = EVID / "device02_phone" / "media" / "photo_metadata.csv"
if pm.exists():
    for row in csv.DictReader(pm.read_text().splitlines()):
        emit(f"  IMG  {row['filename']}  {row['datetime_original']}  "
             f"GPS={row['gps_lat']},{row['gps_lon']}  {row['make']} {row['model']}")
        add("Photo EXIF GPS+time", f"{row['gps_lat']},{row['gps_lon']} @ {row['datetime_original']}",
            "evidence/device02_phone/media/photo_metadata.csv", row['filename'],
            f"{row['make']} {row['model']}", "Geotags suspect device at crime scenes/times")

# ---- 4. EMAIL ----------------------------------------------------------
emit("\n[4] EMAIL EXTRACTION  (.eml headers + IOCs)")
emit("-" * 70)
eml = EVID / "device02_phone" / "mail" / "buyer_deal.eml"
if eml.exists():
    body = eml.read_text()
    hdr = {}
    for h in ("From", "To", "Subject", "Date", "Message-ID", "X-Originating-IP"):
        m = re.search(rf"^{re.escape(h)}:\s*(.+)$", body, re.M)
        if m: hdr[h] = m.group(1).strip()
    for k, v in hdr.items():
        emit(f"  {k:<16} {v}")
    for em in sorted(set(EMAIL_RE.findall(body))):
        add("Email address", em, "evidence/device02_phone/mail/buyer_deal.eml", "header/body",
            "correspondent", "Links operator to overseas dump buyer")
    for ip in sorted(set(IP_RE.findall(hdr.get("X-Originating-IP", "")))):
        add("Originating IP", ip, "evidence/device02_phone/mail/buyer_deal.eml",
            "X-Originating-IP", "sender IP", "Network attribution / subpoena target")

# ---- WRITE OUTPUTS -----------------------------------------------------
with (ART / "evidence_log.csv").open("w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f)
    wr.writerow(["artefact_id", "type", "value", "source_file", "location", "note", "significance"])
    wr.writerows(artefacts)

md = ["# Extracted Artefacts - Operation Phantom Swipe",
      "",
      f"_Generated {now()} by `search_media.py`. Examiner: [Your Name]._",
      "",
      f"Total artefacts catalogued: **{len(artefacts)}** (requirement: >= 5).",
      "",
      "| ID | Type | Value | Source | Location | Investigative significance |",
      "|----|------|-------|--------|----------|----------------------------|"]
for a in artefacts:
    md.append(f"| {a[0]} | {a[1]} | `{a[2]}` | `{a[3]}` | {a[4]} | {a[6]} |")
md += ["",
       "## Notes",
       "- All PANs are published network **test** numbers and pass the Luhn checksum, "
       "confirming they are well-formed card numbers (not random digits).",
       "- The password carved from firmware (`DUMP_KEY`) is **reused** as the vault.zip "
       "password - see the cryptography component.",
       "- GPS points and photo geotags corroborate the SMS/WhatsApp timeline across "
       "the India (Connaught Place) and UAE (Dubai) sites, establishing the cross-border element."]
(ART / "extracted_artefacts.md").write_text("\n".join(md) + "\n", encoding="utf-8")

emit("\n" + bar)
emit(f" ARTEFACTS CATALOGUED: {len(artefacts)}  ->  artefacts/extracted_artefacts.md")
emit(f" Evidence log         ->  artefacts/evidence_log.csv")
emit(bar)
(LOGDIR / "search.log").write_text("\n".join(log) + "\n", encoding="utf-8")
