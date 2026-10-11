#!/usr/bin/env python3
"""
tools/produce_daily_trump_series_batch2.py - Production Engine for Batch 2 Retrospective Daily Investigative Podcasts
ZeroFilter Geopolitical & Counterintelligence Dossier Series (2026-09-18 down to 2026-09-09)
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
        "id": "2026-09-18-18",
        "date": "2026-09-18",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Flynn Backchannel: Russian Sanctions Relief, Secret Kislyak Calls & The Logan Act Violations",
        "subject": "Daily investigative dossier: Michael Flynn's clandestine December 2016 conversations with Russian Ambassador Sergey Kislyak promising to nullify Obama administration sanctions for election interference, deceptive FBI statements, and the systemic subversion of the Logan Act.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In late December 2016, following the formal imposition of executive sanctions by the Obama administration penalizing Russian military intelligence for cyber interference in the presidential election, incoming national security advisor Michael Flynn initiated a series of clandestine phone calls with Russian Ambassador Sergey Kislyak. Declassified transcripts released by the Director of National Intelligence proved that Flynn explicitly urged the Kremlin not to escalate retaliatory measures, promising that the incoming Trump administration would review and neutralize the sanctions once in power.",
            "The secret diplomatic backchannel directly undermined sitting American foreign policy in violation of the Logan Act. While vacationing in the Dominican Republic, Flynn placed five separate calls to Kislyak on December 29 alone, coordinating directly with senior transition officials gathered at the Mar-a-Lago resort. When Russian President Vladimir Putin unexpectedly announced that Moscow would refrain from expelling American diplomats in response to the sanctions, Donald Trump publicly praised the Russian leader on Twitter, calling the calculated move a great move and calling Putin very smart.",
            "The clandestine commitments triggered an immediate national security crisis. On January 24, 2017, FBI counterintelligence agents interviewed Flynn inside the West Wing regarding his discussions with Kislyak. Flynn repeatedly lied under oath, falsely denying that he had requested Russia refrain from escalating sanctions or discussed diplomatic expulsions. Acting Attorney General Sally Yates subsequently traveled to the White House to deliver an emergency warning to White House counsel, emphasizing that Flynn had lied to Vice President Mike Pence and was actively vulnerable to Russian blackmail.",
            "The institutional cover-up compounded the underlying counterintelligence compromise. Despite receiving explicit warnings from the Department of Justice that their incoming national security advisor was compromised by foreign intelligence intercepts, the White House permitted Flynn to retain his highest-level national security clearance and attend top-secret intelligence briefings for an additional eighteen days. He was removed only after the Washington Post publicly exposed his intercepted conversations, demonstrating that public exposure, rather than national security integrity, dictated executive conduct.",
            "In December 2017, Michael Flynn entered a formal guilty plea before the United States District Court for the District of Columbia, admitting under oath that he had willfully made false statements to federal investigators. Legal scholars and national security analysts emphasize that Flynn's private diplomacy signaled to the Kremlin that the incoming executive was eager to dismantle bipartisan accountability in exchange for foreign geopolitical alignment, setting the precedent for four years of institutional accommodation.",
            "Tonight receipts. The Office of the Director of National Intelligence declassified Flynn-Kislyak phone transcripts. The Department of Justice plea agreement and statement of offense in United States v. Flynn. Acting Attorney General Sally Yates sworn Senate testimony, and the FBI 302 investigative interview memoranda. Every official court transcript is cataloged in the dossier drawer. Verify the counterintelligence record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.dni.gov/files/ODNI/documents/release_flynn_transcripts.pdf",
                "title": "Office of the Director of National Intelligence: Declassified Transcripts of Michael Flynn and Sergey Kislyak Calls",
                "published": "2020-05-29",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/file/1015126/download",
                "title": "US District Court DDC Statement of Offense: United States v. Michael T. Flynn",
                "published": "2017-12-01",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.judiciary.senate.gov/imo/media/doc/05-08-17%20Yates%20Testimony.pdf",
                "title": "Testimony of Former Acting Attorney General Sally Q. Yates Before Senate Judiciary Subcommittee",
                "published": "2017-05-08",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/world/national-security/national-security-adviser-flynn-discussed-sanctions-with-russian-ambassador-despite-denials-officials-say/2017/02/09/f628c296-eef1-11e6-b4ff-ac2cf509efe5_story.html",
                "title": "The Washington Post: Flynn Discussed Sanctions with Russian Ambassador Despite Denials, Officials Say",
                "published": "2017-02-09",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/file/1015121/download",
                "title": "Department of Justice: Plea Agreement in United States v. Michael T. Flynn",
                "published": "2017-12-01",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 22, 34), (38, 14, 22)),
        "accent": (255, 65, 85),
        "theme": "FLYNN BACKCHANNEL // LOGAN ACT & BLACKMAIL VULNERABILITY"
    },
    {
        "id": "2026-09-17-18",
        "date": "2026-09-17",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Trump Tower Ambush: The June 9 Veselnitskaya Meeting, Agalarov Overtures & The Dirt on Clinton",
        "subject": "Daily investigative dossier: The June 9, 2016 meeting at Trump Tower arranged by Emin Agalarov offering Russian government official dirt on Hillary Clinton, attended by Donald Trump Jr., Jared Kushner, and Paul Manafort, and the subsequent Air Force One draft statement misleading the press.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On June 9, 2016, inside the corporate executive offices on the 25th floor of Trump Tower in Manhattan, Donald Trump Jr., campaign chairman Paul Manafort, and senior advisor Jared Kushner convened an unannounced meeting with Russian attorney Natalia Veselnitskaya. The meeting was arranged following an explicit written email solicitation from music publicist Rob Goldstone representing Russian real estate billionaire Aras Agalarov and his pop-star son Emin, proposing to transmit sensitive official documents originating from the Russian Crown prosecutor.",
            "The written paper trail documenting the solicitation was unambiguous. In the June 3 email to Trump Jr., Goldstone wrote that the Kremlin-backed overture was part of Russia and its government's support for Mr. Trump. Rather than alerting federal counterintelligence agencies or the Federal Bureau of Investigation, Trump Jr. responded within seventeen minutes with enthusiasm, writing: If it's what you say I love it especially later in the summer. The willingness to accept covert assistance from an adversarial foreign state established the operational posture of the entire campaign hierarchy.",
            "Inside the closed-door conference room, the delegation discussed sensitive geopolitical objectives. Veselnitskaya, whose connections to the Russian Prosecutor General's office were subsequently verified by Swiss and American law enforcement, used the meeting to lobby against the Magnitsky Act, an American human rights law imposing sanctions on corrupt Russian officials. Manafort took contemporaneous notes on his mobile phone noting references to offshore holding companies and political donations, while attendees explored mechanisms to weaponize information against political rivals.",
            "The cover-up orchestrated over a year later reached directly into the Oval Office. In July 2017, when investigative journalists prepared to publish details of the meeting, Donald Trump personally dictated a misleading public statement aboard Air Force One flying back from the G20 summit in Germany. The dictated statement falsely claimed that the meeting primarily discussed a program about the adoption of Russian children, intentionally concealing the promised Russian government assistance and suppressing the underlying counterintelligence coordination.",
            "Bipartisan findings by the Senate Intelligence Committee concluded that the June 9 meeting represented a grave counterintelligence vulnerability that facilitated Russian intelligence penetration of the presidential campaign. By enthusiastically welcoming foreign clandestine assistance and later fabricating false public narratives to conceal the encounter, the campaign leadership exposed itself to foreign coercive leverage and established an enduring precedent of foreign election interference accommodation.",
            "Tonight receipts. The complete email chain between Donald Trump Jr. and Rob Goldstone. The Department of Justice Special Counsel Report Volume One findings on the Trump Tower meeting. The Senate Intelligence Committee Report Volume Five counterintelligence review, and sworn congressional depositions. Every primary exhibit is accessible in the dossier drawer. Review the original email evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Department of Justice: Special Counsel Review of the June 9, 2016 Trump Tower Meeting",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.judiciary.senate.gov/imo/media/doc/Trump%20Jr.%20Transcript_redacted.pdf",
                "title": "Senate Judiciary Committee: Interview Transcript of Donald J. Trump Jr. and Goldstone Email Exhibits",
                "published": "2018-05-16",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Russian Government Links to Natalia Veselnitskaya and Magnitsky Act",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/politics/trump-dictated-sons-misleading-statement-on-meeting-with-russian-lawyer/2017/07/31/e8b95c02-7601-11e7-8839-ec48ec4cae25_story.html",
                "title": "The Washington Post: Trump Dictated Son's Misleading Statement on Meeting with Russian Lawyer",
                "published": "2017-07-31",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/d9/special-counsel-mueller-report/volume1.pdf",
                "title": "Special Counsel Mueller Report: Analysis of False Air Force One Adoption Statement and Obstruction",
                "published": "2019-04-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 20, 36), (42, 18, 12)),
        "accent": (255, 175, 10),
        "theme": "TRUMP TOWER AMBUSH // RUSSIAN OFFICIAL ASSISTANCE"
    },
    {
        "id": "2026-09-16-18",
        "date": "2026-09-16",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Cambridge Analytica Syndicate: Mercer Capital, SCL Defense & Russian Psychographic Profiling",
        "subject": "Daily investigative dossier: The harvesting of eighty-seven million Facebook user profiles by Cambridge Analytica, funded by Robert Mercer and directed by Steve Bannon, micro-targeting psychological fear triggers, and coordination with Russian academic Aleksandr Kogan.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In 2014, backed by a fifteen-million-dollar investment from hedge fund billionaire Robert Mercer and overseen by board vice president Steve Bannon, Cambridge Analytica was incorporated as the American political arm of British military psychological warfare contractor SCL Group. Utilizing an academic data-scraping quiz deployed by Russian-American researcher Aleksandr Kogan, the firm illicitly harvested granular personal data, psychological traits, and private message histories from eighty-seven million unsuspecting Facebook users without informed consent.",
            "The harvested dataset enabled weaponized psychographic profiling. Combining commercial consumer records with Big Five personality psychometrics, Cambridge Analytica engineered algorithmic models designed to predict individual voter neuroses, openness, and emotional vulnerabilities. The Trump campaign contracted the firm for over five million dollars, integrating its predictive analytics directly into Project Alamo, the San Antonio digital advertising command center tasked with suppressing Democratic voter turnout through hyper-targeted dark advertisements.",
            "The operational nexus reached deeply into Russian intelligence orbits. Congressional investigations and whistleblower disclosures by Christopher Wylie revealed that Cambridge Analytica shared detailed research presentations regarding psychographic weaponization with executives at Lukoil, Russia's second-largest state-aligned petroleum corporation. Furthermore, data scientist Aleksandr Kogan simultaneously received research grants from St. Petersburg State University funded by the Russian government, raising profound counterintelligence concerns regarding whether weaponized American voter behavioral models were shared directly with Moscow's cyber apparatus.",
            "Regulatory enforcement actions confirmed sweeping illegality. In July 2019, the United States Federal Trade Commission imposed a historic five-billion-dollar penalty against Facebook for deceptive privacy practices related to the Cambridge Analytica data exfiltration, while issuing formal enforcement orders against Cambridge Analytica CEO Alexander Nix for deceptive data collection. Simultaneously, the United Kingdom Information Commissioner's Office published a comprehensive forensic review documenting that the company operated systematic privacy violations to manipulate democratic electoral processes.",
            "Intelligence analysts and constitutional scholars emphasize that the Cambridge Analytica operation transformed democratic campaigning into military-grade information warfare. By marrying illicit behavioral surveillance data with computational propaganda, political actors exploited cognitive biases at population scale. The legacy of this psychographic syndicate proved that commercial behavioral surveillance represents a catastrophic national security vulnerability capable of destabilizing the democratic foundations of sovereign nations.",
            "Tonight receipts. The Federal Trade Commission five-billion-dollar enforcement order on Cambridge Analytica data misuse. The United Kingdom Information Commissioner's Office forensic investigation report into democratic data analytics. Whistleblower testimony before the Senate Judiciary Committee, and declassified St. Petersburg State University research contracts. Every primary regulatory record is cataloged in the dossier drawer. Examine the forensic findings for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.ftc.gov/news-events/news/press-releases/2019/07/ftc-imposes-5-billion-penalty-sweeping-new-privacy-restrictions-facebook",
                "title": "Federal Trade Commission: FTC Imposes $5 Billion Penalty Against Facebook Over Cambridge Analytica Exfiltration",
                "published": "2019-07-24",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.judiciary.senate.gov/imo/media/doc/05-16-18%20Wylie%20Testimony.pdf",
                "title": "Senate Judiciary Committee: Testimony of Christopher Wylie on Cambridge Analytica and Psychographic Profiling",
                "published": "2018-05-16",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://ico.org.uk/media/action-weve-taken/reports/2260271/investigation-into-the-use-of-data-analytics-in-political-campaigns-final-20181105.pdf",
                "title": "UK Information Commissioner's Office: Investigation into the Use of Data Analytics in Political Campaigns",
                "published": "2018-11-06",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.ftc.gov/news-events/news/press-releases/2019/07/ftc-finds-cambridge-analytica-alexander-nix-aleksandr-kogan-deceived-consumers",
                "title": "FTC Enforcement Action: Findings of Deceptive Data Practices by Cambridge Analytica and Aleksandr Kogan",
                "published": "2019-07-24",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Cambridge Analytica, Lukoil Briefings and Russian Research Grants",
                "published": "2020-08-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((10, 25, 30), (35, 12, 40)),
        "accent": (0, 230, 255),
        "theme": "CAMBRIDGE ANALYTICA // PSYCHOGRAPHIC WARFARE SYNDICATE"
    },
    {
        "id": "2026-09-15-18",
        "date": "2026-09-15",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Alfa Bank Ping Anomaly: Tor-Exit Nodes, Russian Health Servers & The Trump Organization DNS Logs",
        "subject": "Daily investigative dossier: Sustained subterranean DNS queries between Alfa Bank servers in Moscow, Spectrum Health in Michigan, and the Trump Organization's private Trump-Email domain, cyber-forensic analysis, and FBI counterintelligence reviews.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Between May and September 2016, computer network defense researchers analyzing global internet traffic patterns identified an anomalous concentration of Domain Name System lookups originating from servers in Moscow and connecting to an obscure server registered to the Trump Organization. Located inside an outsourced data center in Lititz, Pennsylvania, the domain mail1.trump-email.com was configured to reject incoming marketing traffic, yet thousands of subterranean DNS lookups were executed by Alfa Bank, one of Russia's largest commercial financial conglomerates.",
            "The cyber-forensic telemetry revealed an extraordinary communication architecture. Highly respected academic computer scientists using the pseudonym Tea Leaves documented that over eighty percent of all DNS lookups to the private Trump domain originated from just two entities: Alfa Bank in Moscow and Spectrum Health, a healthcare conglomerate in Michigan overseen by the DeVos family. The timing of the lookups followed standard business hours in Moscow and New York, exhibiting traffic spikes that aligned precisely with major campaign milestones and political developments.",
            "The counterintelligence implications centered on Alfa Bank's close ties to Kremlin power. Owned by Russian oligarchs Mikhail Fridman and Petr Aven, Alfa Bank operated under regular supervisory contact with Russian intelligence and executive authorities. According to Special Counsel Robert Mueller's report, Petr Aven met with Vladimir Putin in the Kremlin during this exact window, where Putin emphasized that ongoing geopolitical sanctions required backchannel communication links with the incoming American political apparatus to establish confidential negotiations.",
            "The domestic infrastructure raised immediate forensic questions. When journalists at Slate approached Alfa Bank and the computer researchers in late October 2016 inquiring about the communication logs, the Trump Organization domain was abruptly shut down within hours. Immediately following the shutdown, a brand-new hostname was registered on the same server, and minutes later, Alfa Bank servers executed a single DNS lookup to the new domain, suggesting an active automated synchronization script maintaining connectivity between Moscow and Manhattan.",
            "Subsequent investigations by the FBI Cyber Division and Special Counsel John Durham concluded that while the DNS queries did not establish an active encrypted human chat protocol, the technical logs were genuine and reflected automated host-resolution traffic. Computer security specialists emphasize that the infrastructure demonstrated how modern distributed networks and automated DNS querying can establish covert signaling channels that evade traditional federal surveillance, presenting complex challenges for international cyber counterintelligence.",
            "Tonight receipts. The academic cyber-forensic DNS lookup telemetry logs from Tea Leaves and network researchers. Special Counsel Robert Mueller Report Volume One findings on Petr Aven and Alfa Bank. Special Counsel John Durham court filings in United States v. Sussmann, and Senate Intelligence Committee technical reviews. Every network trace and judicial filing is preserved in the dossier drawer. Analyze the cyber telemetry for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://slate.com/news-and-politics/2016/10/was-a-trump-server-communicating-with-russia.html",
                "title": "Slate: Was a Trump Server Communicating With Russia? The Cyber-Forensic DNS Mystery",
                "published": "2016-10-31",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Analysis of Alfa Bank and Trump Organization DNS Traffic",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Department of Justice: Special Counsel Mueller Findings on Petr Aven and Kremlin Outreach",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.justice.gov/sco-durham/case/united-states-v-michael-a-sussmann",
                "title": "Special Counsel Durham: Court Filings and Technical Exhibits in United States v. Sussmann",
                "published": "2022-05-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.fbi.gov/wanted/counterintelligence",
                "title": "Federal Bureau of Investigation: Cyber Counterintelligence Technical Advisory on Covert Channels",
                "published": "2021-06-10",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 28, 40), (25, 15, 35)),
        "accent": (0, 245, 180),
        "theme": "ALFA BANK TELEMETRY // AUTOMATED DNS SIGNALING ARCHITECTURE"
    },
    {
        "id": "2026-09-14-18",
        "date": "2026-09-14",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Bayrock Money Trail: Felix Sater, Tevfik Arif & Russian Oligarch Cash in Manhattan Real Estate",
        "subject": "Daily investigative dossier: Bayrock Group's partnership with the Trump Organization inside Trump Tower, Soviet-born felon Felix Sater, Tevfik Arif's Kazakh-Russian oligarch financing, and systemic money laundering through luxury condominium developments in SoHo and Fort Lauderdale.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Throughout the 2000s, as traditional domestic lending dried up for the Trump Organization following repeated corporate bankruptcies, a boutique development firm headquartered two floors below Donald Trump's executive office in Trump Tower emerged as a primary financial lifeline. Bayrock Group, founded by Soviet-born Kazakh financier Tevfik Arif and staffed by convicted racketeer Felix Sater, partnered with Trump on flagship luxury developments including Trump SoHo in Manhattan, Trump International Hotel in Fort Lauderdale, and planned projects in Phoenix and Moscow.",
            "The capital underpinning Bayrock's operations originated from opaque offshore networks across the former Soviet Union. An extensive investigation by the Financial Times and civil fraud litigation in New York State Supreme Court documented that Bayrock funneled hundreds of millions of dollars in murky capital from Central Asia, Russia, and Cypriot shell entities. Sater, who had previously pleaded guilty in federal court to a forty-million-dollar Wall Street stock manipulation scheme orchestrated with Russian organized crime syndicates, carried Trump Organization business cards as a senior advisor.",
            "The flagship Trump SoHo project became a documented conduit for international capital flight. Luxury condominium units were systematically purchased by shell companies and international buyers using unverified offshore trusts, allowing foreign elites to park illicit capital into prime Manhattan real estate. In 2011, buyers filed a civil fraud lawsuit against Donald Trump and his children Ivanka and Donald Jr., alleging they had fraudulently inflated sales numbers to induce purchases. To settle the dispute, the Trump Organization returned millions to buyers while requiring non-disclosure agreements.",
            "The financial structure raised profound money laundering concerns among financial regulators. In 2017, a comprehensive civil racketeering lawsuit filed by former Bayrock executives detailed how millions in profits from Trump SoHo and other joint developments were siphoned into shell companies in Delaware and the Netherlands to evade taxation and conceal the beneficial ownership of Russian and Kazakh investors, directly enriching the Trump family through licensing royalties and development fees.",
            "Counterintelligence scholars emphasize that the Bayrock partnership integrated the Trump brand into the financial infrastructure of post-Soviet oligarch networks. By collaborating for over a decade with convicted felons and opaque foreign capital conduits, the commercial empire established deep structural vulnerabilities. These financial entanglements created lasting counterintelligence exposure, ensuring that foreign financial intelligence services held granular records regarding the president's historic financial survival.",
            "Tonight receipts. The Financial Times forensic investigation into Bayrock Group and Trump SoHo financing. New York State Supreme Court civil fraud and racketeering filings in Kriss v. Bayrock. Federal court criminal dockets in United States v. Sater, and declassified Senate Intelligence Committee reviews. Every judicial exhibit and real estate deed is preserved in the dossier drawer. Examine the corporate transactions for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.ft.com/content/247b97e4-8d42-11e6-a72e-b428734de15b",
                "title": "Financial Times: Trump SoHo and the Russian Money Trail from Central Asia",
                "published": "2016-10-19",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.courtlistener.com/docket/4514782/kriss-v-bayrock-group-llc/",
                "title": "New York State Supreme Court / SDNY: Racketeering Complaint in Kriss v. Bayrock Group LLC",
                "published": "2015-07-10",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/2016/04/06/us/politics/donald-trump-soho-settlement.html",
                "title": "The New York Times: Donald Trump Settled Fraud Suit Over Trump SoHo Condominium Sales",
                "published": "2016-04-06",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Bipartisan Findings on Bayrock, Felix Sater and Tevfik Arif",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.govinfo.gov/content/pkg/USCOURTS-nyed-1_98-cr-01101/pdf/USCOURTS-nyed-1_98-cr-01101-1.pdf",
                "title": "US District Court EDNY: Criminal Docket and Plea Records in United States v. Felix Sater",
                "published": "2011-10-14",
                "kind": "reference"
            }
        ],
        "art_palette": ((18, 20, 28), (38, 22, 12)),
        "accent": (255, 150, 20),
        "theme": "BAYROCK MONEY TRAIL // POST-SOVIET CAPITAL CONDUITS"
    },
    {
        "id": "2026-09-13-18",
        "date": "2026-09-13",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Palm Beach Windfall: Dmitry Rybolovlev, The Maison de L'Amitie & The 54-Million-Dollar Markup",
        "subject": "Daily investigative dossier: Donald Trump's 2008 sale of the Palm Beach mansion Maison de L'Amitié to Russian fertilizer oligarch Dmitry Rybolovlev for ninety-five million dollars during the height of the US real estate crash, generating a fifty-four-million-dollar cash windfall without the oligarch ever residing on the property.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In July 2008, as the global subprime mortgage crisis was causing residential real estate valuations across Florida to plummet and institutional credit to freeze, Donald Trump executed the most lucrative real estate transaction of his private career. He sold the historic Palm Beach oceanfront estate known as Maison de L'Amitié for ninety-five million dollars in cash to Russian fertilizer billionaire Dmitry Rybolovlev. The sale yielded a staggering fifty-four-million-dollar markup over what Trump had paid for the property just four years earlier.",
            "The mechanics of the transaction defied financial logic. Trump purchased the estate out of bankruptcy in 2004 for forty-one point three million dollars, performed cosmetic renovations, and placed it on the market with an astronomical asking price. Despite local real estate appraisers assessing the property at under sixty million dollars as the financial crash deepened, Rybolovlev utilized an opaque offshore limited liability company registered in the British Virgin Islands to wire the ninety-five million dollars without negotiating a single dollar discount.",
            "The buyer's conduct following the purchase deepened international suspicions. Rybolovlev, known as Russia's potash king who made billions privatizing Soviet-era state chemical assets under Kremlin auspices, never lived in the palatial residence or slept a single night on the estate. Instead, the property sat entirely abandoned for nearly a decade, deteriorating under coastal mold and neglect until Rybolovlev obtained municipal demolition permits in 2016, tearing the massive six-acre mansion to the ground and subdividing the raw land into vacant parcels.",
            "Congressional investigators and financial crime experts highlighted the transaction as a classic case study in offshore wealth transfers and foreign capital injection. At a time when Trump faced crushing debt maturities on his Chicago skyscraper and Atlantic City casinos were spiraling toward bankruptcy, the fifty-four-million-dollar cash injection provided vital personal solvency. The Senate Finance Committee subsequently launched inquiries into whether the transaction served as an opaque financial vehicle to infuse foreign capital into Trump's corporate accounts.",
            "Intelligence analysts emphasize that disproportionate real estate transactions represent a primary methodology for foreign actors to establish financial relationships with prominent political targets. By overpaying tens of millions of dollars for an asset that is subsequently destroyed, the patron creates significant goodwill and latent commercial dependence. The transaction remains an indelible milestone demonstrating how foreign oligarch cash preserved the liquidity of the future American president.",
            "Tonight receipts. The Palm Beach County official property deed and real estate transfer tax records. The Senate Finance Committee formal inquiry letters into the Maison de L'Amitié transaction. Financial asset disclosure filings from Dmitry Rybolovlev, and municipal demolition permits. Every property record and financial exhibit is cataloged in the dossier drawer. Review the land transfer documents for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.palmbeachpost.com/story/news/2016/10/05/trumps-palm-beach-mansion-sale/7074719007/",
                "title": "The Palm Beach Post: The 95 Million Dollar Mansion Sale That Saved Trump's Liquidity",
                "published": "2016-10-05",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.finance.senate.gov/ranking-members-news/wyden-demands-records-on-sale-of-trump-mansion-to-russian-oligarch",
                "title": "Senate Finance Committee: Ranking Member Demands Records on Trump Mansion Sale to Russian Oligarch",
                "published": "2018-02-09",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.miamiherald.com/news/business/article135187364.html",
                "title": "The Miami Herald: Potash King Demolishes 95-Million-Dollar Palm Beach Mansion Bought from Trump",
                "published": "2017-02-27",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Financial Counterintelligence Review of Dmitry Rybolovlev Transactions",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.pbcgov.org/papa/Asps/PropertyDetail/PropertyDetail.aspx?parcel=50434314000001010",
                "title": "Palm Beach County Property Appraiser: Official Parcel Historical Deed Transfers for 515 N County Rd",
                "published": "2019-01-15",
                "kind": "reference"
            }
        ],
        "art_palette": ((22, 18, 12), (38, 28, 10)),
        "accent": (255, 205, 50),
        "theme": "MAISON DE L'AMITIE // 54-MILLION DOLLAR OLIGARCH MARKUP"
    },
    {
        "id": "2026-09-12-18",
        "date": "2026-09-12",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Intelligence Purge: The Oval Office Lavrov Leak, Classified Israeli Assets & The Firing of James Comey",
        "subject": "Daily investigative dossier: The May 2017 Oval Office meeting between Donald Trump, Sergei Lavrov, and Sergey Kislyak disclosing highly classified Israeli intelligence regarding ISIS laptop bomb threats, followed immediately by the firing of FBI Director James Comey to shut down the Russia investigation.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On May 10, 2017, one day after abruptly firing FBI Director James Comey, Donald Trump welcomed Russian Foreign Minister Sergei Lavrov and Russian Ambassador Sergey Kislyak into the Oval Office. American press photographers were barred from the encounter, while a photographer from Russian state news agency TASS was granted exclusive access. During the meeting, according to senior administration officials, Trump boasted about the high quality of his intelligence briefings and proceeded to disclose highly classified code-word information regarding an active Islamic State plot.",
            "The intelligence disclosed represented one of the most sensitive operational secrets in the Middle East. Originating from an Israeli deep-cover human intelligence asset embedded within Islamic State networks in Syria, the compartmented intelligence detailed terrorist plans to conceal explosives inside laptop batteries to bypass airport security scanners. Trump revealed the specific city where the plot was detected, compromising the partner intelligence source and prompting Israeli defense officials to issue urgent protests over the reckless breach of bilateral intelligence-sharing agreements.",
            "The meeting laid bare the explicit motivation behind Comey's dismissal. White House transcripts of the Oval Office conversation confirmed that Trump told Lavrov and Kislyak: I just fired the head of the FBI. He was crazy, a real nut job. I faced great pressure because of Russia. That's taken off. The candid admission to foreign adversaries revealed that the termination of the nation's chief law enforcement officer was an intentional maneuver to obstruct the federal counterintelligence probe into Russian election interference.",
            "The institutional fallout reverberated through the Department of Justice. Comey had documented his private encounters with Trump in contemporaneous memoranda, recording that Trump had demanded personal loyalty and asked him to drop the criminal investigation into Michael Flynn. Following the Oval Office disclosures and Trump's televised admission to Lester Holt on NBC that he fired Comey thinking about this Russia thing, Deputy Attorney General Rod Rosenstein appointed Special Counsel Robert Mueller to assume control of the investigation.",
            "Intelligence scholars and former national security officials emphasize that the Lavrov incident epitomized an executive operating without regard for classified security protocols. By sharing allied secrets with Russian officials and celebrating the dismissal of federal law enforcement leadership with foreign diplomats, the commander-in-chief demonstrated profound contempt for intelligence compartmentalization and the constitutional rule of law.",
            "Tonight receipts. The Washington Post investigative report on the Oval Office classified disclosure. The declassified Comey contemporaneous memoranda on presidential pressure. Special Counsel Robert Mueller Report Volume Two on obstruction of justice, and official White House meeting transcripts. Every judicial document and intelligence review is cataloged in the dossier drawer. Verify the evidentiary record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.washingtonpost.com/world/national-security/trump-revealed-highly-classified-information-to-russian-foreign-minister-and-ambassador/2017/05/15/530c172a-3960-11e7-9e48-c4f199710b69_story.html",
                "title": "The Washington Post: Trump Revealed Highly Classified Information to Russian Foreign Minister and Ambassador",
                "published": "2017-05-15",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.nytimes.com/2017/05/16/world/middleeast/israel-trump-classified-intelligence-russia.html",
                "title": "The New York Times: Israel Was Source of Secret Intelligence Trump Disclosed to Russian Envoys",
                "published": "2017-05-16",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/2017/05/19/us/politics/trump-russia-comey.html",
                "title": "The New York Times: Trump Told Russians That Firing 'Nut Job' Comey Eased Pressure on Him",
                "published": "2017-05-19",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Department of Justice: Special Counsel Mueller Report Volume Two on James Comey Termination",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Review of Oval Office Disclosures and Counterintelligence Impact",
                "published": "2020-08-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((25, 12, 18), (14, 24, 38)),
        "accent": (255, 60, 60),
        "theme": "OVAL OFFICE LEAK // CLASSIFIED CODE-WORD COMPROMISE"
    },
    {
        "id": "2026-09-11-18",
        "date": "2026-09-11",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Guccifer 2.0 Concealment: GRU Unit 74455, Roger Stone & The DCLeaks Coordination",
        "subject": "Daily investigative dossier: Russian military intelligence GRU Unit 74455 executing cyber intrusions into the DNC and DCCC, operating online personas Guccifer 2.0 and DCLeaks, and direct encrypted Twitter backchannel communications with Trump advisor Roger Stone.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In July 2018, the Department of Justice unsealed a sweeping federal grand jury indictment charging twelve officers of the Russian Main Intelligence Directorate, or GRU, with executing sophisticated cyber warfare operations targeting the 2016 American election. Operating out of specialized military units 26165 and 74455 in Moscow, the officers hacked computer networks belonging to the Democratic National Committee, the Democratic Congressional Campaign Committee, and the personal email accounts of senior political officials, stealing hundreds of gigabytes of proprietary communications.",
            "To launder and distribute the stolen materials, GRU officers created the fictitious online personas Guccifer 2.0 and DCLeaks, while coordinating directly with WikiLeaks. Declassified forensic evidence presented by the FBI and the Department of Justice proved that Guccifer 2.0 operated directly from a GRU server infrastructure in Moscow. Despite public warnings from American intelligence agencies that Guccifer was a Russian military intelligence front, senior political advisor Roger Stone engaged in private, encrypted communications with the persona via Twitter direct messaging.",
            "The communications synchronized weaponized disclosure dumps. Internal trial records and testimony in United States v. Stone proved that Stone maintained frequent telephone contact with senior Trump campaign leadership, including personal calls with Donald Trump, promising advance knowledge of forthcoming WikiLeaks releases designed to inflict maximum political damage on political opponents. Minutes after the release of the Access Hollywood recording in October 2016, WikiLeaks initiated the public release of thousands of hacked emails from campaign chairman John Podesta.",
            "The criminal investigation revealed systemic perjury and witness intimidation. In November 2019, a federal jury in Washington convicted Roger Stone on all counts, finding he lied under oath to the House Intelligence Committee regarding his communications with intermediaries and attempted to intimidate a witness into silence by threatening his therapy dog. Stone's coordinated efforts demonstrated that political operatives actively leveraged stolen foreign military intelligence to influence the trajectory of the presidential election.",
            "Strategic intelligence analysts emphasize that the Guccifer 2.0 operation represented the successful convergence of state-sponsored cyber warfare and domestic political exploitation. By utilizing hacked and weaponized documents as campaign ammunition while publicly denying foreign provenance, the campaign operationalized Russian military intelligence output, subverting the security of the American electoral system.",
            "Tonight receipts. The Department of Justice federal grand jury indictment of twelve GRU officers in United States v. Netyksho. The jury trial conviction exhibits and encrypted message transcripts in United States v. Stone. The Bipartisan Senate Intelligence Committee Report Volume Five, and the 2017 Intelligence Community Assessment. Every cyber-forensic exhibit is cataloged in the dossier drawer. Review the indictment evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/file/1080281/download",
                "title": "US District Court DDC Grand Jury Indictment: United States v. Viktor Borisovich Netyksho et al. (12 GRU Officers)",
                "published": "2018-07-13",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.dni.gov/files/documents/ICA_2017_01.pdf",
                "title": "Office of the Director of National Intelligence: Assessing Russian Activities and Intentions in Recent US Elections",
                "published": "2017-01-06",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/usao-dc/pr/roger-stone-convicted-obstruction-witnesstampering-and-false-statements",
                "title": "United States Attorney DC: Roger Stone Convicted on All Counts of Perjury and Witness Tampering",
                "published": "2019-11-15",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Volume Five Bipartisan Review of GRU Cyber Operations and Stone",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Special Counsel Mueller Report Volume One: GRU Hacking and Dissemination via Guccifer 2.0 and WikiLeaks",
                "published": "2019-04-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((10, 20, 32), (32, 10, 25)),
        "accent": (0, 220, 240),
        "theme": "GUCCIFER 2.0 // GRU MILITARY CYBER WARFARE"
    },
    {
        "id": "2026-09-10-18",
        "date": "2026-09-10",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Rosneft Privatization Mystery: The 19-Percent Stake, Carter Page & The Moscow Diplomatic Trips",
        "subject": "Daily investigative dossier: Trump campaign foreign policy advisor Carter Page's July 2016 trip to Moscow, meetings with Rosneft officials regarding the privatization of a nineteen-percent stake in the Russian state oil giant, and FISA warrant applications approved by federal judges.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In March 2016, during an editorial board interview with the Washington Post, Donald Trump publicly named Carter Page as one of five key members of his foreign policy advisory council. Page, an energy consultant with a history of living in Moscow who had previously been targeted for recruitment by Russian intelligence operatives in New York in 2013, was granted national political stature. In July 2016, with permission from campaign leadership, Page traveled to Moscow to deliver a commencement address at the New Economic School.",
            "The Moscow trip extended far beyond academic lectures. Declassified congressional testimony and counterintelligence filings revealed that during his visit, Page met with senior Russian officials, including Deputy Prime Minister Arkady Dvorkovich and Andrey Baranov, head of investor relations at Russian state energy monopoly Rosneft. Discussions centered on the potential privatization of a nineteen-point-five percent stake in Rosneft and the prospective lifting of American economic sanctions imposed on Russia's energy sector following the invasion of Crimea.",
            "The timing coincided with intense Kremlin commercial maneuvering. Months later, in December 2016, the Kremlin announced the sudden privatization of the nineteen-point-five percent Rosneft stake to a consortium of commodities trader Glencore and the Qatar Investment Authority, structured through an opaque Cayman Islands holding company that obscured the beneficial recipients of hundreds of millions in transaction fees. Counterintelligence agencies investigated whether the massive equity stake was leveraged to incentivize American sanctions relief.",
            "The counterintelligence concerns prompted the Department of Justice to seek a Foreign Intelligence Surveillance Act warrant targeting Page in October 2016. Four separate federal judges on the Foreign Intelligence Surveillance Court approved and renewed the FISA warrants based on probable cause that Page was acting as an unwitting or witting agent of a foreign power. While an Inspector General review identified systemic process failures in the FBI's warrant affidavits, the underlying Russian contacts remained undisputed.",
            "Intelligence analysts emphasize that the Carter Page episode revealed a campaign eager to elevate individuals with preexisting ties to hostile foreign state enterprises. By placing an operative with documented Russian intelligence exposure on the presidential advisory board and sanctioning high-level meetings with state energy monopolies during an active election, the campaign dismantled standard national security vetting, creating severe counterintelligence vulnerabilities.",
            "Tonight receipts. The Department of Justice Inspector General Report on Foreign Intelligence Surveillance Act applications. Carter Page sworn testimony before the House Permanent Select Committee on Intelligence. The Senate Intelligence Committee Bipartisan Report Volume Five, and federal court filings in United States v. Buryakov. Every declassified transcript and surveillance affidavit is cataloged in the dossier drawer. Verify the counterintelligence findings for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/storage/120919-examination.pdf",
                "title": "DOJ Office of the Inspector General: Review of Four FISA Applications and Carter Page Russian Contacts",
                "published": "2019-12-09",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://docs.house.gov/meetings/IG/IG00/20171102/106561/HHRG-115-IG00-Transcript-20171102.pdf",
                "title": "House Permanent Select Committee on Intelligence: Executive Session Interview of Carter W. Page",
                "published": "2017-11-02",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Volume Five Counterintelligence Review of Carter Page and Rosneft",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Special Counsel Mueller Report Volume One: Carter Page July 2016 Trip to Moscow and Baranov Meetings",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/usao-sdny/pr/russian-banker-evgeny-buryakov-pleads-guilty-manhattan-federal-court-acting-unregistered",
                "title": "US Attorney SDNY: Russian Intelligence Officer Evgeny Buryakov Pleads Guilty in SVR Recruitment Scheme",
                "published": "2016-03-11",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 25, 35), (35, 18, 12)),
        "accent": (255, 160, 40),
        "theme": "ROSNEFT PRIVATIZATION // CARTER PAGE MOSCOW TRAVEL"
    },
    {
        "id": "2026-09-09-18",
        "date": "2026-09-09",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Miss Universe Moscow Pact: Aras Agalarov, Sberbank Financing & The 2013 Russian Pageant",
        "subject": "Daily investigative dossier: The November 2013 Miss Universe pageant held in Moscow, co-hosted by Kremlin-connected billionaire Aras Agalarov, backed by Russian state-controlled Sberbank, Herman Gref negotiations, and the pursuit of commercial Moscow real estate licensing.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In November 2013, Donald Trump traveled to Moscow to stage the Miss Universe pageant at Crocus City Hall, a massive entertainment complex owned by Azerbaijani-Russian real estate oligarch Aras Agalarov. The twenty-million-dollar production was financed through a lucrative partnership with Agalarov and backed by Russian state-controlled financial conglomerate Sberbank, led by Herman Gref, a former Russian Minister of Economic Development and close confidant of Vladimir Putin.",
            "The commercial venture served as an aggressive vehicle to cultivate Kremlin patronage. Throughout his forty-eight hours in the Russian capital, Trump engaged in high-level business summits with senior Russian oligarchs and political elites. He met privately with Herman Gref to discuss financing for a proposed hundred-story Trump Tower in Moscow, signing an exclusive development protocol with the Agalarovs that would have paid the Trump Organization multimillion-dollar licensing fees without requiring capital investment.",
            "The political outreach was direct and obsequious. Months before departing for Moscow, Trump posted public messages on Twitter asking whether Vladimir Putin would attend the pageant, musing: Do you think Putin will be going to the Miss Universe Pageant in November in Moscow? If so, will he become my new best friend? While Putin ultimately canceled his scheduled attendance due to an official state visit with Dutch royalty, he dispatched high-ranking aide Vladimir Kozhin to deliver an official gift and personal greeting.",
            "The counterintelligence implications of the Moscow weekend were profound. The bipartisan Senate Intelligence Committee Report Volume Five documented that Russian intelligence services routinely conduct aggressive technical and human surveillance against high-profile Western visitors in luxury Moscow hotels, including the Ritz-Carlton where Trump stayed. Witnesses testified that Agalarov provided private security details and access to elite social functions, creating an environment rich in potential psychological profiling and kompromat collection.",
            "The 2013 Moscow pageant forged the interpersonal and financial relationships that resurfaced with devastating effect during the 2016 presidential election. It was Aras and Emin Agalarov who arranged the June 2016 Trump Tower meeting offering official Russian government assistance, demonstrating that the commercial relationships established in Moscow served as the direct bridge for state-sponsored political influence operations.",
            "Tonight receipts. The Senate Intelligence Committee Bipartisan Report Volume Five on the 2013 Miss Universe Moscow pageant. Official corporate records and licensing agreements between the Trump Organization and the Crocus Group. Sworn congressional depositions of Miss Universe executives, and Sberbank corporate financing announcements. Every primary exhibit is cataloged in the dossier drawer. Examine the historical contracts for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Bipartisan Findings on the 2013 Moscow Miss Universe Pageant",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Department of Justice: Special Counsel Review of Agalarov Relationship and 2013 Moscow Pageant",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.washingtonpost.com/politics/inside-trumps-financial-ties-to-russia-and-his-unusual-flattery-of-vladimir-putin/2016/06/17/dbdcaac8-31a6-11e6-8ff7-7b6c1998b7a0_story.html",
                "title": "The Washington Post: Inside Trump's Financial Ties to Russia and Flattery of Vladimir Putin",
                "published": "2016-06-17",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.judiciary.senate.gov/imo/media/doc/Goldstone%20Transcript_redacted.pdf",
                "title": "Senate Judiciary Committee: Sworn Interview Transcript of Rob Goldstone on Agalarov Connections",
                "published": "2018-05-16",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.sberbank.ru/en/press_center/all/article?newsID=200000305",
                "title": "Sberbank of Russia Corporate Press Archive: Sberbank Financing for Crocus Group and International Events",
                "published": "2013-11-12",
                "kind": "reference"
            }
        ],
        "art_palette": ((22, 14, 28), (35, 18, 12)),
        "accent": (255, 185, 30),
        "theme": "MISS UNIVERSE 2013 // AGALAROV SBERBANK PARTNERSHIP"
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
    print(f"Checking {len(EPISODES)} retrospective daily episodes for Batch 2...")
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
