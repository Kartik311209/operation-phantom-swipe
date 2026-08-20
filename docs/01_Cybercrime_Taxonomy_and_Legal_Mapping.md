# Sub-Problem 1 — Cybercrime Classification, Legal Mapping & Taxonomy
### Operation Phantom Swipe — Cross-Border ATM & Credit-Card Fraud Ring

**Examiner:** [Your Name]  **Roll No:** [Roll No]  **Course:** [Course/Subject]  **Institution:** [University]
**Date:** [Date]

> All identifiers in the case data are fabricated for teaching purposes. Card numbers are the published network **test** PANs. This document maps the *conduct* observed in the evidence to statute; it is an academic classification, not a charging decision.

---

## 1. Crimes observed in the scenario

From the seized media (skimmer EXH-01 and operator phone EXH-02) the following distinct criminal acts are identifiable:

1. **ATM skimming** — a physical magnetic-stripe reader + PIN-pad overlay installed on ATMs (`device_config.ini`, `captured_tracks.log`) covertly captured Track-1/Track-2 data and PINs.
2. **Credit/debit card cloning** — captured track data is written onto blank/counterfeit cards, creating false payment instruments (recovered `pan_dump_full.csv`).
3. **Online card fraud (carding)** — stolen PANs/OTPs used for card-not-present purchases and ATM cash-outs (`sms_backup.txt`, `whatsapp_chat.txt`).
4. **Trafficking in stolen card data & skimming devices** — "dumps" sold to an overseas buyer via a darknet-linked app (`carderpro_config.json`, `buyer_deal.eml`).
5. **Unauthorised access / data interception & exfiltration** — skimmer intercepts data in transit and exfiltrates it over Bluetooth to the phone (`bluetooth_pairing.txt`).
6. **Criminal conspiracy / organised cross-border ring** — coordinated roles (installer "Kilo", mules, overseas "Buyer-DXB") across India and the UAE.
7. **Laundering of proceeds** — sale proceeds routed to crypto wallets (`btc_wallet`, `usdt_trc20`).

---

## 2. Legal mapping

### 2.1 Information Technology Act, 2000 (as amended 2008)

| Conduct in scenario | IT Act section | Why it applies |
|---|---|---|
| Skimmer captures card data + exfiltrates over BT; dishonest unauthorised access to data | **s.66** r/w **s.43(a),(b),(i)** | Dishonestly/fraudulently accessing, downloading and extracting data from a computer resource (card chip/ATM interface). |
| Using stolen PAN/CVV/PIN (unique ID features) to transact | **s.66C** (Identity theft) | Fraudulent/dishonest use of another person's *unique identification feature* (card credentials, password/OTP). |
| Online/CNP purchases & phishing banking app impersonating the bank | **s.66D** (Cheating by personation using a computer resource) | Cheating by pretending to be the cardholder/bank through a computer resource. |
| Possessing the operator phone loaded with stolen data & fraud tooling | **s.66B** (Dishonestly receiving stolen computer resource/communication device) | Receiving/retaining a communication device and data known to be stolen. |
| Interception of card data in transit at the ATM interface | **s.66** r/w **s.43** | Covers unauthorised interception/extraction; complements Budapest Art. 3. |
| Breach of cardholder data confidentiality | **s.72 / s.72A** | Disclosure of information/personal data without consent. |
| Attempt & abetment by mules/buyer | **s.84C (attempt), s.84B (abetment)** | Extends liability to attempts and those who abet the offences. |

### 2.2 Indian Penal Code, 1860

| Conduct in scenario | IPC section | Why it applies |
|---|---|---|
| Covertly taking card data / installing device to steal value | **s.378 / s.379** (Theft) | Dishonest taking of movable property (data/funds) without consent. |
| Cloning cards = making a false electronic record/instrument | **s.463, s.465, s.468, s.471** (Forgery; forgery for cheating; using forged document as genuine) | A counterfeit card is a forged document made to cheat and then "used as genuine". |
| Fraudulent transactions inducing banks/merchants to part with money | **s.420** (Cheating and dishonestly inducing delivery of property) | Classic charge for card fraud losses. |
| Cash-out / withdrawals by impersonating the cardholder | **s.419** (Cheating by personation) | Personation to obtain funds. |
| Buying/holding "dumps" and cloned cards | **s.411** (Dishonestly receiving stolen property) | Receiving stolen property (card data/instruments). |
| Coordinated multi-actor ring | **s.120B** (Criminal conspiracy) r/w **s.34** (common intention) | Agreement + concerted action across members/jurisdictions. |

> **Currency note.** The IPC, 1860 has been replaced by the **Bharatiya Nyaya Sanhita (BNS), 2023** (in force 01-Jul-2024). Equivalent BNS provisions: cheating **s.318** (was 420), criminal conspiracy **s.61** (was 120B), theft **s.303** (was 378/379), forgery **s.336/340** (was 465/471), receiving stolen property **s.317** (was 411). The assignment specifies IPC 1860, so the primary mapping above uses IPC; BNS equivalents are noted for completeness.

### 2.3 International instruments — Budapest Convention on Cybercrime (ETS 185, 2001)

| Conduct in scenario | Budapest Article | Why it applies |
|---|---|---|
| Unauthorised access to ATM/card computer resource | **Art. 2** (Illegal access) | Access without right to the system/data. |
| Skimmer intercepting card data in transit | **Art. 3** (Illegal interception) | Non-public transmission of data intercepted by technical means. |
| Altering/writing data to clone cards | **Art. 4** (Data interference) | Damaging/altering/producing data without right. |
| **Manufacturing/possessing/selling the skimmer and card "dumps"** | **Art. 6** (Misuse of devices) | Production, sale, procurement or possession of devices/data designed to commit the above offences — squarely covers skimmer hardware + trafficked dumps. |
| Producing counterfeit cards / false records | **Art. 7** (Computer-related forgery) | Input/alteration of data producing inauthentic data. |
| Fraudulent transactions causing loss for economic gain | **Art. 8** (Computer-related fraud) | Causing loss of property by data manipulation with fraudulent intent. |
| Cross-border evidence & suspect | **Arts. 23–35** (International cooperation: extradition, MLA, 24/7 network, expedited preservation) | Framework for cooperation between India and UAE authorities. |

> **Critical caveat for cross-border cooperation:** **India is not a party to the Budapest Convention** (it has declined to accede, citing concerns over Art. 32b trans-border data access and non-participation in drafting). Consequently, cooperation with a state such as the UAE cannot rely on Budapest machinery and must fall back on **bilateral Mutual Legal Assistance Treaties (MLATs)**, **Letters Rogatory** under **s.166A/166B CrPC**, INTERPOL channels, and platform-specific legal process. This materially slows the investigation (see the main report).

---

## 3. Taxonomy of cybercrimes observed

The ring's activity is classified along four complementary axes. Each leaf is justified by the specific artefact that evidences it.

### 3.1 By offence family (primary taxonomy)

```
Operation Phantom Swipe — Cybercrime Taxonomy
│
├── A. Access & Interception crimes
│   ├── A1 Unauthorised access to card/ATM data      → IT s.66/43; Budapest Art.2
│   └── A2 Illegal interception (skimmer + overlay)   → IT s.66/43; Budapest Art.3
│       └─ evidence: device_config.ini, captured_tracks.log (Track1/2 + PIN keylog)
│
├── B. Integrity / Forgery crimes
│   ├── B1 Data interference (writing clones)         → IPC s.463/468/471; Budapest Art.4/7
│   └── B2 Card cloning = computer-related forgery     → IPC s.465/471; Budapest Art.7
│       └─ evidence: pan_dump_full.csv (PAN+expiry+CVV+PIN, Luhn-valid)
│
├── C. Fraud & Identity crimes
│   ├── C1 Identity theft (PAN/PIN/OTP misuse)         → IT s.66C; Budapest Art.8
│   ├── C2 Cheating by personation (CNP + cash-out)    → IT s.66D; IPC s.419/420
│   └── C3 Phishing banking app (com.fake.hdfcbank)    → IT s.66D; IPC s.420
│       └─ evidence: sms_backup.txt (OTP intercept), installed_apps.txt
│
├── D. Trafficking & Device-misuse crimes
│   ├── D1 Sale of stolen "dumps" to overseas buyer    → IT s.66B; IPC s.411; Budapest Art.6
│   └── D2 Possession/deployment of skimming device    → Budapest Art.6
│       └─ evidence: carderpro_config.json, buyer_deal.eml
│
└── E. Organisational & Proceeds crimes
    ├── E1 Criminal conspiracy (cross-border ring)     → IPC s.120B r/w s.34
    └── E2 Laundering of proceeds (crypto)             → PMLA 2002 (proceeds of crime)
        └─ evidence: btc_wallet / usdt_trc20, buyer_invoice.txt
```

### 3.2 By victim/target

| Target | Crime instances | Evidence |
|---|---|---|
| Individual cardholders | Card data theft, cloning, fund loss | captured_tracks.log, pan_dump_full.csv |
| Financial institutions (HDFC/Axis/ICICI) | Fraud loss, brand impersonation | sms_backup.txt, installed_apps.txt |
| Payment infrastructure (ATMs) | Device tampering, interception | device_config.ini, bluetooth_pairing.txt |

### 3.3 By technique / modus operandi

| Technique | Type | Artefact |
|---|---|---|
| Physical magnetic-stripe skimmer + PIN-pad overlay | Hardware-based interception | device_config.ini |
| Bluetooth exfiltration to collector phone | Wireless data exfiltration | bluetooth_pairing.txt |
| Card cloning onto counterfeit plastic | Forgery | pan_dump_full.csv |
| Card-not-present / OTP-driven online fraud | Application fraud | sms_backup.txt |
| Repackaged phishing banking app | Social-engineering malware | installed_apps.txt |
| Darknet dump marketplace + crypto settlement | Trafficking + laundering | carderpro_config.json, buyer_deal.eml |

### 3.4 By actor role (attribution model)

| Alias | Role | Jurisdiction | Linked artefact |
|---|---|---|---|
| **Kilo** | Installer / operator (self) | India (Delhi) | contacts.vcf, firmware `OPERATOR=Kilo` |
| **Mule-2 (Rohit)** | Cash-out mule | India | sms_backup.txt |
| **Buyer-DXB** | Overseas dump buyer | UAE (Dubai) | buyer_deal.eml, whatsapp_chat.txt |

---

## 4. Justification summary

The scenario is **not a single offence** but a **layered, organised cybercrime enterprise**. Physical device crime (Budapest Art. 6 / IT s.43) feeds forgery (IPC s.465/471 / Budapest Art. 7), which enables fraud (IT s.66C/66D / IPC s.420 / Budapest Art. 8), monetised through trafficking (IT s.66B / IPC s.411) and laundering (PMLA), all bound together by conspiracy (IPC s.120B). The **cross-border** dimension (India ⇄ UAE) is what elevates complexity: it triggers international-cooperation provisions (Budapest Arts. 23–35) that India can only partially invoke because it is **not a Convention party**, forcing reliance on MLATs and Letters Rogatory. This taxonomy directly informs the evidence strategy and the SOP recommendations in the main legal-technical report.
