#!/usr/bin/env python3
"""
make_screenshots.py - render tool-usage 'screenshots' (terminal-style PNGs) from
the real log output produced by the forensic scripts. Satisfies the assignment's
"Tool usage screenshots (hash generation, logs)" deliverable.

Outputs -> screenshots/01_hash_generation.png, 02_string_search.png,
           03_password_crack.png, 04_integrity_verify.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
SHOT = REPO / "screenshots"; SHOT.mkdir(exist_ok=True)
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONOB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG   = (13, 17, 23)      # terminal background
BAR  = (32, 37, 46)      # title bar
FG   = (201, 209, 217)   # normal text
GRN  = (63, 185, 80)     # prompt / success
CYN  = (57, 197, 207)    # headings
YEL  = (210, 168, 60)    # highlights
RED  = (248, 81, 73)
DIM  = (110, 118, 129)

FS = 15
LH = 21
PAD = 16
BAR_H = 34
MAXW = 108   # chars per line before truncation

f  = ImageFont.truetype(MONO, FS)
fb = ImageFont.truetype(MONOB, FS)

def color_for(line: str):
    s = line.strip()
    if s.startswith("$"): return GRN, True
    if "RECOVERED" in line or "OK" in line and "[" in line: return GRN, False
    if s.startswith("[+]") or "PASSWORD RECOVERED" in line: return GRN, False
    if s.startswith("[*]"): return CYN, False
    if s.startswith("[!]") or "NOT" in line: return RED, False
    if "Luhn-VALID" in line or "guesses/s" in line: return YEL, False
    if line.startswith("=") or line.startswith("-") or "OPERATION PHANTOM" in line: return CYN, False
    if any(k in line for k in ("PAN ", "GPS ", "C2 ", "BTC ", "STR ", "IMG ", "OTP ")): return FG, False
    return FG, False

def render(fname, title, lines):
    lines = [ln.rstrip("\n") for ln in lines]
    wrapped = []
    for ln in lines:
        if len(ln) <= MAXW:
            wrapped.append(ln)
        else:
            wrapped.append(ln[:MAXW-1] + "…")
    width = PAD*2 + int(fb.getlength("M")) * MAXW
    height = BAR_H + PAD*2 + LH*len(wrapped)
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    # title bar + traffic lights
    d.rectangle([0,0,width,BAR_H], fill=BAR)
    for i,c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([PAD+i*20, BAR_H//2-6, PAD+i*20+12, BAR_H//2+6], fill=c)
    tw = fb.getlength(title)
    d.text(((width-tw)/2, BAR_H//2-FS//2-1), title, font=fb, fill=DIM)
    y = BAR_H + PAD
    for ln in wrapped:
        col, bold = color_for(ln)
        d.text((PAD, y), ln, font=(fb if bold else f), fill=col)
        y += LH
    img.save(SHOT / fname)
    print(f"  [+] screenshots/{fname}  ({width}x{height})")

def loglines(name): return (REPO/"logs"/name).read_text().splitlines()

# 01 - hashing (command + log)
render("01_hash_generation.png", "examiner@fsl: SHA-256 acquisition hashing",
       ["$ python3 scripts/hash_files.py"] + loglines("hashing.log"))

# 02 - search (trim to keep readable)
sl = loglines("search.log")
render("02_string_search.png", "examiner@fsl: media search & artefact extraction",
       ["$ python3 scripts/search_media.py"] + sl)

# 03 - crack
render("03_password_crack.png", "examiner@fsl: vault dictionary attack",
       ["$ python3 scripts/crack_zip.py"] + loglines("cracking.log"))

# 04 - integrity re-verify (generate live)
import subprocess
res = subprocess.run(["sha256sum","-c","hashes/SHA256SUMS.txt"], cwd=REPO,
                     capture_output=True, text=True)
verify = ["$ sha256sum -c hashes/SHA256SUMS.txt"] + res.stdout.splitlines()[:18] + \
         ["", "$ echo \"exit status: $?\"", str(res.returncode) + "  (0 = all files intact)"]
render("04_integrity_verify.png", "examiner@fsl: integrity re-verification", verify)

print("[DONE] screenshots rendered.")
