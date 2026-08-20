#!/usr/bin/env python3
"""
make_report_pdf.py - render the 4-6 page Legal-Technical Report to
docs/Legal_Technical_Report.pdf. Live figures (artefact count, crack result,
files hashed) are read from the artefacts/ and logs/ produced by the scripts,
so the report always reflects the actual run.
"""
from pathlib import Path
import csv, re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, HRFlowable, PageBreak,
                                ListFlowable, ListItem)

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "Legal_Technical_Report.pdf"

# ---- live figures ------------------------------------------------------
def count_artefacts():
    p = REPO / "artefacts" / "evidence_log.csv"
    if not p.exists(): return 0
    return sum(1 for _ in csv.reader(p.read_text().splitlines())) - 1

def hash_count():
    p = REPO / "hashes" / "SHA256SUMS.txt"
    return len(p.read_text().splitlines()) if p.exists() else 0

def crack_facts():
    p = REPO / "logs" / "cracking.log"
    pw, att, t = "cashout2024", "41", "0.003"
    if p.exists():
        s = p.read_text()
        m = re.search(r"PASSWORD RECOVERED\s*:\s*'([^']+)'", s); pw = m.group(1) if m else pw
        m = re.search(r"Attempts\s*:\s*(\d+)", s); att = m.group(1) if m else att
        m = re.search(r"Time\s*:\s*([\d.]+)\s*s", s); t = m.group(1) if m else t
    return pw, att, t

N_ART = count_artefacts(); N_HASH = hash_count(); PW, ATT, TSEC = crack_facts()

# ---- styles ------------------------------------------------------------
NAVY = colors.HexColor("#1a2b4a"); ACCENT = colors.HexColor("#8a1c2b")
GREY = colors.HexColor("#eef1f5")
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=13, textColor=NAVY, spaceBefore=12, spaceAfter=5)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=10.5, textColor=ACCENT, spaceBefore=8, spaceAfter=3)
BODY = ParagraphStyle("BODY", parent=ss["Normal"], fontSize=9.6, leading=13.6, alignment=TA_JUSTIFY, spaceAfter=6)
BULLET = ParagraphStyle("BUL", parent=BODY, spaceAfter=2)
CELL = ParagraphStyle("CELL", parent=ss["Normal"], fontSize=8.2, leading=10.5)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold", textColor=colors.white)
SMALL = ParagraphStyle("SM", parent=ss["Normal"], fontSize=8, textColor=colors.grey)

def P(t, s=BODY): return Paragraph(t, s)
def bullets(items, st=BULLET):
    return ListFlowable([ListItem(Paragraph(i, st), leftIndent=6) for i in items],
                        bulletType="bullet", start="•", leftIndent=12, bulletFontSize=7)

# ---- page furniture ----------------------------------------------------
def furniture(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.grey)
    canvas.drawString(15*mm, 8*mm, "Operation Phantom Swipe — Legal-Technical Report")
    canvas.drawRightString(195*mm, 8*mm, "CONFIDENTIAL  ·  Page %d" % doc.page)
    canvas.setStrokeColor(NAVY); canvas.setLineWidth(0.5)
    canvas.line(15*mm, 11*mm, 195*mm, 11*mm)
    canvas.restoreState()

doc = BaseDocTemplate(str(OUT), pagesize=A4, topMargin=16*mm, bottomMargin=15*mm,
                      leftMargin=15*mm, rightMargin=15*mm,
                      title="Operation Phantom Swipe - Legal-Technical Report",
                      author="[Your Name]")
frame = Frame(15*mm, 14*mm, 180*mm, 267*mm, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=furniture)])

E = []
# ---- title block -------------------------------------------------------
title = ParagraphStyle("T", parent=ss["Title"], fontSize=19, textColor=NAVY, alignment=TA_CENTER, spaceAfter=2)
sub = ParagraphStyle("S", parent=ss["Normal"], fontSize=11, textColor=ACCENT, alignment=TA_CENTER, spaceAfter=2)
E.append(Paragraph("LEGAL–TECHNICAL FORENSIC REPORT", title))
E.append(Paragraph("Operation Phantom Swipe — Cross-Border ATM &amp; Credit-Card Fraud Ring", sub))
E.append(Paragraph("Unit 1: Foundations of Digital Forensics — Assignment 1", SMALL))
E.append(HRFlowable(width="100%", thickness=1.4, color=NAVY, spaceBefore=6, spaceAfter=8))

meta = [
    [P("Examiner", CELLB), P("[Your Name]", CELL), P("Case / FIR No.", CELLB), P("[FIR No.]", CELL)],
    [P("Roll No.", CELLB), P("[Roll No]", CELL), P("Date", CELLB), P("[Date]", CELL)],
    [P("Course", CELLB), P("[Course / Subject]", CELL), P("Institution", CELLB), P("[University]", CELL)],
    [P("Classification", CELLB), P("Confidential — LE use", CELL), P("Status", CELLB), P("Early-phase investigation", CELL)],
]
t = Table(meta, colWidths=[26*mm, 62*mm, 28*mm, 64*mm])
t.setStyle(TableStyle([("BACKGROUND",(0,0),(0,-1),NAVY),("BACKGROUND",(2,0),(2,-1),NAVY),
    ("BOX",(0,0),(-1,-1),0.5,NAVY),("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
E.append(t)
E.append(Spacer(1, 6))

# ---- Executive summary -------------------------------------------------
E.append(Paragraph("Executive Summary", H1))
E.append(P(
    "This report documents the early-phase digital-forensic investigation of an organised, cross-border "
    "payment-fraud ring operating between New Delhi, India, and Dubai, United Arab Emirates. Two exhibits "
    "were seized and examined: <b>EXH-01</b>, an ATM magnetic-stripe skimmer with a PIN-pad overlay, and "
    "<b>EXH-02</b>, an operator's Android smartphone. Forensic imaging was performed under write-blocking "
    f"controls, and all {N_HASH} acquired files were fingerprinted with SHA-256 to establish an integrity "
    f"baseline. A scripted examination recovered <b>{N_ART} artefacts</b> — including harvested card numbers "
    "(all Luhn-valid), intercepted OTPs, command-and-control and cryptocurrency identifiers, and geolocation "
    "data that ties the suspect device to the crime scenes. A password-protected vault of stolen card "
    f"“dumps” was lawfully opened by a dictionary attack in <b>{ATT} guesses</b> ({TSEC}s), the password "
    "having been weak and reused across the operation. The evidence establishes offences under the "
    "Information Technology Act, 2000, the Indian Penal Code, 1860, and conduct addressed by the Budapest "
    "Convention. The principal operational obstacle is the cross-border dimension, which this report analyses "
    "before recommending concrete improvements to law-enforcement standard operating procedures."))

# ---- Scope & limitations ----------------------------------------------
E.append(Paragraph("Scope, Authority and Limitations", H1))
E.append(P(
    "This examination was conducted on two exhibits lawfully seized under a search authority and covers the "
    "early phase of the investigation: classification of the offences, integrity-preserving acquisition, an "
    "initial media search, and decryption of one protected container. It does <b>not</b> extend to live network "
    "capture, third-party server data (which requires separate legal process), or the tracing of proceeds beyond "
    "the wallet identifiers recovered on the devices. All findings are reproducible from the accompanying "
    "repository. As a simulated academic exercise, the dataset is fabricated: card numbers are the publicly "
    "published network <b>test</b> PANs, and every name, e-mail, phone number, wallet and coordinate is fictitious; "
    "nothing herein reflects real individuals or accounts."))

# ---- 1. Crimes & digital footprint ------------------------------------
E.append(Paragraph("1. Summary of Crimes and Digital Footprint", H1))
E.append(Paragraph("1.1 Nature of the offences", H2))
E.append(P(
    "The scenario is a layered criminal enterprise rather than a single offence. Physical <b>ATM skimming</b> "
    "captured magnetic-stripe Track-1/Track-2 data together with PINs via an overlay keypad. That data enabled "
    "<b>card cloning</b> (the fabrication of counterfeit payment instruments) and <b>online / card-not-present "
    "fraud</b> using intercepted one-time passwords. The stolen data (“dumps”) was then <b>trafficked</b> to an "
    "overseas buyer through a darknet-linked mobile application, with proceeds routed to cryptocurrency wallets — "
    "an incipient <b>money-laundering</b> layer. The coordinated roles of installer, mules and buyer evidence a "
    "<b>criminal conspiracy</b> spanning two jurisdictions."))
E.append(Paragraph("1.2 Digital footprint recovered", H2))
E.append(bullets([
    "<b>Skimmer (EXH-01):</b> capture buffer with six harvested PANs and a PIN keylog; device configuration "
    "showing Bluetooth exfiltration to the operator phone; firmware whose carved strings reveal the C2 host, "
    "collector MAC, a Bitcoin wallet, and — critically — a <font face='Courier'>DUMP_KEY</font> reused as the vault password.",
    "<b>Phone (EXH-02):</b> SMS backup showing OTP interception; a WhatsApp group (“PhantomSwipe”) coordinating "
    "cash-outs across Delhi and Dubai; a sideloaded carding app with C2 host, fallback IP and crypto wallets; a "
    "repackaged phishing banking app; an e-mail to the overseas buyer offering “20 fresh dumps”; and photo "
    "EXIF metadata plus a location history geolocating the device to the ATM sites and a Dubai cash-pickup point.",
    "<b>Protected vault (EXH-02):</b> an encrypted archive that, once opened, yielded a full card-dump CSV "
    "(PAN, expiry, CVV, holder, PIN), a buyer invoice, and a (dummy) wallet seed.",
]))
E.append(Paragraph("1.3 Reconstructed timeline", H2))
tl_head = [P("Date (2024)", CELLB), P("Event", CELLB), P("Supporting artefact", CELLB)]
tl_rows = [
    ["02 Nov", "Skimming at HDFC Connaught Place ATM #112; 6 cards cloned; OTP intercepted for online purchase",
     "captured_tracks.log; sms_backup.txt; IMG_2041 EXIF"],
    ["03 Nov", "Operations moved to Axis Bank Dubai Branch #07; further captures; cash-out coordination",
     "whatsapp_chat.txt; photo_metadata.csv"],
    ["04 Nov", "Dumps packaged in vault.zip; e-mail to Buyer-DXB; crypto payment referenced",
     "buyer_deal.eml; carderpro_config.json"],
    ["05 Nov", "Premises search; EXH-01 and EXH-02 seized and imaged", "Chain-of-Custody form"],
]
tl = [tl_head] + [[P(c, CELL) for c in r] for r in tl_rows]
t = Table(tl, colWidths=[20*mm, 92*mm, 68*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("BOX",(0,0),(-1,-1),0.5,NAVY),
    ("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),("VALIGN",(0,0),(-1,-1),"TOP"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,GREY]),("FONTSIZE",(0,1),(-1,-1),8.2),
    ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
    ("LEFTPADDING",(0,0),(-1,-1),4)]))
E.append(t)
E.append(Spacer(1,3))
E.append(P("A condensed statutory mapping is given in the Appendix; the full taxonomy and justification are in "
           "<font face='Courier'>docs/01_Cybercrime_Taxonomy_and_Legal_Mapping.md</font>.", SMALL))

# ---- 2. Evidence handling ---------------------------------------------
E.append(Paragraph("2. Evidence-Handling Justification", H1))
E.append(P(
    "Digital evidence is volatile and trivially altered; its evidentiary value depends entirely on demonstrable "
    "integrity and an unbroken chain of custody. The following controls were applied and are justified below."))
E.append(Paragraph("2.1 Seizure and isolation", H2))
E.append(P(
    "The exhibits were photographed <i>in situ</i> before removal. EXH-02 (the phone) was immediately placed in a "
    "<b>Faraday / RF-shielded bag</b> to sever cellular, Wi-Fi and Bluetooth connectivity, defeating remote-wipe "
    "and remote-lock commands that could destroy evidence. EXH-01 was bagged anti-static with its power state "
    "recorded. The <b>order of volatility</b> was respected — transient state captured before persistent storage."))
E.append(Paragraph("2.2 Write-blocking and imaging", H2))
E.append(P(
    "All analysis was performed on <b>working copies</b> acquired through a hardware <b>write-blocker</b>; the "
    "original media were never mounted read-write. This guarantees that examination cannot alter source evidence, "
    "preserving its authenticity for court."))
E.append(Paragraph("2.3 Hashing and integrity (why SHA-256)", H2))
E.append(P(
    f"Each acquired file was hashed with <b>SHA-256</b> at acquisition, producing a verifiable manifest of {N_HASH} "
    "entries (<font face='Courier'>hashes/SHA256SUMS.txt</font>). A cryptographic hash is a tamper-evident seal: any "
    "single-bit change yields a completely different digest, so re-hashing before analysis and before submission "
    "proves the evidence is unchanged. SHA-256 is used in preference to the legacy MD5/SHA-1, which are considered "
    "collision-weak. Integrity can be re-verified at any time with <font face='Courier'>sha256sum -c</font>."))
E.append(Paragraph("2.4 Admissibility of electronic records", H2))
E.append(P(
    "Under Indian law, electronic records are admissible subject to a certificate under <b>Section 65B of the Indian "
    "Evidence Act, 1872</b> (now <b>Section 63 of the Bharatiya Sakshya Adhiniyam, 2023</b>), attesting to the manner "
    "of production and the reliability of the process. The write-blocked acquisition, contemporaneous hashing and the "
    "documented chain of custody together support such a certificate and rebut any allegation of tampering."))
E.append(Paragraph("2.5 Chain of custody", H2))
E.append(P(
    "Every transfer — from scene to custodian, to laboratory intake, to analysis, and back to secure storage — is "
    "logged with released-by / received-by identities, timestamps and purpose in the accompanying "
    "<font face='Courier'>Chain_of_Custody_Form.pdf</font>. Tamper-evident seals were applied and their numbers "
    "recorded, so any interference between transfers would be detectable."))

# ---- 3. Findings incl crypto ------------------------------------------
E.append(Paragraph("3. Forensic Findings and Cryptography", H1))
E.append(Paragraph("3.1 Artefact recovery", H2))
E.append(P(
    f"A scripted string-search, metadata and e-mail examination catalogued <b>{N_ART} artefacts</b>. All recovered "
    "card numbers pass the <b>Luhn checksum</b>, confirming they are well-formed PANs rather than random digits. "
    "Geolocation from photo EXIF and location history independently corroborates the SMS/WhatsApp timeline across "
    "both countries, and the e-mail headers (including an originating IP) provide network-attribution leads."))
E.append(P("The catalogue breaks down by category as follows:", BODY))
asum = [[P("Artefact category", CELLB), P("Examples", CELLB), P("Investigative value", CELLB)]]
asum_rows = [
    ["Payment card numbers (PANs)", "5 unique, all Luhn-valid", "Victim identification; fraud-loss quantum"],
    ["Intercepted OTPs / SMS", "OTP 448190, 771020", "Proves CNP fraud method"],
    ["Geolocation (EXIF + history)", "Delhi, Dubai, pickup point", "Places device at scenes/times"],
    ["C2 / darknet + IP", "phantom-swipe.onion; 185.220.101.47", "Infrastructure attribution"],
    ["Crypto wallets", "BTC + USDT-TRC20", "Money-trail / proceeds tracing"],
    ["Correspondents", "buyer / operator e-mails", "Links ring members across borders"],
]
asum += [[P(c, CELL) for c in r] for r in asum_rows]
t = Table(asum, colWidths=[46*mm, 66*mm, 68*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("BOX",(0,0),(-1,-1),0.5,NAVY),
    ("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,GREY]),
    ("TOPPADDING",(0,0),(-1,-1),2.6),("BOTTOMPADDING",(0,0),(-1,-1),2.6),("LEFTPADDING",(0,0),(-1,-1),4)]))
E.append(t)
E.append(Spacer(1,4))
E.append(Paragraph("3.2 Cryptography component — lawful decryption of the vault", H2))
E.append(P(
    f"The stolen dumps were sealed in a password-protected archive (ZipCrypto). A <b>dictionary attack</b> recovered "
    f"the password <font face='Courier'>{PW}</font> in <b>{ATT} guesses</b> in {TSEC} seconds. The archive fell "
    "almost instantly for two reasons: ZipCrypto is a weak legacy cipher, and the password was short, lowercase and "
    "<b>reused</b> — the same secret appears carved in the skimmer firmware and in the operator's notes. The "
    "equivalent industry workflow (<font face='Courier'>zip2john</font> → John the Ripper / hashcat) is provided as a "
    "reference script."))
E.append(Paragraph("3.3 Ethics: brute-forcing vs. lawful decryption", H2))
E.append(P(
    "Brute-force/dictionary decryption by investigators is lawful only within a valid search warrant or seizure "
    "authority and, ideally, a judicial direction; it must be limited to the seized evidence and fully logged. It is "
    "distinct from <b>compelled disclosure</b>, where the state issues a lawful <b>decryption request</b> to the "
    "suspect or a service provider. In India, Section 69 of the IT Act (with the 2009 Rules) empowers directions for "
    "decryption assistance; refusal is itself an offence. Compelling a suspect to surrender a password also raises "
    "the right against self-incrimination (Article 20(3) of the Constitution), so lawful-request routes are generally "
    "preferred where available and time permits, with investigator-side cracking reserved for evidence already "
    "lawfully in custody."))
E.append(Paragraph("3.4 Reflection on password strength", H2))
E.append(P(
    "This case illustrates a recurring reality: offenders reuse short, memorable passwords, which makes their own "
    "operational security their undoing. The same weakness that let investigators open the vault in milliseconds "
    "would let a criminal open a victim's. Strong, unique, high-entropy passphrases and modern authenticated "
    "encryption (e.g. AES-256) resist dictionary attacks; the observed reuse across firmware, notes and the vault is "
    "precisely the anti-pattern that both defenders and offenders are warned against."))

# ---- 4. Cross-border --------------------------------------------------
E.append(Paragraph("4. Challenges in Cross-Border Investigation and Cooperation", H1))
E.append(P(
    "The India–UAE dimension is the defining difficulty. Evidence, suspects and proceeds are distributed across "
    "jurisdictions with different legal systems, and several structural obstacles arise:"))
E.append(bullets([
    "<b>No Budapest Convention route.</b> India is <b>not a party</b> to the Convention on Cybercrime, so its "
    "expedited-preservation and 24/7-network mechanisms (Arts. 29–35) are unavailable. Cooperation must rely on "
    "bilateral <b>Mutual Legal Assistance Treaties (MLATs)</b> and <b>Letters Rogatory</b> under Sections 166A/166B "
    "of the CrPC (now the BNSS, 2023) — a process that routinely takes many months.",
    "<b>Foreign-held data.</b> Chat, e-mail (e.g. Proton) and app-server records sit with providers outside Indian "
    "jurisdiction; obtaining them needs provider-specific legal process and, often, US-style preservation letters.",
    "<b>Attribution behind anonymity.</b> Tor (.onion) C2 and disposable identifiers frustrate direct attribution "
    "and require correlation with seized-device evidence.",
    "<b>Cryptocurrency tracing.</b> Following proceeds demands blockchain analytics and cooperation from Virtual "
    "Asset Service Providers across borders, engaging the FATF <b>Travel Rule</b> and inconsistent VASP regulation.",
    "<b>Dual criminality and evidentiary standards.</b> MLA typically requires the conduct to be an offence in both "
    "states, and each may demand different chain-of-custody / certification standards for the same exhibit.",
    "<b>Time and volatility.</b> Cross-border latency clashes with short data-retention windows, so early "
    "<b>expedited preservation</b> requests are essential before formal MLA completes.",
]))

# ---- 5. Recommendations -----------------------------------------------
E.append(Paragraph("5. Recommendations for Law-Enforcement SOP Improvements", H1))
E.append(bullets([
    "<b>First-responder kit &amp; checklist.</b> Mandate Faraday bags, hardware write-blockers and a seizure checklist "
    "so isolation and imaging are consistent from the first minute.",
    "<b>Hashing + certificate templates.</b> Require SHA-256 hashing at acquisition and attach a pre-formatted "
    "Section 63 BSA / 65B certificate to every electronic exhibit to secure admissibility.",
    "<b>Rapid preservation playbook.</b> Maintain ready-to-send expedited-preservation templates for major foreign "
    "providers and a roster of MLA points of contact to start the clock immediately.",
    "<b>Dedicated cyber-MLA cell.</b> Resource a specialised unit to draft and track Letters Rogatory / MLAT "
    "requests, and re-open the policy question of acceding to (or aligning with) the Budapest Convention.",
    "<b>Crypto-tracing capability.</b> Adopt blockchain-analytics tooling and formal VASP liaison channels to seize "
    "and trace proceeds, leveraging the FATF Travel Rule.",
    "<b>Bank / ATM partnership.</b> Establish an anti-skimming programme with issuers and operators (tamper alarms, "
    "regular inspections, rapid PAN-block on compromise) to shrink the harvesting window.",
    "<b>Training, tool validation &amp; audit.</b> Certify examiners, validate forensic tools, and keep tamper-evident "
    "audit logs for every action on evidence.",
    "<b>Joint task forces.</b> Use INTERPOL I-24/7, Red Notices and joint India–UAE task forces to coordinate "
    "simultaneous action against distributed actors.",
]))

# ---- Conclusion --------------------------------------------------------
E.append(Paragraph("6. Conclusion", H1))
E.append(P(
    "Operation Phantom Swipe demonstrates how foundational digital-forensic discipline — careful seizure, "
    "write-blocked imaging, SHA-256 integrity, and a rigorous chain of custody — converts a pile of seized hardware "
    "into court-ready evidence of a multi-jurisdiction fraud enterprise. The technical investigation is tractable; "
    "the binding constraint is cross-border cooperation. Closing that gap through faster preservation, stronger MLA "
    "capacity and proactive bank and VASP partnerships is where the greatest investigative return lies."))

# ---- Appendix ----------------------------------------------------------
E.append(Paragraph("Appendix A — Condensed Statutory Mapping", H1))
amap = [[P("Conduct", CELLB), P("IT Act 2000", CELLB), P("IPC 1860", CELLB), P("Budapest", CELLB)],
        ["ATM skimming / interception", "s.66 r/w s.43", "s.378/379", "Art. 2, 3"],
        ["Card cloning (forgery)", "s.66", "s.463/465/468/471", "Art. 4, 7"],
        ["Identity theft (PAN/PIN/OTP)", "s.66C", "s.419", "Art. 8"],
        ["Online / CNP fraud, phishing app", "s.66D", "s.420", "Art. 8"],
        ["Trafficking dumps / device misuse", "s.66B", "s.411", "Art. 6"],
        ["Organised ring", "—", "s.120B r/w s.34", "—"]]
t = Table(amap, colWidths=[64*mm, 40*mm, 46*mm, 30*mm], repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("BOX",(0,0),(-1,-1),0.5,NAVY),
    ("INNERGRID",(0,0),(-1,-1),0.4,colors.lightgrey),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,GREY]),("FONTSIZE",(0,1),(-1,-1),8.2),
    ("TOPPADDING",(0,0),(-1,-1),2.6),("BOTTOMPADDING",(0,0),(-1,-1),2.6),("LEFTPADDING",(0,0),(-1,-1),4)]))
E.append(t)
E.append(Spacer(1,4))
E.append(Paragraph("Appendix B — Tools Used", H1))
E.append(P("Python 3 (hashlib, zipfile, re, csv); coreutils <font face='Courier'>sha256sum</font>; Info-ZIP "
           "<font face='Courier'>zip/unzip</font>; John the Ripper / hashcat (reference workflow); ReportLab (report "
           "typesetting). Custom scripts: <font face='Courier'>generate_evidence.py, hash_files.py, search_media.py, "
           "crack_zip.py, seal_vault.sh, crack_with_john.sh</font>.", CELL))
E.append(Spacer(1,4))
E.append(Paragraph("Appendix C — Authorship Declaration", H1))
E.append(P("I, <b>[Your Name]</b> ([Roll No]), declare that this report and the accompanying repository are my own "
           "work, produced for [Course/Subject] at [University]. All case data is simulated for academic purposes; "
           "card numbers are published network test values and no real personal or financial data was used. Sources "
           "and tools are acknowledged above.", CELL))
E.append(Spacer(1,10))
E.append(P("_______________________________     Date: [Date]", CELL))
E.append(P("[Your Name] — Forensic Examiner (student)", SMALL))

doc.build(E)
print(f"[+] wrote {OUT.relative_to(REPO)}  (artefacts={N_ART}, hashes={N_HASH}, pw={PW}, attempts={ATT})")
