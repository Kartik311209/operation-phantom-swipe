#!/usr/bin/env python3
"""
generate_evidence.py
Operation Phantom Swipe - Simulated Evidence Generator
-------------------------------------------------------
Creates a reproducible set of DUMMY seized-device media for a digital-forensics
teaching exercise. NOTHING here is real: card numbers are the publicly published
network *test* PANs, all names/emails/phones/wallets/GPS points are fabricated.

Two seized exhibits are simulated:
  EXH-01  : an ATM magnetic-stripe skimmer (embedded device dump)
  EXH-02  : a mule/operator Android phone (logical file-system extract)

It also stages the plaintext that will be sealed inside the password-protected
vault (evidence/protected/vault.zip). The plaintext staging dir (_build_src) is
NOT committed - only the encrypted zip ships, exactly as an investigator would
receive it.

Usage:  python3 scripts/generate_evidence.py
"""
from pathlib import Path
import json
import textwrap
import struct

# ---------------------------------------------------------------- paths
REPO = Path(__file__).resolve().parents[1]
SKIMMER = REPO / "evidence" / "device01_skimmer"
PHONE   = REPO / "evidence" / "device02_phone"
APPS    = PHONE / "apps"
MEDIA   = PHONE / "media"
MAIL    = PHONE / "mail"
VAULT_SRC = REPO / "_build_src" / "vault"          # sealed into vault.zip later
for d in (SKIMMER, APPS, MEDIA, MAIL, VAULT_SRC):
    d.mkdir(parents=True, exist_ok=True)

def w(path: Path, text: str):
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    print(f"  [+] {path.relative_to(REPO)}")

# ==================================================================
# EXHIBIT 01 - ATM SKIMMER (embedded device)
# ==================================================================
print("[*] Generating EXH-01 (skimmer) ...")

# 1. Captured magnetic-stripe track data (the core loot).
#    PANs below are the PUBLISHED test card numbers of each network - they are
#    designed for testing and are NOT valid for real transactions.
w(SKIMMER / "captured_tracks.log", """
    # PHANTOM-SKIMMER v2 capture buffer  (offsets = read order)
    # Format:  %B<PAN>^<LAST>/<FIRST>^<YYMM><svc>?  ;<PAN>=<YYMM><svc>?
    # ---- All PANs are network TEST numbers (dummy) ----
    2024-11-02T09:14:22Z ATM=HDFC_CP_112 TRK1=%B4111111111111111^DOE/JOHN^2609101?  TRK2=;4111111111111111=26091010000000000?
    2024-11-02T09:41:07Z ATM=HDFC_CP_112 TRK1=%B5555555555554444^MEHTA/RITA^2711201?  TRK2=;5555555555554444=27112010000000000?
    2024-11-02T11:03:55Z ATM=HDFC_CP_112 TRK1=%B378282246310005^KHAN/AMIR^2508101?    TRK2=;378282246310005=25081010000000000?
    2024-11-03T18:22:41Z ATM=AXIS_DXB_07 TRK1=%B6011000990139424^SINGH/PRIYA^2610201? TRK2=;6011000990139424=26102010000000000?
    2024-11-03T19:57:12Z ATM=AXIS_DXB_07 TRK1=%B3530111333300000^LEE/DAVID^2504101?   TRK2=;3530111333300000=25041010000000000?
    2024-11-04T08:30:00Z ATM=AXIS_DXB_07 TRK1=%B4111111111111111^DOE/JOHN^2609101?    TRK2=;4111111111111111=26091010000000000?
    # PIN pad overlay keylog (paired to PAN by timestamp):
    KEYLOG 2024-11-02T09:14:25Z PAN=4111111111111111 PIN=4517
    KEYLOG 2024-11-02T09:41:10Z PAN=5555555555554444 PIN=8890
    KEYLOG 2024-11-03T18:22:44Z PAN=6011000990139424 PIN=1122
""")

# 2. Device configuration (exfil path -> the phone, Bluetooth pairing).
w(SKIMMER / "device_config.ini", """
    [device]
    model        = PHANTOM-SKIMMER v2
    fw_version   = 2.3.1-mod
    serial       = PS2-000734
    installed_at = HDFC Connaught Place ATM #112 ; Axis Bank Dubai Branch #07

    [exfil]
    mode            = bluetooth
    collector_name  = GalaxyM32-OP
    collector_mac   = 44:80:EB:9F:1C:7A          ; == EXH-02 phone BT MAC
    dump_interval_h = 12
    autowipe        = false

    [pinpad_overlay]
    enabled   = true
    keymap    = 3x4-default
    store_pin = true
""")

# 3. Bluetooth pairing table (links skimmer <-> phone).
w(SKIMMER / "bluetooth_pairing.txt", """
    PAIRED DEVICES (skimmer BT stack)
    ---------------------------------
    44:80:EB:9F:1C:7A   GalaxyM32-OP     trusted   last=2024-11-04T08:31Z
    A0:1D:48:22:9E:00   PS2-000734       self
""")

# 4. Firmware blob: real binary bytes with recoverable ASCII strings inside,
#    so a `strings`/string-search demo has something to surface.
fw = bytearray()
fw += b"\x7fELF" + bytes(60)                       # fake ELF-ish header
hidden = [
    b"PHANTOM-SKIMMER v2.3.1-mod build 20240915",
    b"C2_HOST=phantom-swipe[.]onion",
    b"BT_COLLECTOR=44:80:EB:9F:1C:7A",
    b"DUMP_KEY=cashout2024",                        # <-- same as vault password (weak reuse!)
    b"OPERATOR=Kilo",
    b"WALLET_BTC=1PhaNtoMsWiPe000TestOnlyDummyAddr",
]
for i, s in enumerate(hidden):
    fw += struct.pack("<I", 0xDEAD0000 + i) + s + b"\x00"
    fw += bytes((i * 37) % 251 for _ in range(48))  # filler bytes
(SKIMMER / "skimmer_firmware.bin").write_bytes(bytes(fw))
print(f"  [+] evidence/device01_skimmer/skimmer_firmware.bin ({len(fw)} bytes)")

# ==================================================================
# EXHIBIT 02 - OPERATOR PHONE (logical extract)
# ==================================================================
print("[*] Generating EXH-02 (phone) ...")

# 5. SMS backup - OTP interception + drop coordination.
w(PHONE / "sms_backup.txt", """
    # Android SMS logical extract (com.android.providers.telephony)
    2024-11-02 09:15 | +91-98XXXX2210  | INBOX | HDFCBK: OTP 448190 for txn of INR 49,999 at AMZ. Do not share.
    2024-11-02 09:16 | Kilo            | SENT  | got 448190, pushing the amz order now
    2024-11-03 18:23 | +91-90XXXX8841  | INBOX | ICICI: 6011 card used AED 3,500 DXB. OTP 771020
    2024-11-03 18:24 | Buyer-DXB       | SENT  | tracks landed, sending 20 dumps tonight. usual split
    2024-11-04 08:35 | Kilo            | SENT  | skimmer dump pulled over BT, uploading to vault
    2024-11-04 21:10 | Mule-2          | INBOX | 3 cards declined at CP, switching to Dubai ATMs
""")

# 6. WhatsApp export - cross-border ring chatter.
w(PHONE / "whatsapp_chat.txt", """
    # WhatsApp export - group "PhantomSwipe" (com.whatsapp)
    [02/11/2024, 09:20:11] Kilo: cloned 6 cards today at CP. tracks in captured_tracks.log
    [02/11/2024, 09:21:40] Buyer-DXB: send dumps to my proton. price 12$ each for platinum
    [03/11/2024, 18:40:02] Kilo: moving ops to Dubai branch 07, cameras blind on left lane
    [03/11/2024, 18:41:19] Mule-2: withdrawing at 33.865143,35.512142 then 25.276987,55.296249
    [04/11/2024, 08:36:55] Kilo: everything zipped in vault.zip pass is the usual dump key
    [04/11/2024, 08:37:30] Buyer-DXB: crypto sent to 1PhaNtoMsWiPe000TestOnlyDummyAddr
""")

# 7. Contacts (aliases -> phones/emails).
w(PHONE / "contacts.vcf", """
    BEGIN:VCARD
    VERSION:3.0
    FN:Buyer DXB
    TEL;TYPE=CELL:+971-5X-XXX-4417
    EMAIL:buyer.dxb@proton-dummy.test
    END:VCARD
    BEGIN:VCARD
    VERSION:3.0
    FN:Mule-2 (Rohit)
    TEL;TYPE=CELL:+91-90XXXX8841
    END:VCARD
    BEGIN:VCARD
    VERSION:3.0
    FN:Kilo (self)
    TEL;TYPE=CELL:+91-98XXXX2210
    EMAIL:kilo.ops@mail-dummy.test
    END:VCARD
""")

# 8. Installed-apps inventory (fraud tooling stands out).
w(APPS / "installed_apps.txt", """
    # pm list packages -f  (trimmed logical extract)
    com.whatsapp                         2.24.10.85
    com.android.chrome                   129.0
    com.phantom.carderpro                1.4        <-- non-Play sideload (carding tool)
    com.fake.hdfcbank                     3.0        <-- repackaged phishing banking app
    org.torproject.android               17.2       (Orbot)
    com.bluetooth.dumpsync               0.9        <-- pulls skimmer dumps over BT
""")

# 9. Fraud-app config (C2 + wallets + PAN sink).
w(APPS / "carderpro_config.json", json.dumps({
    "app": "com.phantom.carderpro",
    "version": "1.4",
    "c2_host": "phantom-swipe.onion",
    "c2_fallback": "185.220.101.47",
    "operator_id": "Kilo",
    "btc_wallet": "1PhaNtoMsWiPe000TestOnlyDummyAddr",
    "usdt_trc20": "TPhantoMsWipeTestOnlyDummyAddr0",
    "pan_sink_file": "/sdcard/Android/data/com.phantom.carderpro/dumps.csv",
    "buyer_contact": "buyer.dxb@proton-dummy.test",
    "dump_price_usd": 12
}, indent=2) + "\n")
print("  [+] evidence/device02_phone/apps/carderpro_config.json")

# 10. Email export (.eml) - deal with overseas buyer.
w(MAIL / "buyer_deal.eml", """
    From: Kilo <kilo.ops@mail-dummy.test>
    To: Buyer DXB <buyer.dxb@proton-dummy.test>
    Subject: 20 fresh dumps - CP + DXB batch
    Date: Mon, 04 Nov 2024 08:45:03 +0530
    Message-ID: <a1b2c3d4@mail-dummy.test>
    X-Originating-IP: [185.220.101.47]

    Batch ready. 6 platinum + 14 classic, all with PIN.
    Sample PAN 4111111111111111 exp 2609. Full set in vault.zip (pass = dump key).
    Send 50% to 1PhaNtoMsWiPe000TestOnlyDummyAddr, rest on delivery.
    Meet coords for cash pickup: 25.276987,55.296249 (Dubai) Thu 20:00.
    - K
""")

# 11. Location history (Google-style) - GPS artefacts.
loc = {"locations": [
    {"timestampMs": "1730531662000", "latE7": 285632000, "lngE7": 772249000,
     "note": "HDFC Connaught Place ATM #112, New Delhi"},
    {"timestampMs": "1730656961000", "latE7": 252769870, "lngE7": 552962490,
     "note": "Axis Bank Dubai Branch #07"},
    {"timestampMs": "1730660000000", "latE7": 338651430, "lngE7": 355121420,
     "note": "cash pickup point"},
]}
w(MEDIA / "location_history.json", json.dumps(loc, indent=2) + "\n")

# 12. Photo EXIF-style metadata sidecar (GPS per image, no binary needed).
w(MEDIA / "photo_metadata.csv", """
    filename,datetime_original,make,model,gps_lat,gps_lon
    IMG_2041.jpg,2024:11:02 09:12:59,samsung,SM-M325F,28.5632,77.2249
    IMG_2042.jpg,2024:11:03 18:20:07,samsung,SM-M325F,25.276987,55.296249
    IMG_2043.jpg,2024:11:04 08:29:44,samsung,SM-M325F,33.865143,35.512142
""")

# 13. Operator notes - target ATM list.
w(PHONE / "notes.txt", """
    TODO / TARGETS
    - CP HDFC #112  (done x6)   -> move before cams reset Fri
    - Dubai Axis #07 (done x2)  -> best 6-9pm, left lane blind
    - Karol Bagh SBI #* (scout) -> pending overlay fit
    - remember: dump key = cashout2024   (reuse for vault + firmware)
""")

# ==================================================================
# VAULT PLAINTEXT (staged -> will be sealed into vault.zip, then deleted)
# ==================================================================
print("[*] Staging protected-vault plaintext (not committed) ...")
w(VAULT_SRC / "pan_dump_full.csv", """
    pan,expiry,cvv,holder,network,pin
    4111111111111111,2609,123,JOHN DOE,VISA,4517
    5555555555554444,2711,456,RITA MEHTA,MASTERCARD,8890
    378282246310005,2508,1234,AMIR KHAN,AMEX,0000
    6011000990139424,2610,789,PRIYA SINGH,DISCOVER,1122
    3530111333300000,2504,321,DAVID LEE,JCB,0000
""")
w(VAULT_SRC / "buyer_invoice.txt", """
    INVOICE - dumps batch 2024-11-04
    20 dumps @ $12  = $240
    BTC 1PhaNtoMsWiPe000TestOnlyDummyAddr
    50% advance, 50% on delivery. Buyer: buyer.dxb@proton-dummy.test
""")
w(VAULT_SRC / "wallet_seed.txt", """
    # DUMMY seed phrase (NOT a real wallet)
    phantom swipe test only dummy never use ledger sample invalid seed words here
""")

print("\n[DONE] Evidence generated. Vault plaintext staged in _build_src/ (seal with seal_vault.sh).")
