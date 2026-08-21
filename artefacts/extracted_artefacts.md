# Extracted Artefacts - Operation Phantom Swipe

_Generated 2026-08-21T03:58:35Z by `search_media.py`. Examiner: [Your Name]._

Total artefacts catalogued: **19** (requirement: >= 5).

| ID | Type | Value | Source | Location | Investigative significance |
|----|------|-------|--------|----------|----------------------------|
| ART-001 | Payment card number (PAN) | `4111111111111111` | `evidence/device01_skimmer/captured_tracks.log` | line 4 | Cloned/stolen card harvested by ring; matches network test-PAN format |
| ART-002 | Payment card number (PAN) | `5555555555554444` | `evidence/device01_skimmer/captured_tracks.log` | line 5 | Cloned/stolen card harvested by ring; matches network test-PAN format |
| ART-003 | Payment card number (PAN) | `378282246310005` | `evidence/device01_skimmer/captured_tracks.log` | line 6 | Cloned/stolen card harvested by ring; matches network test-PAN format |
| ART-004 | Payment card number (PAN) | `6011000990139424` | `evidence/device01_skimmer/captured_tracks.log` | line 7 | Cloned/stolen card harvested by ring; matches network test-PAN format |
| ART-005 | Payment card number (PAN) | `3530111333300000` | `evidence/device01_skimmer/captured_tracks.log` | line 8 | Cloned/stolen card harvested by ring; matches network test-PAN format |
| ART-006 | C2 / darknet host | `phantom-swipe.onion` | `evidence/device02_phone/apps/carderpro_config.json` | line 4 | Command-and-control / exfil endpoint for the fraud app |
| ART-007 | Crypto wallet (BTC) | `1PhaNtoMsWiPe000TestOnlyDummyAddr` | `evidence/device02_phone/apps/carderpro_config.json` | line 7 | Receives proceeds from dump sales - money-trail anchor |
| ART-009 | GPS coordinate | `25.276987,55.296249` | `evidence/device02_phone/mail/buyer_deal.eml` | line 11 | Places suspect/withdrawals at ATM & cash-pickup sites |
| ART-010 | GPS coordinate | `28.5632,77.2249` | `evidence/device02_phone/media/photo_metadata.csv` | line 2 | Places suspect/withdrawals at ATM & cash-pickup sites |
| ART-012 | GPS coordinate | `33.865143,35.512142` | `evidence/device02_phone/media/photo_metadata.csv` | line 4 | Places suspect/withdrawals at ATM & cash-pickup sites |
| ART-016 | Reused password (firmware) | `cashout2024` | `evidence/device01_skimmer/skimmer_firmware.bin` | carved string | Same secret guards vault.zip - weak reuse enables crack |
| ART-017 | Crypto wallet (firmware) | `1PhaNtoMsWiPe000TestOnlyDummyAddr` | `evidence/device01_skimmer/skimmer_firmware.bin` | carved string | Ties skimmer hardware to the same money trail |
| ART-018 | Photo EXIF GPS+time | `28.5632,77.2249 @ 2024:11:02 09:12:59` | `evidence/device02_phone/media/photo_metadata.csv` | IMG_2041.jpg | Geotags suspect device at crime scenes/times |
| ART-019 | Photo EXIF GPS+time | `25.276987,55.296249 @ 2024:11:03 18:20:07` | `evidence/device02_phone/media/photo_metadata.csv` | IMG_2042.jpg | Geotags suspect device at crime scenes/times |
| ART-020 | Photo EXIF GPS+time | `33.865143,35.512142 @ 2024:11:04 08:29:44` | `evidence/device02_phone/media/photo_metadata.csv` | IMG_2043.jpg | Geotags suspect device at crime scenes/times |
| ART-021 | Email address | `a1b2c3d4@mail-dummy.test` | `evidence/device02_phone/mail/buyer_deal.eml` | header/body | Links operator to overseas dump buyer |
| ART-022 | Email address | `buyer.dxb@proton-dummy.test` | `evidence/device02_phone/mail/buyer_deal.eml` | header/body | Links operator to overseas dump buyer |
| ART-023 | Email address | `kilo.ops@mail-dummy.test` | `evidence/device02_phone/mail/buyer_deal.eml` | header/body | Links operator to overseas dump buyer |
| ART-024 | Originating IP | `185.220.101.47` | `evidence/device02_phone/mail/buyer_deal.eml` | X-Originating-IP | Network attribution / subpoena target |

## Notes
- All PANs are published network **test** numbers and pass the Luhn checksum, confirming they are well-formed card numbers (not random digits).
- The password carved from firmware (`DUMP_KEY`) is **reused** as the vault.zip password - see the cryptography component.
- GPS points and photo geotags corroborate the SMS/WhatsApp timeline across the India (Connaught Place) and UAE (Dubai) sites, establishing the cross-border element.
