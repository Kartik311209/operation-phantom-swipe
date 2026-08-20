#!/usr/bin/env python3
"""
make_coc_pdf.py - render the Chain-of-Custody form to docs/Chain_of_Custody_Form.pdf
Hashes are pulled live from hashes/SHA256SUMS.txt so the form always matches the
actual acquired evidence. Run scripts/hash_files.py first.
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable)

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "Chain_of_Custody_Form.pdf"
SUMS = REPO / "hashes" / "SHA256SUMS.txt"

# ---- pull hashes -------------------------------------------------------
hashes = {}
if SUMS.exists():
    for line in SUMS.read_text().splitlines():
        if "  " in line:
            h, f = line.split("  ", 1)
            hashes[f.strip()] = h.strip()

def short(path):
    return hashes.get(path, "—")

NAVY = colors.HexColor("#1a2b4a")
GREY = colors.HexColor("#e8ebf0")
styles = getSampleStyleSheet()
st_title = ParagraphStyle("t", parent=styles["Title"], fontSize=17, textColor=NAVY, spaceAfter=2)
st_sub = ParagraphStyle("s", parent=styles["Normal"], fontSize=8.5, textColor=colors.grey)
st_h = ParagraphStyle("h", parent=styles["Heading2"], fontSize=11, textColor=NAVY, spaceBefore=10, spaceAfter=4)
st_n = ParagraphStyle("n", parent=styles["Normal"], fontSize=8.5, leading=12)
st_cell = ParagraphStyle("c", parent=styles["Normal"], fontSize=7.6, leading=9.5)
st_cellb = ParagraphStyle("cb", parent=st_cell, fontName="Helvetica-Bold")
st_mono = ParagraphStyle("m", parent=styles["Normal"], fontName="Courier", fontSize=6.6, leading=8)

def P(t, s=st_cell): return Paragraph(t, s)

doc = SimpleDocTemplate(str(OUT), pagesize=A4, topMargin=14*mm, bottomMargin=14*mm,
                        leftMargin=15*mm, rightMargin=15*mm,
                        title="Chain of Custody Form - Operation Phantom Swipe")
E = []
E.append(Paragraph("CHAIN OF CUSTODY FORM", st_title))
E.append(Paragraph("Digital Evidence — Confidential Law-Enforcement Record", st_sub))
E.append(HRFlowable(width="100%", thickness=1.2, color=NAVY, spaceBefore=4, spaceAfter=8))

# ---- case header -------------------------------------------------------
case = [
    [P("Case / Operation:", st_cellb), P("Operation Phantom Swipe"),
     P("Case / FIR No.:", st_cellb), P("[FIR No.]")],
    [P("Offences:", st_cellb), P("IT Act s.66/66B/66C/66D; IPC s.420/465/471/120B"),
     P("Cyber PS / Unit:", st_cellb), P("[Cyber Police Station]")],
    [P("Investigating Officer:", st_cellb), P("[IO Name & Rank]"),
     P("Forensic Examiner:", st_cellb), P("[Your Name]")],
    [P("Seizure date/time:", st_cellb), P("2024-11-05, 07:30 IST"),
     P("Seizure location:", st_cellb), P("Connaught Place, New Delhi (premises)")],
]
t = Table(case, colWidths=[32*mm, 62*mm, 30*mm, 56*mm])
t.setStyle(TableStyle([
    ("BOX", (0,0), (-1,-1), 0.6, NAVY), ("INNERGRID", (0,0), (-1,-1), 0.4, colors.lightgrey),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("BACKGROUND", (0,0), (0,-1), GREY),
    ("BACKGROUND", (2,0), (2,-1), GREY), ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
]))
E.append(t)

# ---- exhibits ----------------------------------------------------------
E.append(Paragraph("1. Seized Exhibits", st_h))
ex_head = [P("Exhibit ID", st_cellb), P("Description", st_cellb), P("Make / Model / Serial", st_cellb),
           P("Seal / Tag No.", st_cellb), P("Acquired by", st_cellb)]
ex_rows = [
    [P("EXH-01"), P("ATM magnetic-stripe skimmer + PIN-pad overlay (embedded device)"),
     P("PHANTOM-SKIMMER v2 / SN PS2-000734"), P("[Seal #A-0001]"), P("[Your Name]")],
    [P("EXH-02"), P("Operator smartphone (fraud apps, dumps, chat)"),
     P("Samsung SM-M325F (Galaxy M32) / IMEI [•]"), P("[Seal #A-0002]"), P("[Your Name]")],
]
t = Table([ex_head]+ex_rows, colWidths=[16*mm, 55*mm, 48*mm, 25*mm, 36*mm])
t.setStyle(TableStyle([
    ("BOX",(0,0),(-1,-1),0.6,NAVY),("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
]))
E.append(t)

# ---- acquisition & integrity ------------------------------------------
E.append(Paragraph("2. Acquisition &amp; Integrity Verification (SHA-256)", st_h))
E.append(Paragraph("Working copies were acquired through a hardware <b>write-blocker</b>; "
                   "originals were not mounted read-write at any point. Each acquired file was "
                   "hashed with SHA-256 at acquisition. Full manifest: <font face='Courier'>hashes/SHA256SUMS.txt</font>.", st_n))
hh = [P("Exhibit", st_cellb), P("Key acquired file", st_cellb), P("SHA-256 (acquisition baseline)", st_cellb)]
key_files = [
    ("EXH-01", "evidence/device01_skimmer/captured_tracks.log"),
    ("EXH-01", "evidence/device01_skimmer/skimmer_firmware.bin"),
    ("EXH-02", "evidence/device02_phone/apps/carderpro_config.json"),
    ("EXH-02", "evidence/device02_phone/mail/buyer_deal.eml"),
    ("EXH-02", "evidence/protected/vault.zip"),
]
rows = [hh]
for ex, f in key_files:
    rows.append([P(ex), P(f.split("/")[-1]), Paragraph(short(f), st_mono)])
t = Table(rows, colWidths=[16*mm, 55*mm, 109*mm])
t.setStyle(TableStyle([
    ("BOX",(0,0),(-1,-1),0.6,NAVY),("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5),
]))
E.append(t)

# ---- handling checklist -----------------------------------------------
E.append(Paragraph("3. Evidence-Handling Checklist", st_h))
chk = [
    [P("[X]", st_cellb), P("Photographed <i>in situ</i> before removal; scene notes recorded")],
    [P("[X]", st_cellb), P("EXH-02 (phone) placed in <b>Faraday/RF-shielded bag</b> to block remote wipe / network")],
    [P("[X]", st_cellb), P("EXH-01 (skimmer) bagged anti-static; battery/power state noted")],
    [P("[X]", st_cellb), P("Write-blocker used for all imaging; originals never mounted RW")],
    [P("[X]", st_cellb), P("SHA-256 computed at acquisition and re-verified before analysis")],
    [P("[X]", st_cellb), P("Tamper-evident seals applied; seal numbers logged above")],
    [P("[X]", st_cellb), P("Analysis performed on working copies only; originals in secure store")],
]
t = Table(chk, colWidths=[10*mm, 170*mm])
t.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),1.5),("BOTTOMPADDING",(0,0),(-1,-1),1.5)]))
E.append(t)

# ---- custody log -------------------------------------------------------
E.append(Paragraph("4. Chain-of-Custody Transfer Log", st_h))
log_head = [P("#", st_cellb), P("Date / Time", st_cellb), P("Released by", st_cellb),
            P("Received by", st_cellb), P("Purpose / Location", st_cellb), P("Signature", st_cellb)]
log_rows = [
    ["1", "2024-11-05 07:30", "[IO Name]", "[IO Name]", "Seizure at scene → evidence bag", ""],
    ["2", "2024-11-05 10:15", "[IO Name]", "Evidence Custodian", "Transport → Cyber FSL intake", ""],
    ["3", "2024-11-05 11:00", "Evidence Custodian", "[Your Name]", "Intake → forensic imaging (write-blocked)", ""],
    ["4", "2024-11-06 09:00", "[Your Name]", "[Your Name]", "Analysis on working copy", ""],
    ["5", "____-__-__ __:__", "[Your Name]", "Evidence Custodian", "Return → secure evidence store", ""],
]
rows = [log_head] + [[P(c) for c in r] for r in log_rows]
t = Table(rows, colWidths=[7*mm, 27*mm, 33*mm, 33*mm, 55*mm, 25*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BOX",(0,0),(-1,-1),0.6,NAVY),("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),
    ("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, GREY]),
]))
E.append(t)

# ---- attestation -------------------------------------------------------
E.append(Spacer(1, 8))
E.append(Paragraph("5. Examiner Attestation", st_h))
E.append(Paragraph(
    "I certify that the evidence described above was handled in accordance with accepted digital-forensic "
    "practice; that working copies were acquired via write-blocker and verified by SHA-256; and that the "
    "integrity of the exhibits was preserved throughout the period of my custody.", st_n))
E.append(Spacer(1, 14))
sig = [[P("________________________"), P("________________________"), P("________________________")],
       [P("Forensic Examiner: [Your Name]", st_cell), P("Investigating Officer: [IO Name]", st_cell), P("Date: [Date]", st_cell)]]
t = Table(sig, colWidths=[60*mm, 60*mm, 60*mm])
t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),1),("BOTTOMPADDING",(0,0),(-1,-1),1)]))
E.append(t)

doc.build(E)
print(f"[+] wrote {OUT.relative_to(REPO)}")
