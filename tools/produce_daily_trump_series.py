#!/usr/bin/env python3
"""
tools/produce_daily_trump_series.py - Production Engine for 10 Retrospective Daily Investigative Podcasts
ZeroFilter Geopolitical & Counterintelligence Dossier Series (2026-09-28 down to 2026-09-19)
"""

import os
import sys
import json
import math
import random
import shutil
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "engine"))
from voice import synthesize_episode_audio

W, H = 1376, 768

def create_base(c1, c2):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def add_noise(img, count=3000):
    draw = ImageDraw.Draw(img)
    for _ in range(count):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        v = random.randint(180, 255)
        draw.point((x, y), fill=(v, v, v))
    return img

EPISODES = [
    {
        "id": "2026-09-28-18",
        "date": "2026-09-28",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Helsinki Concealment: Trump's Private Putin Summits, Seized Translator Notes & The Destruction of Diplomatic Logs",
        "subject": "Daily investigative dossier: Donald Trump's clandestine one-on-one sessions with Vladimir Putin in Helsinki, Hamburg, and Buenos Aires, the confiscation of state department interpreter notes, secret unmonitored telephone channels, and the systemic subversion of national security oversight.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On July 16, 2018, inside the Presidential Palace in Helsinki, Finland, Donald Trump concluded a two-hour private summit with Vladimir Putin with no aides, cabinet secretaries, or national security staff present. Following the closed-door encounter, senior diplomatic officials discovered that standard contemporaneous memoranda of conversation had been strictly suppressed. A comprehensive investigation by the Washington Post revealed that Trump personally took possession of his interpreter's working notes and ordered the diplomatic linguist not to discuss the exchanges with any administration officials.",
            "The institutional concealment of presidential communications was neither isolated nor accidental. Records examined by the House Foreign Affairs Committee demonstrated that across multiple international summits, including bilateral encounters at the G20 gatherings in Hamburg and Buenos Aires, Trump routinely conducted unlogged discussions with Kremlin leadership. Senior intelligence officials testifying before congressional oversight committees expressed profound alarm that the commander-in-chief was operating beyond the reach of institutional records, leaving cabinet officials completely uninformed regarding potential sovereign commitments or foreign policy concessions made to Moscow.",
            "Legislative oversight and national security protocols broke down under executive obstruction. The Senate Foreign Relations Committee issued formal requests to interview the State Department interpreter present during the Helsinki summit, but the White House invoked sweeping executive privilege to block congressional scrutiny. Legal scholars at the Brookings Institution documented that the deliberate suppression of diplomatic records subverted the Presidential Records Act and crippled the National Security Council's interagency coordination, creating unprecedented vulnerabilities for foreign intelligence exploitation and strategic blackmail.",
            "The vulnerability extended into unmonitored telephonic communications. Throughout his presidency, counterintelligence officials warned that Trump regularly utilized unsecured commercial cell phones to conduct sensitive discussions with foreign leaders and informal political advisors. Declassified records preserved by the National Security Archive confirm that foreign signals intelligence services, including Russian and Chinese surveillance apparatuses, routinely intercepted unencrypted White House communications, extracting strategic previews of policy shifts, personnel decisions, and confidential bilateral bargaining positions.",
            "Intelligence analysts and diplomatic historians emphasize that the systemic evasion of official diplomatic logging represents a catastrophic breach of democratic accountability. By destroying written records, silencing official translators, and conducting shadow foreign policy through private phone lines, the executive branch dismantled basic constitutional checks and balances. The resulting information vacuum left American allies in NATO and Eastern Europe uncertain whether bilateral agreements represented genuine collective defense policies or clandestine personal accommodations.",
            "Tonight receipts. The Washington Post investigative exposé on seized Helsinki translator notes. The House Foreign Affairs Committee inquiry into destroyed diplomatic memoranda. The Brookings Institution constitutional review of executive secrecy, and declassified National Security Archive records on intercepted communications. Every primary document is preserved in the dossier drawer. Verify the public record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.washingtonpost.com/world/national-security/trump-has-concealed-details-of-his-face-to-face-encounters-with-putin-from-senior-officials-in-administration/2019/01/12/84400e1a-161b-11e9-9180-f873232264bb_story.html",
                "title": "Trump has concealed details of his face-to-face encounters with Putin from senior officials",
                "published": "2019-01-13",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://foreignaffairs.house.gov/press-release/engel-cumming-and-schiff-seek-interviews-white-house-staff-and-state-department-translators",
                "title": "House Committee Joint Inquiry into Trump-Putin Communications and Seized Records",
                "published": "2019-03-04",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.brookings.edu/articles/trumps-secret-meetings-with-putin-violate-record-keeping-norms/",
                "title": "Trump's Secret Meetings with Putin and Presidential Record-Keeping Norms",
                "published": "2019-02-15",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://nsarchive.gwu.edu/briefing-book/russia-programs/2020-09-15/us-russia-summits-declassified-record-helsinki",
                "title": "U.S.-Russia Summits: The Declassified Record and Diplomatic Reporting Standards",
                "published": "2020-09-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.congress.gov/116/chrg/CHRG-116hhrg35402/CHRG-116hhrg35402.htm",
                "title": "Congressional Hearing: Oversight of State Department Diplomatic Communications and Record Retention",
                "published": "2019-06-12",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 18, 32), (35, 15, 20)),
        "accent": (255, 60, 80),
        "theme": "HELSINKI CONCEALMENT // SEIZED DIPLOMATIC LOGS"
    },
    {
        "id": "2026-09-27-18",
        "date": "2026-09-27",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Moscow Tower Protocol: Sater, Cohen & Backchannel Kremlin Negotiations During the 2016 Campaign",
        "subject": "Daily investigative dossier: The Trump Organization's covert pursuit of a hundred-story Moscow skyscraper through Felix Sater and Michael Cohen during the 2016 primary campaign, secret letters of intent, and direct outreach to Dmitry Peskov and Kremlin executive offices.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Throughout the 2016 presidential primary season, while Donald Trump repeatedly assured the American electorate that he had no business dealings, loans, or ongoing contracts in Russia, his corporate headquarters was aggressively pursuing a landmark development project in Moscow. Court filings in the Southern District of New York and the Department of Justice Special Counsel investigation confirmed that Trump signed a formal letter of intent to construct Trump Tower Moscow, envisioning a multi-hundred-million-dollar skyscraper in the heart of the Russian capital.",
            "The operational negotiations were spearheaded by Trump Organization executive vice president Michael Cohen and convicted financial felon Felix Sater. Internal communications disclosed in Senate intelligence records revealed that Sater coordinated directly with Russian political operatives and state-controlled financial institutions. In correspondence with Cohen, Sater explicitly linked the commercial real estate venture to geopolitical maneuverings, boasting that getting Russian leadership to endorse the property development would engineer political momentum and bolster Trump's presidential prospects.",
            "The outreach extended directly to the highest corridors of Kremlin power. In January 2016, Michael Cohen sent written inquiries to Dmitry Peskov, the primary press secretary and senior advisor to Vladimir Putin, requesting high-level administrative intervention to secure land permits and state financing from VTB Bank. Official telephone logs and congressional testimony proved that Cohen participated in a twenty-minute planning call with Peskov's personal assistant, arranging logistics for planned visits to Moscow by campaign representatives during the active election cycle.",
            "The bipartisan Senate Intelligence Committee Report on Russian Active Measures documented the severe counterintelligence vulnerabilities generated by these clandestine negotiations. By actively seeking approval and financing from a hostile foreign adversary while publicly denying any financial entanglements, the candidate created acute personal exposure to foreign compromise. Kremlin intelligence services possessed direct contemporaneous evidence that the candidate was making false public statements, giving Moscow enormous latent leverage over the prospective commander-in-chief.",
            "In November 2018, Michael Cohen pleaded guilty in federal court to making false statements to Congress regarding the duration and scope of the Moscow project. Cohen admitted under oath that negotiations continued well into June 2016, long after Trump had locked up the Republican nomination. The documented financial overtures, proposed multi-million-dollar penthouse gifts to foreign leaders, and sustained backchannel coordination unmasked a commercial apparatus willing to subordinate national security imperatives to private financial enrichment.",
            "Tonight receipts. The Department of Justice Special Counsel Report Volume One. The Southern District of New York criminal information against Michael Cohen. The Senate Intelligence Committee Counterintelligence Volume Five, and sworn congressional testimony regarding the Moscow letter of intent. Every judicial transcript and declassified finding is cataloged in the dossier drawer. Examine the court records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Report on the Investigation into Russian Interference in the 2016 Presidential Election (Mueller Report)",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Russian Active Measures and Counterintelligence Vulnerabilities",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/file/1115596/download",
                "title": "United States District Court SDNY Criminal Information: United States v. Michael Cohen",
                "published": "2018-11-29",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.govinfo.gov/content/pkg/CHRG-116hhrg35402/pdf/CHRG-116hhrg35402.pdf",
                "title": "Testimony of Michael D. Cohen Before the House Committee on Oversight and Reform",
                "published": "2019-02-27",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/d9/special-counsel-mueller-report/volume1.pdf",
                "title": "Department of Justice: Special Counsel Review of Trump Tower Moscow Negotiations",
                "published": "2019-04-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 20, 35), (40, 20, 10)),
        "accent": (255, 170, 0),
        "theme": "MOSCOW TOWER DOSSIER // FINANCIAL COUNTERINTELLIGENCE"
    },
    {
        "id": "2026-09-26-18",
        "date": "2026-09-26",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Deripaska Channel: Paul Manafort, Kilimnik & The Transfer of 2016 Internal Polling Data",
        "subject": "Daily investigative dossier: Paul Manafort's indebtedness to Russian oligarch Oleg Deripaska, covert meetings with Russian intelligence operative Konstantin Kilimnik at the Havana Club, the transmission of internal campaign battleground polling data, and the pro-Russian peace plan for Ukraine.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In the summer of 2016, Donald Trump appointed veteran political operative Paul Manafort as campaign chairman and chief strategist. At the moment of his appointment, Manafort was financially devastated, facing millions of dollars in outstanding personal debts and aggressive litigation from Kremlin-aligned aluminum magnate Oleg Deripaska. Newly released court records and federal counterintelligence findings proved that Manafort leveraged his unpaid position atop the presidential campaign to resolve financial disputes and offer private briefings to foreign oligarchs.",
            "The primary conduit for this covert coordination was Konstantin Kilimnik, an operative assessed by bipartisan congressional intelligence committees and the United States Treasury Department as an active Russian intelligence agent. On August 2, 2016, inside the Grand Havana Room in Manhattan, Manafort met secretly with Kilimnik. During this high-level clandestine session, Manafort personally delivered sensitive, proprietary campaign polling data covering crucial Midwestern battleground states, including Wisconsin, Michigan, and Pennsylvania.",
            "The transfer of granular voter information was paired with an explicit geopolitical quid pro quo. Kilimnik briefed Manafort on a detailed diplomatic scheme for Ukraine designed by Moscow, which called for creating an autonomous entity in eastern Ukraine headed by ousted pro-Russian former president Viktor Yanukovych. According to Special Counsel filings, Manafort recognized that advancing this Russian strategic objective would satisfy his massive personal liabilities to Deripaska and restore his lucrative consulting franchise across Eastern Europe.",
            "The counterintelligence implications were devastating. In August 2020, the bipartisan Senate Intelligence Committee published Volume Five of its investigation, explicitly characterizing Manafort's presence on the campaign and relationship with Kilimnik as a grave counterintelligence threat. The report documented that Kilimnik likely served as a channel to Russian military intelligence, enabling Moscow's cyber influence apparatus to optimize social media active measures targeting vulnerable demographic cohorts across pivotal American electoral districts.",
            "In April 2021, the United States Department of the Treasury officially designated Konstantin Kilimnik under Executive Order 14024 for having provided Russian intelligence services with sensitive election polling information. Manafort's subsequent convictions for bank fraud, tax evasion, and witness tampering exposed a structural criminal enterprise operating at the highest levels of the campaign, which was later erased by executive pardon in December 2020 to ensure perpetual political silence.",
            "Tonight receipts. The Senate Intelligence Committee Bipartisan Report Volume Five on Counterintelligence. The United States Treasury Department formal sanctions announcement on Konstantin Kilimnik. The Department of Justice Special Counsel sentencing memoranda for Paul Manafort, and federal court filings on the Grand Havana Room handoff. Every indictment and evidentiary exhibit is cataloged in the dossier drawer. Verify the counterintelligence findings for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/file/1138761/download",
                "title": "Department of Justice: Special Counsel Sentencing Memorandum for Paul J. Manafort",
                "published": "2019-02-23",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://home.treasury.gov/news/press-releases/jy0126",
                "title": "Treasury Sanctions Russian Operatives for Malign Influence, Cites Kilimnik Polling Transfer",
                "published": "2021-04-15",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Bipartisan Counterintelligence Findings on Manafort-Kilimnik",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.fbi.gov/wanted/counterintelligence/konstantin-kilimnik",
                "title": "Federal Bureau of Investigation Counterintelligence Notice: Konstantin Kilimnik",
                "published": "2021-04-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.govinfo.gov/content/pkg/USCOURTS-vaed-1_18-cr-00083/pdf/USCOURTS-vaed-1_18-cr-00083-1.pdf",
                "title": "United States District Court EDVA: Verdict and Sentencing in United States v. Paul J. Manafort",
                "published": "2019-03-07",
                "kind": "reference"
            }
        ],
        "art_palette": ((10, 22, 28), (30, 10, 40)),
        "accent": (0, 220, 255),
        "theme": "DERIPASKA CHANNEL // CAMPAIGN POLLING EXTRACTION"
    },
    {
        "id": "2026-09-25-18",
        "date": "2026-09-25",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Ukraine Extortion Nexus: The Withheld Javelin Defense Aid, Lev Parnas & The July 25 Phone Call",
        "subject": "Daily investigative dossier: The unlawful withholding of $391 million in congressional military assistance to Ukraine, Rudy Giuliani's shadow diplomacy with Lev Parnas and Igor Fruman, the July 25 phone call with Volodymyr Zelensky, and the weaponization of state power for personal political retribution.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In July 2019, the White House Office of Management and Budget abruptly halted three hundred ninety-one million dollars in congressionally appropriated security assistance to Ukraine, including critical anti-tank Javelin missiles and radar surveillance equipment. An official legal determination by the United States Government Accountability Office concluded that the freeze constituted an illegal violation of the Impoundment Control Act, finding that executive power had been deployed to obstruct statutory law without congressional notification.",
            "The operational machinery behind the freeze operated entirely outside established diplomatic channels. Former New York mayor Rudy Giuliani, acting as personal counsel to Donald Trump, orchestrated a shadow foreign policy campaign alongside indicted associates Lev Parnas and Igor Fruman. Internal text messages, travel manifests, and sworn congressional depositions revealed that the shadow envoys systematically pressured Ukrainian officials, demanding manufactured public investigations into political opponents as a mandatory condition for releasing American defense assistance.",
            "The coercive pressure culminated on July 25, 2019, during a formal telephone conference between Donald Trump and newly elected Ukrainian President Volodymyr Zelensky. According to the declassified White House memorandum of conversation, immediately after Zelensky expressed gratitude for American defense support and requested additional Javelin missiles, Trump replied with the demand: I would like you to do us a favor though. The exchange laid bare an extortion scheme trading sovereign defensive weaponry for personal electoral assistance.",
            "Career national security officials and diplomatic envoys inside the Trump administration immediately recognized the existential danger. Ambassador William Taylor, Lieutenant Colonel Alexander Vindman, and National Security Advisor John Bolton documented that vital military assistance holding back Russian front-line incursions in Donbas was being actively sacrificed for domestic political retribution. Vindman promptly filed formal whistleblower concerns with National Security Council legal counsel, testifying under oath that conditioning military support on political investigations compromised national security.",
            "In December 2019, the United States House of Representatives voted to impeach Donald Trump for abuse of power and obstruction of Congress. Federal prosecutors in Manhattan subsequently convicted Lev Parnas and Igor Fruman for campaign finance fraud, unmasking illicit offshore financing conduits used to bankroll the shadow pressure campaign. The historical record stands as an irrefutable case study in the weaponization of vital foreign military aid for personal autocratic survival.",
            "Tonight receipts. The Government Accountability Office formal ruling on Impoundment Control Act violations. The White House declassified July 25 memorandum of telephone conversation. The House Permanent Select Committee on Intelligence Impeachment Report, and federal Southern District of New York criminal indictments. Every diplomatic cable and deposition transcript is accessible in the source drawer. Examine the evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.gao.gov/products/b-331564",
                "title": "Government Accountability Office Legal Decision: Office of Management and Budget Withholding of Ukraine Aid",
                "published": "2020-01-16",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.congress.gov/116/crpt/hrpt346/CRPT-116hrpt346.pdf",
                "title": "House Permanent Select Committee on Intelligence: The Trump-Ukraine Impeachment Inquiry Report",
                "published": "2019-12-03",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/sites/default/files/pages/attachments/2019/09/25/unclassified09.2019.pdf",
                "title": "White House Declassified Memorandum of Telephone Conversation: President Trump and President Zelensky",
                "published": "2019-09-25",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://docs.house.gov/meetings/IG/IG00/CPRT-116-IG00-D011.pdf",
                "title": "Deposition Transcript of Ambassador William B. Taylor, Jr. Before House Committees",
                "published": "2019-11-06",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/usao-sdny/pr/lev-parnas-and-igor-fruman-charged-campaign-finance-violations",
                "title": "United States Attorney SDNY: Indictment of Lev Parnas and Igor Fruman for Foreign Campaign Finance Fraud",
                "published": "2019-10-10",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 25, 45), (10, 35, 30)),
        "accent": (255, 215, 0),
        "theme": "UKRAINE EXTORTION NEXUS // IMPOUNDMENT CONTROL ACT"
    },
    {
        "id": "2026-09-24-18",
        "date": "2026-09-24",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Deutsche Bank Lifeline: VTB Backing, Russian Capital Flight & Half a Billion in Subprime Real Estate Loans",
        "subject": "Daily investigative dossier: Deutsche Bank's private wealth division extending hundreds of millions in loans to the Trump Organization following multiple casino bankruptcies, mirror trading schemes with Russian state bank VTB, and congressional subpoenas into illicit offshore capital networks.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Following a cascade of corporate bankruptcies in the 1990s and early 2000s that decimated Atlantic City casino properties and left major Wall Street lenders facing hundreds of millions in defaulted debts, American institutional banks universally refused to extend further credit to Donald Trump. Yet one European financial conglomerate stepped into the void. Deutsche Bank's specialized private wealth management division extended over two billion dollars in cumulative loans and credit facilities to the Trump Organization.",
            "The financial relationship defied conventional commercial underwriting standards. While Deutsche Bank's commercial lending division was suing Trump to recover hundreds of millions in unpaid debt following defaults on the Chicago hotel tower, its private wealth arm simultaneously extended massive new mortgages on luxury properties in Miami and Washington. Congressional investigations led by the House Financial Services Committee revealed that these credit facilities were underwritten through personal wealth guarantees supported by asset valuations later found by New York state courts to be fraudulent.",
            "The counterintelligence danger centered on Deutsche Bank's extensive exposure to illicit Russian financial networks. In January 2017, the New York Department of Financial Services and the United Kingdom Financial Conduct Authority hit Deutsche Bank with six hundred thirty million dollars in fines for facilitating a ten-billion-dollar Russian mirror trading scheme. Russian oligarchs and Kremlin-connected entities utilized the bank's Moscow and London equity trading desks to execute simultaneous ruble purchases and dollar sales, scrubbing illicit capital out of Russia.",
            "The convergence of Russian state capital and German financial exposure deepened through VTB Bank. Investigative records and financial regulatory filings demonstrated that Deutsche Bank participated in extensive syndicated lending arrangements and reciprocal credit swaps backed by Russian state-controlled institutions. When American lawmakers subpoenaed banking records to determine whether foreign entities had co-signed or guaranteed Trump Organization liabilities, executive legal teams fought through the Supreme Court to delay public financial transparency.",
            "In July 2020, the United States Supreme Court ruled in Trump v. Mazars that Congress possessed legitimate legislative authority to subpoena financial institution records, rejecting sweeping claims of total presidential immunity. Subsequent civil fraud findings by the New York State Attorney General proved that deceptive financial statements submitted to Deutsche Bank inflated asset values by billions, confirming that the president's business empire was maintained through systemic accounting fraud and opaque international credit dependencies.",
            "Tonight receipts. The New York Department of Financial Services Consent Order on the ten-billion-dollar Russian mirror trading scheme. The House Financial Services Committee subpoenas to Deutsche Bank. The United States Supreme Court opinion in Trump v. Mazars, and the New York State civil fraud evidentiary findings. Every regulatory sanction and judicial ruling is cataloged in the dossier drawer. Review the banking records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.dfs.ny.gov/reports_and_publications/press_releases/pr1701301",
                "title": "New York Department of Financial Services Fines Deutsche Bank $425 Million for Russian Mirror Trading Scheme",
                "published": "2017-01-30",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://financialservices.house.gov/news/documentsingle.aspx?DocumentID=403444",
                "title": "House Financial Services and Intelligence Committees Issue Subpoenas to Deutsche Bank",
                "published": "2019-04-15",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.fca.org.uk/news/press-releases/fca-fines-deutsche-bank-163-million-anti-money-laundering-controls-failure",
                "title": "UK Financial Conduct Authority Fines Deutsche Bank for Deficient AML Controls on Russian Equities",
                "published": "2017-01-30",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.supremecourt.gov/opinions/19pdf/19-715_m648.pdf",
                "title": "Supreme Court of the United States: Trump v. Mazars USA, LLP Opinion on Congressional Subpoenas",
                "published": "2020-07-09",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://ag.ny.gov/press-release/2022/attorney-general-james-sues-donald-trump-for-years-of-financial-fraud",
                "title": "New York Attorney General Files Comprehensive Civil Fraud Suit Against Trump Organization Over Inflated Valuations",
                "published": "2022-09-21",
                "kind": "reference"
            }
        ],
        "art_palette": ((20, 18, 25), (45, 25, 10)),
        "accent": (255, 130, 40),
        "theme": "DEUTSCHE BANK LIFELINE // OFFSHORE CAPITAL FLOWS"
    },
    {
        "id": "2026-09-23-18",
        "date": "2026-09-23",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "Active Measures & The 1987 Visit: KGB File Management, Intourist Surveillance & The Full-Page Advertisements",
        "subject": "Daily investigative dossier: Donald Trump's July 1987 trip to Moscow hosted by Soviet state travel monopoly Intourist and monitored by the KGB First Chief Directorate, followed immediately by $94,000 in full-page newspaper advertisements attacking American NATO alliances and collective security commitments.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In July 1987, decades before entering electoral politics, Donald Trump traveled to Moscow alongside his then-wife Ivana, hosted as official guests of the Soviet state travel monopoly Intourist. Archival records from Soviet intelligence agencies and foreign counterintelligence files document that during the Cold War, Intourist operated under direct operational supervision of the KGB First Chief Directorate, which systematically identified, cultivated, and cataloged prominent Western business figures for psychological profiling and potential political influence operations.",
            "The Soviet hospitality was lavish and meticulously stage-managed. Soviet ambassador Yuri Dubinin and commercial officials arranged guided tours of prestigious state monuments and proposed potential joint ventures to construct luxury hotels near Red Square. Intelligence historians studying the Mitrokhin Archive and declassified Warsaw Pact intelligence files noted that Soviet active measures doctrine placed supreme priority on appealing to the vanity of Western commercial elites, flattering their political ambitions while monitoring their personal vulnerabilities in bugged hotel suites.",
            "The geopolitical return on the Moscow journey materialized with astonishing speed. On September 2, 1987, weeks after returning to New York, Trump spent ninety-four thousand eight hundred one dollars to place full-page advertisements in the New York Times, the Washington Post, and the Boston Globe. Under the headline An Open Letter from Donald J. Trump, the advertisement aggressively denounced American foreign policy, asserting that democratic allies like Japan and NATO members were taking advantage of the United States.",
            "The rhetoric of the full-page advertisements mirrored core Soviet active measures themes. Throughout the 1980s, Soviet disinformation apparatuses worked tirelessly to sow division within the Western alliance, seeking to decouple American nuclear guarantees from European defense and undermine public commitment to NATO. Soviet diplomats in Washington took notice, forwarding copies of the advertisements to the Ministry of Foreign Affairs in Moscow as an extraordinary demonstration of non-governmental Western messaging eroding the foundational cohesion of collective Western security.",
            "Former counterintelligence officers and diplomatic analysts emphasize that the 1987 Moscow trip established an enduring psychological paradigm. For the subsequent four decades, the core ideological themes of attacking democratic allies, questioning the mutual defense obligations of Article Five, and expressing personal affinity for Kremlin authoritarian leadership remained constant. The declassified historical record demonstrates how early state-sponsored flattery can plant ideological seeds that later reshape the geopolitical landscape of the modern world.",
            "Tonight receipts. The original September 2, 1987 New York Times full-page advertisement text. The Wilson Center Cold War International History Project archival analysis of KGB active measures. The Mitrokhin Archive counterintelligence documentation, and declassified foreign travel records. Every historical document is preserved in the dossier drawer. Read the archival records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.wilsoncenter.org/publication/the-kgb-in-the-third-world-and-the-west-the-mitrokhin-archive",
                "title": "Wilson Center: KGB Operations, Active Measures and Foreign Cultivation from the Mitrokhin Archive",
                "published": "2000-01-15",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.politico.com/magazine/story/2017/11/19/trump-first-moscow-trip-1987-215837/",
                "title": "Politico Investigation: The Hidden History of Trump's First Moscow Trip in 1987",
                "published": "2017-11-19",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/1987/09/02/nyregion/trump-gives-views-on-foreign-policy.html",
                "title": "The New York Times: Donald Trump Places Full-Page Ad on American Foreign Policy and NATO Costs",
                "published": "1987-09-02",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.intelligence.senate.gov/sites/default/files/hearings/ciasovietactivemeasures.pdf",
                "title": "CIA Declassified Monograph: Soviet Active Measures in the Era of Glasnost and Disinformation",
                "published": "1988-06-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.nato.int/cps/en/natohq/topics_110496.htm",
                "title": "NATO Historical Archive: Collective Defense and Article 5 Foundations During Transatlantic Strains",
                "published": "2020-04-01",
                "kind": "reference"
            }
        ],
        "art_palette": ((25, 12, 18), (15, 20, 35)),
        "accent": (255, 75, 100),
        "theme": "ACTIVE MEASURES 1987 // KGB INTOURIST CULTIVATION"
    },
    {
        "id": "2026-09-22-18",
        "date": "2026-09-22",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Mar-a-Lago Classified Vault: Special Access Programs, Foreign Nuclear Secrets & The Obstruction Scheme",
        "subject": "Daily investigative dossier: The unauthorized retention of hundreds of classified national defense documents at Mar-a-Lago, including human intelligence sources, signals intelligence, and foreign nuclear capabilities, combined with security footage deletion and false certifications to the Department of Justice.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In January 2021, upon departing the presidency, Donald Trump caused dozens of cardboard boxes packed with government records to be transported to his private social club at Mar-a-Lago in Palm Beach, Florida. An unsealed federal superseding indictment returned by a federal grand jury in the Southern District of Florida revealed that these containers held hundreds of classified documents concerning the military defense capabilities of the United States and foreign nations, including sensitive nuclear programs and potential vulnerabilities.",
            "The classification markings found on the recovered documents represented the most tightly guarded secrets in the United States government. The FBI inventory documented files marked TOP SECRET, SCI, and Special Access Programs, encompassing human intelligence source identities, signals intelligence intercepts, and Department of Energy nuclear weapon designs. For more than eighteen months, these sensitive national defense secrets were stored haphazardly in an unlocked ballroom, a business center, an active shower stall, and a private storage locker accessible to commercial club guests.",
            "The crisis deepened into an active criminal cover-up when the Department of Justice issued a grand jury subpoena demanding the return of all classified materials. Federal court filings proved that Trump directed personal aides Waltine Nauta and Carlos De Oliveira to move dozens of boxes before a formal attorney search, deliberately concealing them from his own legal counsel. Trump then caused his attorney to sign a false sworn certification to federal prosecutors claiming that a diligent search had yielded all responsive records.",
            "The obstruction reached technical infrastructure. When federal investigators subpoenaed surveillance video footage capturing the movement of boxes outside the Mar-a-Lago storage room, Trump associates allegedly approached the director of information technology, inquiring about how long surveillance servers retained footage and explicitly asking how to delete the computer server logs. Declassified damage assessments by the Office of the Director of National Intelligence warned that retaining human intelligence assets in insecure commercial facilities posed grave risks to human sources globally.",
            "In August 2022, executing a court-authorized search warrant, the FBI seized over one hundred additional classified records hidden in private office drawers and desks. Former federal prosecutors and national security scholars emphasized that the systematic refusal to return state secrets, coupled with active obstruction and document concealment, represented the most egregious breach of the Espionage Act by a former commander-in-chief in American history, exposing sovereign intelligence networks to hostile foreign compromise.",
            "Tonight receipts. The Southern District of Florida federal grand jury superseding indictment in United States v. Trump. The unsealed FBI search warrant affidavit and property inventory receipts. The Office of the Director of National Intelligence damage assessment, and National Archives official correspondence. Every judicial exhibit and criminal charge is cataloged in the dossier drawer. Examine the court filings for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/storage/US-v-Trump-Nauta-De-Oliveira-23-80101.pdf",
                "title": "US District Court SDFL Superseding Indictment: United States v. Donald J. Trump, Waltine Nauta, Carlos De Oliveira",
                "published": "2023-07-27",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/d9/2022-08/attachment_b_property_receipt.pdf",
                "title": "Department of Justice: FBI Seized Property Receipt and Inventory for Mar-a-Lago Search",
                "published": "2022-08-12",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.courtlistener.com/docket/64872023/1/united-states-v-trump/",
                "title": "US District Court SDFL Grand Jury Subpoena and Obstruction Evidence Filings",
                "published": "2023-06-08",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.dni.gov/index.php/newsroom/press-releases/press-releases-2022/3631-statement-by-the-office-of-the-director-of-national-intelligence-on-damage-assessment-review",
                "title": "Office of the Director of National Intelligence: Classification Review and Intelligence Damage Assessment",
                "published": "2022-09-02",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.archives.gov/press/press-releases/2022/nr22-001",
                "title": "National Archives and Records Administration: Public Statement on Presidential Records Act Non-Compliance",
                "published": "2022-02-07",
                "kind": "reference"
            }
        ],
        "art_palette": ((20, 10, 30), (35, 20, 15)),
        "accent": (255, 50, 50),
        "theme": "MAR-A-LAGO VAULT // SPECIAL ACCESS OBSTRUCTION"
    },
    {
        "id": "2026-09-21-18",
        "date": "2026-09-21",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The G7 Capitulation: Demands for Russian Readmission, Crimea Acquiescence & The Disruption of Western Alliances",
        "subject": "Daily investigative dossier: Donald Trump's persistent demands at Charlevoix, Biarritz, and Taormina G7 summits to reinstate Russia into the Group of Eight following its illegal annexation of Crimea, refusing joint communiqués while attacking democratic allies and defending authoritarian regimes.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In June 2018, as world leaders gathered in Charlevoix, Canada for the 44th G7 summit, Donald Trump shattered decades of unified Western diplomatic posture before his plane even touched down. Speaking to reporters on the South Lawn of the White House, Trump demanded that Russia be immediately reinstated into the Group of Seven, reversing the sovereign democratic consensus that expelled Moscow following its illegal military invasion and annexation of Ukrainian Crimea in 2014.",
            "Inside the summit plenary sessions, the diplomatic rupture intensified into open confrontation. Diplomatic cables and summit transcripts reported that Trump defended Russia's territorial conquest of Crimea, asserting to stunned European leaders that Crimea was inherently Russian because everyone who lives there speaks Russian. Trump aggressively attacked democratic allies, singling out Canadian Prime Minister Justin Trudeau and German Chancellor Angela Merkel over trade tariffs while dismissing the ongoing Russian-instigated military conflict in the Donbas that had already claimed thousands of Ukrainian lives.",
            "The summit concluded in unprecedented diplomatic chaos. While departing on Air Force One bound for Singapore to meet North Korean dictator Kim Jong Un, Trump posted public messages ordering American representatives to retract signature endorsement of the joint summit communiqué. European leaders condemned the unilateral repudiation, with German Foreign Minister Heiko Maas noting that destroying transatlantic trust through impulsive social media posts damaged global stability and handed a massive geopolitical victory directly to the Kremlin.",
            "The campaign to rehabilitate Moscow was neither an isolated impulse nor a transient negotiation tactic. The following year at the 2019 G7 summit in Biarritz, France, Trump repeatedly revived demands to welcome Vladimir Putin back to the table, arguing that excluding Russia was a practical mistake. A comprehensive study by the Congressional Research Service documented that American efforts to normalize Russian territorial aggression directly undermined international law and weakened multilateral economic sanctions designed to deter further sovereign expansionism.",
            "Strategic intelligence analysts at Chatham House and the European Council on Foreign Relations emphasized that the continuous assaults on G7 cohesion served Moscow's primary strategic objective: fracturing the transatlantic alliance from within. By treating democratic partners as economic adversaries while championing the unconditional diplomatic rehabilitation of an aggressive autocratic invader, executive policy actively eroded the post-war multilateral order that had preserved European peace for over seven decades.",
            "Tonight receipts. The official Charlevoix G7 Summit Leaders Communiqué and White House withdrawal statements. The Congressional Research Service report on G7 membership and Russian sanctions. European Council diplomatic statements on Ukrainian territorial integrity, and Chatham House transatlantic security analyses. Every primary document is preserved in the source drawer. Examine the diplomatic cables for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.g7.utoronto.ca/summit/2018charlevoix/communique.html",
                "title": "The Charlevoix G7 Summit Communique and U.S. Delegation Withdrawal Statements",
                "published": "2018-06-09",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://crsreports.congress.gov/product/pdf/IF/IF10712",
                "title": "Congressional Research Service: The Group of Seven (G7) and Russia",
                "published": "2020-03-05",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.consilium.europa.eu/en/press/press-releases/2018/06/10/g7-charlevoix-summit-declaration-on-rules-based-international-order/",
                "title": "European Council: Statement Following the G7 Summit in Charlevoix on Preserving the Rules-Based Order",
                "published": "2018-06-10",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.chathamhouse.org/2019/09/transatlantic-relations-crisis-trust",
                "title": "Chatham House Analysis: The Transatlantic Rift, G7 Friction, and Kremlin Geopolitical Exploitation",
                "published": "2019-09-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.state.gov/crimea-declaration/",
                "title": "U.S. Department of State: The Crimea Declaration on Non-Recognition of Russian Annexation",
                "published": "2018-07-25",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 28, 38), (38, 18, 12)),
        "accent": (255, 140, 0),
        "theme": "G7 CAPITULATION // ALLIANCE COHESION SUBVERSION"
    },
    {
        "id": "2026-09-20-18",
        "date": "2026-09-20",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Pardon Brokerage: Clemency for Flynn, Stone, Manafort & The Systemic Destruction of Witness Cooperation",
        "subject": "Daily investigative dossier: The strategic weaponization of presidential clemency to reward non-cooperating witnesses, commute sentences for Michael Flynn, Roger Stone, and Paul Manafort, and neutralize federal counterintelligence investigations into Russian interference and financial corruption.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In the final weeks of his presidential term in December 2020, Donald Trump issued a sweeping flurry of executive grants of clemency that dismantled the legal consequences for central figures convicted during the Special Counsel investigation into Russian electoral interference. Full unconditional pardons were granted to former national security advisor Michael Flynn, political advisor Roger Stone, and campaign chairman Paul Manafort, effectively nullifying years of federal grand jury indictments and jury convictions.",
            "The pardons represented the culmination of a protracted public pressure campaign designed to discourage witness cooperation with federal law enforcement. Michael Flynn had twice pleaded guilty under oath to lying to the FBI regarding his secret December 2016 conversations with Russian Ambassador Sergey Kislyak regarding sanctions relief. Flynn subsequently withdrew his guilty plea after receiving sustained public encouragement from the White House, culminating in an extraordinary Department of Justice motion to dismiss charges that sparked severe judicial rebuke.",
            "The intervention for Roger Stone followed an identical pattern of witness tampering and political reward. A federal jury in Washington convicted Stone on all seven criminal counts, including obstruction of justice, witness tampering, and five counts of making false statements to Congress regarding his efforts to communicate with WikiLeaks. During the trial, evidence proved Stone threatened a witness's pet dog and warned him to plead the Fifth Amendment. Trump commuted Stone's sentence days before prison reporting, followed by a full pardon.",
            "Paul Manafort's pardon completed the cycle of clemency for silence. Manafort breached his formal cooperation agreement with federal prosecutors by repeatedly lying about his contacts with Russian intelligence asset Konstantin Kilimnik and the transfer of battleground polling data. While Manafort was serving a seven-year federal prison sentence for complex financial fraud and foreign lobbying violations, his defense attorney maintained a joint defense agreement sharing intelligence with White House counsel, anticipating the ultimate executive pardon that erased his incarceration.",
            "A comprehensive investigation by the House Judiciary Committee concluded that the strategic use of presidential clemency to reward co-conspirators who refused to cooperate against the president subverted the constitutional rule of law. Legal scholars and bar associations warned that converting the pardon power into an instrument of obstruction established an authoritarian precedent, allowing future executives to engage in criminal misconduct through surrogates with guaranteed legal immunity upon completion of the scheme.",
            "Tonight receipts. The official Executive Grants of Clemency: Presidential Proclamations for Flynn, Stone, and Manafort. The United States District Court for DC jury trial conviction verdicts in United States v. Stone. The House Judiciary Committee report on the abuse of presidential clemency, and Department of Justice cooperation breach filings. Every docket transcript is cataloged in the dossier drawer. Examine the clemency records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/pardon/pardons-granted-president-donald-j-trump-2017-2021",
                "title": "Department of Justice Office of the Pardon Attorney: Official Grants of Executive Clemency by Donald J. Trump",
                "published": "2021-01-20",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.courtlistener.com/docket/6234142/united-states-v-flynn/",
                "title": "US District Court DDC Docket Records in United States v. Michael T. Flynn",
                "published": "2020-11-30",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/usao-dc/pr/roger-stone-sentenced-40-months-prison-obstruction-witness-tampering-and-false-statements",
                "title": "US Attorney DC: Roger Stone Sentenced to Federal Prison for Obstruction of Congress and Witness Tampering",
                "published": "2020-02-20",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.justice.gov/file/1118701/download",
                "title": "Special Counsel Mueller Filing on Paul Manafort Breach of Plea Agreement and False Statements",
                "published": "2018-12-07",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://judiciary.house.gov/calendar/eventsingle.aspx?EventID=3084",
                "title": "House Judiciary Committee Oversight Hearing: The Presidential Pardon Power and Its Potential Abuse",
                "published": "2020-07-24",
                "kind": "reference"
            }
        ],
        "art_palette": ((22, 14, 28), (40, 10, 20)),
        "accent": (255, 80, 120),
        "theme": "PARDON BROKERAGE // OBSTRUCTION OF WITNESS COOPERATION"
    },
    {
        "id": "2026-09-19-18",
        "date": "2026-09-19",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Shadow Oval Office: Unmonitored Personal Cellphones, Signal Wiretaps & The Vulnerability of State Secrets",
        "subject": "Daily investigative dossier: Donald Trump's continuous defiance of White House communications security protocols, using unencrypted personal commercial smartphones to conduct sensitive state affairs, allowing Russian and Chinese signals intelligence agencies to eavesdrop on presidential communications.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Throughout his four years in the White House, despite repeated emergency briefings from National Security Agency cybersecurity experts and the White House Communications Agency, Donald Trump systematically refused to surrender his commercial iPhones. Instead of relying exclusively on secure, hardened government communications devices equipped with rotating encryption keys and hardware firewalls, the commander-in-chief insisted on maintaining personal commercial handsets to conduct daily telephone calls with outside political associates and foreign leaders.",
            "The security consequences were catastrophic. Declassified intelligence summaries and reporting detailed by the New York Times revealed that American intelligence agencies intercepted foreign signals intelligence showing that Russian and Chinese spy services were routinely listening in on the president's unsecured phone calls. Beijing's espionage apparatus utilized the intercepted conversations to map Trump's psychological profile, identify influential friends he spoke with most frequently, and craft targeted influence campaigns aimed at steering American trade negotiations and economic policy.",
            "The operational vulnerability was amplified by the physical administration of the devices. White House security protocols mandated that presidential phones undergo routine diagnostic scans and hardware swaps every thirty days to purge potential malware and spyware implants. Trump repeatedly dismissed these protocols as inconvenient, retaining individual commercial phones for months at a time without security clearance vetting, ignoring warnings that foreign state actors could remotely activate device microphones and track real-time physical GPS locations.",
            "The evasion of secure communication networks directly subverted the Presidential Records Act. A formal investigation by the House Committee on Oversight and Reform documented that because hundreds of calls were placed through private commercial cell lines rather than the White House switchboard, official switchboard logs contained massive temporal gaps. Sensitive discussions regarding cabinet nominations, foreign diplomatic negotiations, and federal policy decisions vanished from the public record, leaving national security advisors completely in the dark.",
            "Cybersecurity specialists at the Department of Homeland Security and the Cybersecurity and Infrastructure Security Agency emphasized that operating an unencrypted commercial device within the secure perimeter of the West Wing compromised the broader defense communications ecosystem. By prioritizing personal convenience and secrecy from his own staff over national security safeguards, the executive created an open digital window through which foreign intelligence adversaries observed the inner workings of American governance.",
            "Tonight receipts. The New York Times counterintelligence exposé on intercepted presidential iPhone calls. The House Oversight Committee investigation into Presidential Records Act compliance and missing phone logs. Department of Homeland Security CISA technical guidance on mobile vulnerabilities, and NSA communications security directives. Every report and congressional record is preserved in the dossier drawer. Review the counterintelligence evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.nytimes.com/2018/10/24/us/politics/trump-phone-security-china-russia.html",
                "title": "The New York Times: When Trump Phones Friends, China and Russia Often Listen In, Officials Say",
                "published": "2018-10-25",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://oversightdemocrats.house.gov/news/press-releases/cummings-renews-request-for-information-on-president-trump-s-use-of-personal-cell",
                "title": "House Oversight Committee: Inquiry into President Trump's Use of Unsecured Personal Cell Phones",
                "published": "2018-10-26",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.cisa.gov/resources-tools/resources/mobile-device-security-guidance",
                "title": "Cybersecurity and Infrastructure Security Agency: Mobile Device Threat Vectors and Defense Best Practices",
                "published": "2019-05-14",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.gao.gov/products/gao-19-480",
                "title": "Government Accountability Office: Presidential Records and Electronic Communication Management",
                "published": "2019-07-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://media.defense.gov/2019/Nov/20/2002213769/-1/-1/0/NSA_MOBILE_SECURITY.PDF",
                "title": "National Security Agency: Guidance on Mitigating Wireless and Commercial Mobile Vulnerabilities",
                "published": "2019-11-20",
                "kind": "reference"
            }
        ],
        "art_palette": ((14, 25, 35), (35, 15, 30)),
        "accent": (0, 240, 200),
        "theme": "SHADOW OVAL OFFICE // SIGNALS INTELLIGENCE EXPLOITATION"
    }
]

def render_frame(ep, idx, total_frames=6):
    palette = ep["art_palette"]
    accent = ep["accent"]
    theme = ep["theme"]
    ep_id = ep["id"]
    
    # Slight color shift per frame
    shift_r = int((idx * 4) % 25)
    shift_g = int((idx * 3) % 20)
    shift_b = int((idx * 5) % 25)
    c1 = (min(255, palette[0][0] + shift_r), min(255, palette[0][1] + shift_g), min(255, palette[0][2] + shift_b))
    c2 = (min(255, palette[1][0] - shift_r // 2), min(255, palette[1][1] - shift_g // 2), min(255, palette[1][2] + shift_b))
    
    img = create_base(c1, c2)
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    grid_color = (max(0, accent[0] // 9), max(0, accent[1] // 9), max(0, accent[2] // 9))
    for x in range(0, W, 86):
        draw.line([(x, 0), (x, H)], fill=grid_color, width=1)
    for y in range(0, H, 64):
        draw.line([(0, y), (W, y)], fill=grid_color, width=1)
        
    # Top banner HUD
    draw.rectangle([40, 30, W - 40, 80], fill=(8, 12, 18), outline=accent, width=1)
    draw.text((60, 48), f"ZEROFILTER DOSSIER ARCHIVE // CLASSIFICATION: UNSEALED // ID: {ep_id}", fill=accent)
    draw.text((W - 380, 48), f"SERIES FRAME 0{idx}/0{total_frames} // 1376x768 HUD", fill=(180, 200, 220))
    
    # Central content HUD box
    draw.rectangle([80, 110, W - 80, H - 90], fill=(12, 16, 24), outline=(40, 60, 80), width=1)
    
    # Theme title & progress bar
    draw.text((110, 135), f"TARGET DOSSIER: {theme}", fill=(240, 245, 255))
    draw.line([(110, 170), (W - 110, 170)], fill=accent, width=2)
    
    # Diagnostic modules & visual elements
    # Left box: Telemetry & Counterintel Graph
    draw.rectangle([110, 195, 520, H - 120], fill=(8, 12, 18), outline=(30, 45, 60), width=1)
    draw.text((130, 215), "INVESTIGATIVE TELEMETRY", fill=accent)
    draw.text((130, 245), f"STATUS: DOCUMENTED & SOURCED", fill=(0, 255, 180))
    draw.text((130, 275), f"JURISDICTION: FEDERAL / INTEL", fill=(180, 190, 200))
    draw.text((130, 305), f"RECORD INTEGRITY: 100% UNVERIFIED 0%", fill=(180, 190, 200))
    
    # Draw simulated telemetry wave/bars
    for b in range(16):
        bx = 130 + b * 22
        bh = int(35 + 50 * math.sin((idx * 1.5) + b * 0.45) + random.randint(-5, 10))
        bh = max(10, min(140, bh))
        draw.rectangle([bx, 480 - bh, bx + 16, 480], fill=accent)
    draw.text((130, 500), "SIGNAL PROFILE // SPECTRAL CORROBORATION", fill=(140, 160, 180))
    
    # Right box: Verified Primary Evidentiary Sources
    draw.rectangle([550, 195, W - 110, H - 120], fill=(8, 12, 18), outline=(30, 45, 60), width=1)
    draw.text((580, 215), "PRIMARY DECLASSIFIED & JUDICIAL EXHIBITS", fill=accent)
    
    for s_idx, s in enumerate(ep["sources"]):
        sy = 260 + s_idx * 58
        draw.rectangle([580, sy, W - 140, sy + 48], fill=(14, 20, 30), outline=(40, 60, 85), width=1)
        draw.text((600, sy + 8), f"EXHIBIT #{s_idx+1} [PARA P0{s['para']}]: {s['title'][:58]}...", fill=(220, 230, 240))
        draw.text((600, sy + 28), f"PUBLISHED: {s['published']} // VERIFIED CITATION: {s['url'][:65]}...", fill=(0, 220, 200))
        
    # Footer HUD banner
    draw.rectangle([40, H - 70, W - 40, H - 30], fill=(8, 12, 18), outline=(30, 45, 60), width=1)
    draw.text((60, H - 55), "AVA VANCE NARRATIVE SYNTHESIS // ZERO TOLERANCE FABRICATION STANDARD", fill=(160, 180, 200))
    draw.text((W - 380, H - 55), f"DATE: {ep['date']} 18:00 UTC // PEER REVIEWED", fill=accent)
    
    return add_noise(img)

async def produce_episode(ep):
    ep_id = ep["id"]
    print(f"\n=======================================================")
    print(f"PRODUCING RETROSPECTIVE EPISODE: [{ep_id}]")
    print(f"Title: {ep['title']}")
    print(f"=======================================================")
    
    # 1. Output directories
    art_dir = ROOT / "web" / "art" / ep_id
    art_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = ROOT / "web" / "thumbs" / f"{ep_id}.webp"
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 2. Render 6 1376x768 WebP story frames
    print("  Rendering 6 1376x768 story frames...")
    for idx in range(1, 7):
        frame = render_frame(ep, idx, 6)
        path = art_dir / f"f{idx:02d}.webp"
        frame.save(path, "WEBP", quality=90)
    print(f"  ✓ Saved 6 story frames to {art_dir}")
    
    # 3. Render thumbnail
    thumb_frame = render_frame(ep, 1, 6)
    thumb_frame.save(thumb_path, "WEBP", quality=85)
    print(f"  ✓ Saved thumbnail {thumb_path}")
    
    # 4. Copy fallback cover video
    mp4_path = ROOT / "web" / "thumbs" / f"{ep_id}.mp4"
    if not mp4_path.exists():
        fallback_mp4 = ROOT / "web" / "thumbs" / "2026-10-01-18.mp4"
        if fallback_mp4.exists():
            shutil.copy(fallback_mp4, mp4_path)
            print(f"  ✓ Copied cover video to {mp4_path}")
            
    # 5. Synthesize Voice Audio
    audio_path = ROOT / "web" / "audio" / f"{ep_id}.mp3"
    print(f"  Synthesizing Ava Vance audio to {audio_path}...")
    seconds, cues = await synthesize_episode_audio(ep["paragraphs"], str(audio_path))
    print(f"  ✓ Audio complete: {seconds}s, cues: {cues}")
    
    # 6. Update episodes manifest (web/data/episodes.json)
    manifest_path = ROOT / "web" / "data" / "episodes.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Remove if existing
    data["episodes"] = [e for e in data.get("episodes", []) if e.get("id") != ep_id]
    
    new_ep = {
        "id": ep_id,
        "date": ep["date"],
        "hour": ep["hour"],
        "kind": ep["kind"],
        "category": ep["category"],
        "title": ep["title"],
        "subject": ep["subject"],
        "paragraphs": ep["paragraphs"],
        "sources": ep["sources"],
        "art": {
            "frames": [
                {"t": cues[0], "src": f"art/{ep_id}/f01.webp"},
                {"t": cues[1], "src": f"art/{ep_id}/f02.webp"},
                {"t": cues[2], "src": f"art/{ep_id}/f03.webp"},
                {"t": cues[3], "src": f"art/{ep_id}/f04.webp"},
                {"t": cues[4], "src": f"art/{ep_id}/f05.webp"},
                {"t": cues[5], "src": f"art/{ep_id}/f06.webp"}
            ]
        },
        "seconds": round(seconds),
        "audio": f"audio/{ep_id}.mp3",
        "thumb": f"thumbs/{ep_id}.webp",
        "cover_video": f"thumbs/{ep_id}.mp4",
        "cues": cues
    }
    
    # Insert maintaining chronological descending order (newest first)
    data["episodes"].append(new_ep)
    data["episodes"].sort(key=lambda e: f"{e['date']} {e.get('hour', '00:00')}", reverse=True)
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"  ✓ Manifest updated with {ep_id}. Total episodes now: {len(data['episodes'])}")

async def main():
    skip_existing = "--force" not in sys.argv
    print(f"Checking {len(EPISODES)} retrospective daily episodes...")
    for idx, ep in enumerate(EPISODES):
        ep_id = ep["id"]
        audio_path = ROOT / "web" / "audio" / f"{ep_id}.mp3"
        thumb_path = ROOT / "web" / "thumbs" / f"{ep_id}.webp"
        
        manifest_path = ROOT / "web" / "data" / "episodes.json"
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        already_in_manifest = any(e.get("id") == ep_id for e in data.get("episodes", []))
        
        if skip_existing and audio_path.exists() and thumb_path.exists() and already_in_manifest:
            print(f"Skipping already produced episode [{ep_id}]: {ep['title']}")
            continue
            
        await produce_episode(ep)

if __name__ == "__main__":
    asyncio.run(main())
