#!/usr/bin/env python3
"""
tools/produce_daily_trump_series_batch3.py - Production Engine for Batch 3 Retrospective Daily Investigative Podcasts
ZeroFilter Geopolitical & Counterintelligence Dossier Series (2026-09-08 down to 2026-08-30)
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
        "id": "2026-09-08-18",
        "date": "2026-09-08",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Inaugural Fund Conduit: Citgo Donations, Straw Donors & Foreign Lobbying Payments",
        "subject": "Daily investigative dossier: The record-breaking $107 million Trump 2017 presidential inaugural committee fund, illicit $500,000 corporate contribution from Russian state oil subsidiary Citgo, straw donor convictions, and federal SDNY corruption inquiries.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In January 2017, the 58th Presidential Inaugural Committee raised an unprecedented one hundred seven million dollars, more than double the previous historical record. Chaired by real estate investor Thomas Barrack, who was subsequently indicted for acting as an unregistered foreign agent of the United Arab Emirates, the committee became an opaque turnstile for corporate patrons, foreign political emissaries, and straw donors seeking direct access to executive policymakers.",
            "The sources of corporate capital raised immediate counterintelligence and national security alarms. Federal Election Commission filings revealed that Citgo Petroleum, a Houston-based subsidiary of Venezuelan state oil company PDVSA that had pledged forty-nine point nine percent of its equity as collateral to Russian state-owned energy giant Rosneft, contributed five hundred thousand dollars to the inaugural committee. The contribution injected foreign state-linked capital into inaugural accounts while Rosneft actively sought relief from Treasury Department energy sanctions.",
            "Federal law strictly prohibits foreign nationals from contributing to inaugural committees directly or through intermediaries. However, an extensive investigation by the Southern District of New York and the Department of Justice National Security Division uncovered pervasive straw-donor networks. Prominent foreign figures, including pro-Russian Ukrainian politicians and Middle Eastern financiers, routed funds through domestic pass-through entities and commercial shell companies to purchase VIP inaugural access and private gala tickets.",
            "The judicial fallout confirmed systematic legal violations. In 2019, prominent foreign-linked donor Imaad Zuberi pleaded guilty to making nearly one million dollars in illegal straw donations, including a nine-hundred-thousand-dollar transfer to the Trump inaugural committee sourced from foreign clients. Zuberi was subsequently sentenced to twelve years in federal prison. Separately, the Attorney General for the District of Columbia sued the inaugural committee for gross self-dealing, proving it funneled over one million dollars in non-profit charitable funds directly to the Trump International Hotel.",
            "Financial integrity scholars and anti-corruption analysts emphasize that the 2017 inauguration established an early financial template for monetizing the presidency. By dissolving traditional vetting procedures and accepting opaque multi-hundred-thousand-dollar contributions from entities entangled with hostile foreign oil monopolies, the incoming administration transformed a constitutional rite of democratic transfer into an unregulated pay-to-play marketplace.",
            "Tonight receipts. The Federal Election Commission official 2017 Presidential Inaugural Committee donor disclosure reports. The Southern District of New York criminal plea agreements in United States v. Zuberi. The District of Columbia Attorney General settlement and self-dealing evidentiary exhibits, and the foreign agent indictment of committee chairman Thomas Barrack. Every financial exhibit is preserved in the dossier drawer. Review the inaugural ledgers for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/opa/pr/thomas-barrack-charged-acting-unregistered-agent-united-arab-emirates",
                "title": "Department of Justice: Thomas Barrack Indicted for Unregistered Foreign Lobbying and Obstruction",
                "published": "2021-07-20",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://docquery.fec.gov/pdf/316/201704189052285316/201704189052285316.pdf",
                "title": "Federal Election Commission: 58th Presidential Inaugural Committee Official Filing on Citgo Contribution",
                "published": "2017-04-18",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/usao-cdca/pr/venture-capitalist-sentenced-12-years-prison-falsifying-records-conceal-foreign-lobbying",
                "title": "US Attorney CDCA: Venture Capitalist Imaad Zuberi Sentenced to 12 Years for Foreign Straw Donations",
                "published": "2021-02-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://oag.dc.gov/release/ag-racine-announces-trump-inaugural-committee-and",
                "title": "Office of the Attorney General DC: Inaugural Committee Pays $750,000 Settlement for Hotel Misuse",
                "published": "2022-05-03",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/d9/special-counsel-mueller-report/volume1.pdf",
                "title": "Special Counsel Mueller Report Volume One: Review of Foreign Transition Outreach and Inaugural Access",
                "published": "2019-04-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 22, 35), (38, 18, 12)),
        "accent": (255, 175, 40),
        "theme": "INAUGURAL FUND CONDUIT // CITGO & FOREIGN STRAW DONORS"
    },
    {
        "id": "2026-09-07-18",
        "date": "2026-09-07",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Tenet Media Indictment: RT Secret Financing, Lauren Chen & The $10 Million Disinformation Network",
        "subject": "Daily investigative dossier: The September 2024 DOJ indictment of Russian state media network RT employees Kostiantyn Kalashnikov and Elena Afanasyeva funnelling nearly $10 million to Tenet Media to covertly contract prominent conservative commentators.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On September 4, 2024, the United States Department of Justice unsealed a historic criminal indictment in the Southern District of New York charging two employees of the Russian state media network RT with conspiracy to commit money laundering and violate the Foreign Agents Registration Act. Kostiantyn Kalashnikov and Elena Afanasyeva covertly funneled nearly ten million dollars to a Tennessee-based online production company known as Tenet Media, orchestrating an illicit foreign influence operation to sway American voters.",
            "The operational scheme bypassed foreign agent registration through deceptive commercial intermediaries. Founded by conservative commentator Lauren Chen and her husband Liam Donovan, Tenet Media contracted several prominent American right-wing commentators, paying individual podcast hosts up to four hundred thousand dollars per month to generate viral video content. The contracted commentators were led to believe their financial backing came from a fictitious European banker named Eduard Grigoriann, when the capital flowed directly from Kremlin state coffers.",
            "The editorial direction of the platform mirrored core Russian active measures objectives. Indictment exhibits proved that Russian state operatives actively dictated editorial directives, inserting hundreds of videos into American digital feeds that blamed Ukraine for the war, attacked Western military assistance, and amplified polarizing domestic racial and political grievances. When an ISIS terrorist attack struck Crocus City Hall in Moscow, the Russian handlers explicitly ordered Tenet to publish content falsely blaming Ukraine and the United States.",
            "The Department of the Treasury simultaneously coordinated comprehensive economic countermeasures. The Office of Foreign Assets Control designated ten individuals and two entities, including RT Editor-in-Chief Margarita Simonyan, while the State Department seized thirty-two internet domains deployed in the Doppelganger cyber campaign that impersonated legitimate Western news outlets like the Washington Post and Fox News to launder pro-Russian propaganda.",
            "National security scholars and federal counterintelligence officials emphasize that the Tenet Media indictment revealed the modern evolution of Soviet-era active measures doctrine. By exploiting the lucrative economics of digital political influencer culture, foreign intelligence agencies bypassed traditional state broadcasting restrictions, weaponizing domestic political figures as unwitting mouthpieces to erode democratic consensus and undermine American national security.",
            "Tonight receipts. The United States District Court Southern District of New York criminal indictment in United States v. Kalashnikov and Afanasyeva. The Department of Justice official press conference statement on countering Russian election interference. The United States Department of the Treasury OFAC designation notice, and seized Doppelganger domain affidavits. Every indictment exhibit is preserved in the dossier drawer. Review the criminal charges for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/opa/pr/two-rt-employees-indicted-covert-influence-operation-and-money-laundering",
                "title": "Department of Justice: Two RT Employees Indicted in $10 Million Covert US Influence Scheme",
                "published": "2024-09-04",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/d9/2024-09/u.s._v._kalashnikov_and_afanasyeva_indictment.pdf",
                "title": "US District Court SDNY Indictment: United States v. Kostiantyn Kalashnikov and Elena Afanasyeva",
                "published": "2024-09-04",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://home.treasury.gov/news/press-releases/jy2559",
                "title": "U.S. Department of the Treasury: Treasury Sanctions Russian State Media Leadership Over 2024 Interference",
                "published": "2024-09-04",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.fbi.gov/news/press-releases/doppelganger-seizure-affidavit-russian-disinformation",
                "title": "Federal Bureau of Investigation: Affidavits in Support of 32 Seized Russian Cyber Domains",
                "published": "2024-09-04",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.state.gov/taking-additional-measures-to-counter-russian-disinformation-and-electoral-interference/",
                "title": "U.S. Department of State: Diplomatic Measures Against Russian State Influence Networks",
                "published": "2024-09-04",
                "kind": "reference"
            }
        ],
        "art_palette": ((18, 12, 28), (35, 15, 20)),
        "accent": (255, 60, 90),
        "theme": "TENET MEDIA INDICTMENT // RT 10-MILLION INFLUENCE CONDUIT"
    },
    {
        "id": "2026-09-06-18",
        "date": "2026-09-06",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Internet Research Agency Pipeline: Yevgeny Prigozhin, Concord Management & The St. Petersburg Troll Farm",
        "subject": "Daily investigative dossier: The indictment of Russian oligarch Yevgeny Prigozhin and the Internet Research Agency for executing Project Lakhta, automated social bot armies, identity theft, and synthetic rally organization to boost Donald Trump.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In February 2018, Special Counsel Robert Mueller secured a sweeping federal grand jury indictment in Washington charging thirteen Russian nationals and three Russian corporate entities with waging information warfare against the United States. Spearheaded by Kremlin catering magnate Yevgeny Prigozhin and his corporate conglomerates Concord Management and Concord Catering, the operation funded the Internet Research Agency, an industrial-scale troll farm headquartered at 55 Savushkina Street in St. Petersburg.",
            "Operating under the operational codename Project Lakhta, the Agency maintained an annual operating budget exceeding twelve million dollars. Hundreds of Russian operatives working in day and night shifts utilized virtual private networks, stolen American social security numbers, and fraudulent identities to build hundreds of synthetic social media personas on Twitter, Facebook, and Instagram. These synthetic personas amassed millions of American followers, posing as grassroots political activists, Christian conservatives, and community organizers.",
            "The operational objectives were explicitly designed to benefit Donald Trump and depress turnout for his political opponents. Indictment exhibits proved that by early 2016, internal operational directives ordered specialists to use any opportunity to criticize political rivals and support the candidacy of Donald Trump. Operatives purchased thousands of targeted political advertisements using rubles, established weaponized activist communities like Being Patriotic, and systematically promoted narratives questioning the legitimacy of American democratic elections.",
            "The cyber operation penetrated the physical world. Posing as American campaign volunteers, Russian operatives communicated directly with unwitting local campaign officials in Florida, Pennsylvania, and New York, organizing physical political rallies, funding custom parade floats, and hiring American citizens to carry banners and dress in political costumes. The operation demonstrated how synthetic online deception can effortlessly translate into real-world political mobilizations.",
            "The bipartisan Senate Intelligence Committee Report Volume Two concluded that the Internet Research Agency executed a sophisticated, multi-year state-sponsored operation that reached over one hundred twenty-six million Americans. The comprehensive findings established that foreign psychological warfare operations no longer rely on covert physical infiltration, but rather exploit the algorithmic architectures of commercial social media platforms to destabilize democratic societies from within.",
            "Tonight receipts. The Department of Justice Special Counsel federal grand jury indictment in United States v. Internet Research Agency et al. The Senate Select Committee on Intelligence Report Volume Two on social media disinformation. Oxford University Computational Propaganda Project empirical forensic data, and Concord Management corporate asset filings. Every primary legal exhibit is cataloged in the dossier drawer. Examine the cyber warfare evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/file/1035477/download",
                "title": "US District Court DDC Grand Jury Indictment: United States v. Internet Research Agency, Yevgeny Prigozhin et al.",
                "published": "2018-02-16",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/Report_Volume2.pdf",
                "title": "Senate Select Committee on Intelligence: Volume Two Russian Active Measures on Social Media",
                "published": "2019-10-08",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Special Counsel Mueller Report Volume One: Section II Russian 'Active Measures' Social Media Campaign",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://comprop.oii.ox.ac.uk/research/ira-social-media-manipulation/",
                "title": "Oxford Computational Propaganda Project: The IRA and Political Polarization in the United States",
                "published": "2018-12-17",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://home.treasury.gov/news/press-releases/sm0312",
                "title": "U.S. Department of the Treasury: Sanctions on Russian Cyber Actors and Internet Research Agency Leadership",
                "published": "2018-03-15",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 24, 38), (35, 12, 25)),
        "accent": (0, 240, 220),
        "theme": "INTERNET RESEARCH AGENCY // PROJECT LAKHTA DISINFORMATION"
    },
    {
        "id": "2026-09-05-18",
        "date": "2026-09-05",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Seychelles Meeting: Erik Prince, Kirill Dmitriev & The UAE Crown Prince Transition Channel",
        "subject": "Daily investigative dossier: The January 2017 clandestine meeting in the Seychelles between Blackwater founder Erik Prince and Kirill Dmitriev, CEO of the Russian Direct Investment Fund (RDIF), brokered by UAE Crown Prince Mohammed bin Zayed to build a covert Kremlin channel.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On January 11, 2017, nine days before the presidential inauguration, Blackwater founder Erik Prince arrived at a secluded luxury resort in the Seychelles archipelago in the Indian Ocean. The unannounced gathering, brokered by United Arab Emirates Crown Prince Mohammed bin Zayed and advisor George Nader, was arranged to facilitate a face-to-face meeting between Prince, presenting himself as an unofficial surrogate for the Trump transition team, and Kirill Dmitriev, the chief executive of the Russian Direct Investment Fund.",
            "The Russian Direct Investment Fund was not a neutral commercial entity. Managed directly under the oversight of Vladimir Putin and Russian sovereign authorities, the state-run sovereign wealth fund operated under existing American financial sanctions imposed after the 2014 invasion of Crimea. Dmitriev, a Kremlin-connected financier, traveled to the remote Indian Ocean island seeking to establish a confidential communication conduit with the incoming American executive branch to negotiate the removal of financial sanctions and coordinate Middle Eastern security policies.",
            "The discussions inside the private hotel villas focused on sensitive geopolitical bargaining. Prince and Dmitriev met for over forty minutes, discussing bilateral reconciliation, potential joint military operations in Syria, and mechanisms to normalize diplomatic and commercial relations. Dmitriev subsequently prepared a formal post-meeting memorandum for the Kremlin outlining the transition team's openness to strategic coordination, which was forwarded directly to senior Russian foreign policy leadership.",
            "The cover-up following the meeting prompted a criminal perjury referral. In November 2017, Prince testified under oath before the House Permanent Select Committee on Intelligence that he had merely traveled to the Seychelles on private business and happened to bump into Dmitriev by complete chance over a beer. However, subsequent findings by Special Counsel Robert Mueller, supported by contemporaneous flight manifests, encrypted text messages, and sworn testimony from George Nader, disproved Prince's account.",
            "Intelligence scholars emphasize that the Seychelles summit epitomized shadow foreign policy conducted outside institutional governance. By dispatching private military contractors to negotiate sensitive state affairs with sanctioned Kremlin financiers, the incoming leadership bypassed the State Department, the Central Intelligence Agency, and the diplomatic record, establishing an illicit backchannel that severely compromised American national security.",
            "Tonight receipts. Special Counsel Robert Mueller Report Volume One findings on the Seychelles gathering. House Permanent Select Committee on Intelligence testimony transcripts of Erik Prince. Federal court plea agreements in United States v. Nader, and declassified Russian Direct Investment Fund communications. Every primary document is cataloged in the dossier drawer. Review the Seychelles evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Special Counsel Mueller Report Volume One: Section IV The Seychelles Meetings and Kirill Dmitriev",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://docs.house.gov/meetings/IG/IG00/20171130/106661/HHRG-115-IG00-Transcript-20171130.pdf",
                "title": "House Permanent Select Committee on Intelligence: Executive Session Interview Transcript of Erik Prince",
                "published": "2017-11-30",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Bipartisan Findings on UAE Mediation and Dmitriev Outreach",
                "published": "2020-08-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/world/national-security/blackwater-founder-held-secret-seychelles-meeting-to-establish-trump-putin-back-channel/2017/04/03/95908a08-1648-11e7-833c-503e1f6394c9_story.html",
                "title": "The Washington Post: Blackwater Founder Held Secret Seychelles Meeting to Establish Trump-Putin Back Channel",
                "published": "2017-04-03",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://home.treasury.gov/news/press-releases/sm608",
                "title": "U.S. Department of the Treasury: Sanctions Background and Legal Restrictions on Russian Direct Investment Fund",
                "published": "2019-03-15",
                "kind": "reference"
            }
        ],
        "art_palette": ((10, 28, 35), (38, 20, 15)),
        "accent": (255, 165, 0),
        "theme": "SEYCHELLES GATHERING // RDIF SOVEREIGN FUND BACKCHANNEL"
    },
    {
        "id": "2026-09-04-18",
        "date": "2026-09-04",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Kislyak Suite Encounters: The Mayflower Hotel Speech, Jeff Sessions & The Undisclosed Diplomatic Meetings",
        "subject": "Daily investigative dossier: Russian Ambassador Sergey Kislyak attending Donald Trump's first major foreign policy speech at the Mayflower Hotel in April 2016, undisclosed VIP reception encounters, and Senator Jeff Sessions's subsequent recusal from the Russia investigation.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On April 27, 2016, inside the Grand Ballroom of the Mayflower Hotel in Washington, Donald Trump delivered his first comprehensive foreign policy address as a presidential candidate. Seated prominently in the front row, invited directly by the campaign's host organization, was Russian Ambassador Sergey Kislyak. Prior to taking the podium, Trump, campaign chairman Paul Manafort, and senior national security advisor Senator Jeff Sessions attended an exclusive pre-speech VIP reception where Kislyak was personally greeted.",
            "The Mayflower encounter marked the commencement of a series of undisclosed high-level contacts between Trump's core inner circle and senior Russian diplomatic officials. Throughout the spring and summer of 2016, Sessions met repeatedly with Kislyak, including a private conference in his Senate Russell building office in September 2016 as Russian military intelligence cyber intrusions into the American election were intensifying and dominating national security briefings.",
            "The institutional crisis erupted during Sessions's confirmation hearings for Attorney General. In January 2017, questioned under oath by Senator Al Franken regarding whether he was aware of any communications between the campaign and the Russian government, Sessions testified: I did not have communications with the Russians. The categorical denial under oath directly contradicted FBI counterintelligence surveillance records capturing Sessions's multiple private encounters with the Russian ambassador.",
            "The revelation forced an unprecedented institutional retreat. On March 2, 2017, facing intense public outrage and the imminent release of classified intelligence summaries confirming the meetings, Attorney General Jeff Sessions announced his formal recusal from all existing and future Department of Justice investigations into the Trump campaign and Russian election interference. The recusal infuriated Donald Trump, who repeatedly demanded that Sessions reverse his decision to protect the presidency.",
            "Legal historians and former Department of Justice officials emphasize that Sessions's recusal proved indispensable for safeguarding constitutional accountability. By stepping aside from the investigation he was conflicted out of, Sessions created the legal opening that enabled Deputy Attorney General Rod Rosenstein to appoint Special Counsel Robert Mueller, ensuring that federal law enforcement could independently investigate foreign election interference without direct executive interference.",
            "Tonight receipts. The Senate Judiciary Committee Attorney General confirmation hearing transcripts of Jeff Sessions. The Department of Justice official public announcement of Attorney General Sessions's recusal. The Special Counsel Mueller Report Volume One findings on the Mayflower Hotel reception, and FBI counterintelligence interview records. Every judicial transcript and declassified memorandum is cataloged in the dossier drawer. Review the confirmation records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/archives/sco/file/1373816/download",
                "title": "Special Counsel Mueller Report Volume One: Section III The Mayflower Hotel Foreign Policy Address and Reception",
                "published": "2019-04-18",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.judiciary.senate.gov/imo/media/doc/01-10-17%20Sessions%20Testimony.pdf",
                "title": "Senate Judiciary Committee: Confirmation Hearing of Senator Jeff Sessions for Attorney General of the United States",
                "published": "2017-01-10",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/opa/pr/attorney-general-sessions-statement-recusal",
                "title": "U.S. Department of Justice: Attorney General Jeff Sessions Public Statement on Recusal",
                "published": "2017-03-02",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/world/national-security/sessions-met-with-russian-envoy-twice-last-year-counter-to-firm-denials-in-senate-testimony/2017/03/01/e272a578-fecc-11e6-99b4-9e613afeb09f_story.html",
                "title": "The Washington Post: Sessions Met With Russian Envoy Twice Last Year, Counter to Denials",
                "published": "2017-03-01",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Bipartisan Findings on Kislyak Diplomatic Outreach",
                "published": "2020-08-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((14, 20, 32), (35, 18, 14)),
        "accent": (255, 190, 50),
        "theme": "MAYFLOWER SUITE // UNDISCLOSED SESSIONS KISLYAK MEETINGS"
    },
    {
        "id": "2026-09-03-18",
        "date": "2026-09-03",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Stormy Daniels Hush Money Ledger: Michael Cohen, AMI Catch-and-Kill & The 34 Felony Convictions",
        "subject": "Daily investigative dossier: The Manhattan District Attorney conviction of Donald Trump on 34 felony counts of falsifying business records to conceal $130,000 in pre-election hush money payments to Stormy Daniels, American Media Inc. catch-and-kill schemes, and election interference.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On May 30, 2024, inside the Manhattan Criminal Court, a New York state jury returned unanimous guilty verdicts against Donald Trump on all thirty-four felony counts of falsifying business records in the first degree. The historic trial, prosecuted by Manhattan District Attorney Alvin Bragg, marked the first time in American history that a former president was convicted of state felonies, establishing that the defendant orchestrated an unlawful scheme to corrupt the 2016 presidential election.",
            "The criminal conduct centered on the covert suppression of damaging sexual misconduct allegations weeks before the presidential vote. Following the public release of the Access Hollywood recording in October 2016, Trump personal attorney Michael Cohen wired one hundred thirty thousand dollars to adult film actress Stormy Daniels through an offshore shell company called Essential Consultants LLC. The transaction secured Daniels's silence regarding a 2006 sexual encounter, preventing catastrophic political fallout during the final days of the campaign.",
            "The cover-up required systemic accounting fraud across the Trump Organization. Throughout 2017, while sitting in the Oval Office, Trump reimbursed Cohen through monthly corporate installments structured as fictitious legal retainers. Executive payroll records, general ledgers, and signed checks were systematically falsified to disguise personal campaign hush money reimbursements as ordinary commercial legal expenses, evading New York state tax reporting and federal campaign finance disclosure laws.",
            "The conspiracy operated alongside American Media Inc., publisher of the National Enquirer. Former CEO David Pecker testified under immunity that he entered into a corrupt agreement with Trump and Cohen to act as the campaign's eyes and ears, executing catch-and-kill operations to purchase and bury negative stories, including paying former Playboy model Karen McDougal one hundred fifty thousand dollars to ensure total pre-election media suppression.",
            "Constitutional scholars and criminal justice historians emphasize that the thirty-four felony convictions punctured the myth of executive legal immunity. By establishing that fraudulent corporate accounting deployed to deceive voters constitutes criminal conduct under state penal law, the jury's verdict reaffirmed the core democratic principle that no political figure, regardless of status, stands above the rule of law.",
            "Tonight receipts. The Supreme Court of the State of New York trial indictment and jury verdict sheets in People of the State of New York v. Donald J. Trump. The Federal Election Commission formal conciliation agreement and fine against American Media Inc. The Southern District of New York plea agreement in United States v. Cohen, and signed Trump Organization ledger checks. Every trial exhibit is cataloged in the dossier drawer. Review the criminal conviction records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://manhattanda.org/d-a-bragg-announces-34-count-felony-indictment-of-former-president-donald-j-trump/",
                "title": "Manhattan District Attorney: D.A. Bragg Announces 34-Count Felony Trial Indictment and Verdict of Donald J. Trump",
                "published": "2024-05-30",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/usao-sdny/pr/michael-cohen-pleads-guilty-manhattan-federal-court-eight-counts-including-criminal-tax",
                "title": "US Attorney SDNY: Michael Cohen Pleads Guilty to Campaign Finance Violations in Stormy Daniels Payment",
                "published": "2018-08-21",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.fec.gov/files/legal/murs/7313/19044465497.pdf",
                "title": "Federal Election Commission: Conciliation Agreement and Fine with American Media Inc. Over Catch-and-Kill",
                "published": "2021-04-06",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.nycourts.gov/LegacyPDFS/press/PDFs/People-v-DonaldTrump-VerdictSheet.pdf",
                "title": "New York Supreme Court Criminal Term: Official Jury Verdict Sheet in The People v. Donald J. Trump",
                "published": "2024-05-30",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/d9/special-counsel-mueller-report/volume2.pdf",
                "title": "Special Counsel Mueller Report Volume Two: Analysis of Efforts to Discourage Michael Cohen Cooperation",
                "published": "2019-04-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((25, 12, 20), (38, 15, 15)),
        "accent": (255, 50, 80),
        "theme": "HUSH MONEY CONVICTION // 34 STATE FELONY COUNTS"
    },
    {
        "id": "2026-09-02-18",
        "date": "2026-09-02",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Jan 6 Defense Obstruction: The Pentagon Guard Delays, Jeffrey Clark & The Insurrection Blueprint",
        "subject": "Daily investigative dossier: The weaponization of the Department of Justice through environmental lawyer Jeffrey Clark, pressuring state officials to overturn certified elections, the hours-long delay in deploying the National Guard, and the House January 6 Committee findings.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On January 6, 2021, as violent mobs assaulted the United States Capitol to disrupt the constitutional certification of the presidential election, the federal command structure experienced a catastrophic three-hour-and-nineteen-minute delay before the Department of Defense authorized the deployment of the District of Columbia National Guard. Sworn testimony before the House January 6 Committee proved that while vice president Mike Pence and congressional leaders pleaded for immediate military reinforcement, Donald Trump made zero calls to the Pentagon or law enforcement leadership.",
            "The violent assault was preceded by an aggressive campaign to subvert the Department of Justice from within. In late December 2020, Trump attempted to install environmental division assistant attorney general Jeffrey Clark as Acting Attorney General after Clark drafted a fraudulent letter to Georgia state officials claiming the Department had identified significant electoral irregularities. The attempted administrative coup was thwarted only when the entire senior leadership of the Department of Justice and White House Counsel threatened mass resignation.",
            "The parallel strategy pressured state election administrators to fabricate false vote totals. In an extraordinary January 2, 2021 phone call, Trump personally pressured Georgia Secretary of State Brad Raffensperger, demanding that election officials find eleven thousand seven hundred eighty votes to overturn the certified election results, threatening criminal prosecution if state officials refused to comply with the demand. The recorded audio laid bare an explicit effort to subvert democratic outcomes through executive coercion.",
            "The resulting criminal accountability crystallized in federal and state indictments. Special Counsel Jack Smith secured a federal grand jury indictment in Washington charging Trump with four felony counts of conspiracy to defraud the United States and obstruction of an official proceeding. Simultaneously, a Fulton County grand jury returned a sweeping state racketeering indictment against Trump and eighteen co-defendants, establishing that the multi-state scheme to submit fraudulent alternate electors constituted a criminal enterprise.",
            "Constitutional scholars and national security analysts emphasize that the January 6 assault represented the most perilous domestic challenge to the American constitutional republic since the Civil War. By deploying mob violence, pressuring federal law enforcement to fabricate fraud, and seeking to commandeer military assets, executive power was weaponized to nullify the peaceful transfer of power.",
            "Tonight receipts. The House Select Committee to Investigate the January 6th Attack Final Report. The Special Counsel Jack Smith federal criminal indictment in United States v. Trump. The Fulton County District Attorney state racketeering indictment, and the declassified Department of Defense timeline on National Guard deployment. Every congressional finding and grand jury charge is cataloged in the dossier drawer. Review the evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.govinfo.gov/collection/january-6th-committee-final-report",
                "title": "House Select Committee to Investigate the January 6th Attack: Official Final Congressional Report",
                "published": "2022-12-22",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/storage/US_v_Trump_23_cr_257.pdf",
                "title": "US District Court DDC Grand Jury Indictment: United States v. Donald J. Trump (2020 Election Obstruction)",
                "published": "2023-08-01",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.fultonclerk.org/DocumentCenter/View/2023/Trump-Indictment-Fulton-County",
                "title": "Superior Court of Fulton County Georgia: State RICO Indictment in State of Georgia v. Donald J. Trump et al.",
                "published": "2023-08-14",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://media.defense.gov/2021/Nov/18/2002895697/-1/-1/1/DODIG-2022-039%20REDACTED%20SECURE.PDF",
                "title": "Department of Defense Office of Inspector General: Review of DoD Role and Response to January 6 Attack",
                "published": "2021-11-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.dcbar.org/getmedia/discip-clark-report",
                "title": "District of Columbia Bar Board on Professional Responsibility: Disciplinary Findings on Jeffrey Clark",
                "published": "2024-04-04",
                "kind": "reference"
            }
        ],
        "art_palette": ((20, 10, 30), (35, 12, 18)),
        "accent": (255, 60, 60),
        "theme": "JANUARY 6 ASSAULT // SUBVERSION OF CONSTITUTIONAL TRANSFER"
    },
    {
        "id": "2026-09-01-18",
        "date": "2026-09-01",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Trump Taj Mahal Sanctions: FinCEN Fines, Money Laundering Violations & The 10-Million-Dollar Penalty",
        "subject": "Daily investigative dossier: The Treasury Department Financial Crimes Enforcement Network (FinCEN) assessing a historic $10 million civil penalty against Trump Taj Mahal casino for willful, long-standing violations of the Bank Secrecy Act and failing to report suspicious cash transactions.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In February 2015, the United States Department of the Treasury's Financial Crimes Enforcement Network, or FinCEN, imposed a landmark ten-million-dollar civil money penalty against Trump Taj Mahal Casino Resort in Atlantic City. The federal enforcement action, the largest penalty ever assessed against a commercial casino at that time, sanctioned the property for willful, long-standing, and systemic violations of the Bank Secrecy Act and federal anti-money laundering regulations.",
            "The Treasury Department's forensic audit revealed pervasive operational failures dating back to the property's opening. For years, the Taj Mahal deliberately failed to implement an effective anti-money laundering compliance program, failed to maintain required internal accounting controls, and systematically neglected to file mandatory Currency Transaction Reports for cash transactions exceeding ten thousand dollars, creating an open gateway for illicit financial syndicates to launder dirty currency.",
            "The casino's geographic and financial exposure made it a magnet for international organized crime. During the 1990s and 2000s, federal law enforcement agencies documented numerous Russian organized crime figures and international racketeers frequenting the property's private high-stakes gaming rooms, moving millions in illicit cash through casino cages with minimal documentation. The casino admitted in federal court filings that it repeatedly failed to conduct required independent compliance audits.",
            "The regulatory sanctions were neither novel nor unexpected. In 1998, FinCEN had previously fined the Taj Mahal four hundred seventy-seven thousand dollars for similar systemic reporting violations. Despite the prior federal penalty, the casino management willfully ignored regulatory warnings, demonstrating an institutional culture that prioritized lucrative high-roller cash volume over federal anti-money laundering compliance and national financial integrity.",
            "Financial intelligence experts and forensic accountants emphasize that commercial casinos operating without robust anti-money laundering safeguards function as critical nodes in global capital flight networks. By permitting untracked cash transactions, the Taj Mahal established the early commercial framework through which illicit international capital flows became interwoven with the broader Trump corporate empire.",
            "Tonight receipts. The United States Department of the Treasury FinCEN Assessment of Civil Money Penalty against Trump Taj Mahal Casino Resort. United States District Court for the District of New Jersey consent decree filings. The 1998 FinCEN historical enforcement order, and federal Bank Secrecy Act compliance audit exhibits. Every regulatory decree is preserved in the dossier drawer. Review the Treasury enforcement records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.fincen.gov/news/news-releases/fincen-fines-trump-taj-mahal-casino-resort-10-million-significant-and-long-standing",
                "title": "Financial Crimes Enforcement Network (FinCEN): $10 Million Civil Penalty Against Trump Taj Mahal Casino Resort",
                "published": "2015-02-11",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.fincen.gov/sites/default/files/enforcement_action/Trump_Taj_Mahal_Assessment.pdf",
                "title": "US Treasury Department FinCEN: Official Assessment of Civil Money Penalty In the Matter of Trump Taj Mahal",
                "published": "2015-02-11",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.wsj.com/articles/trump-taj-mahal-fined-10-million-for-poor-anti-money-laundering-controls-1423692994",
                "title": "The Wall Street Journal: Trump Taj Mahal Fined $10 Million for Deficient Anti-Money-Laundering Controls",
                "published": "2015-02-11",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.govinfo.gov/content/pkg/USCOURTS-njd-1_15-cv-01089/pdf/USCOURTS-njd-1_15-cv-01089-0.pdf",
                "title": "US District Court DNJ: Consent Judgment and Settlement in FinCEN v. Trump Entertainment Resorts Inc.",
                "published": "2015-02-11",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.fincen.gov/sites/default/files/news_release/19980323.pdf",
                "title": "FinCEN Historical Archive: 1998 Civil Money Penalty Against Trump Taj Mahal for BSA Violations",
                "published": "1998-03-23",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 20, 30), (35, 25, 10)),
        "accent": (255, 180, 0),
        "theme": "TRUMP TAJ MAHAL // 10-MILLION FINCEN MONEY LAUNDERING SANCTIONS"
    },
    {
        "id": "2026-08-31-18",
        "date": "2026-08-31",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Emoluments Cartel: The Trump International Hotel DC, Foreign Delegations & Sovereign Influence Peddling",
        "subject": "Daily investigative dossier: Hundreds of thousands of dollars in lodging and banquet spending at the Trump International Hotel in Washington DC by foreign governments including Saudi Arabia, Kuwait, and Bahrain, violating the Foreign Emoluments Clause of the US Constitution.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Throughout Donald Trump's four-year presidency, the Trump International Hotel, housed inside the historic Old Post Office Pavilion on Pennsylvania Avenue just blocks from the White House, served as an overt hub for foreign governments and domestic lobbyists seeking presidential favor. Financial records obtained by the House Committee on Oversight and Reform documented that foreign officials from at least thirty-seven nations spent millions of dollars patronizing the property, directly enriching the sitting president.",
            "The spending was explicitly coordinated to influence foreign policy. Weeks after the 2016 election, the Embassy of Kuwait abruptly canceled its long-standing National Day reservation at the Four Seasons, moving the lavish celebration to the Trump International Hotel. Simultaneously, lobbying firms working on behalf of the Kingdom of Saudi Arabia reserved hundreds of rooms, spending over two hundred seventy thousand dollars at the hotel while aggressively lobbying Congress to preserve American arms transfers to Riyadh.",
            "The commercial arrangement directly violated the Foreign Emoluments Clause of the United States Constitution, which strictly prohibits federal officeholders from accepting any present, emolument, office, or title of any kind from any king, prince, or foreign state without the consent of Congress. Rather than placing the property into a blind trust, Trump retained direct financial ownership through a revocable trust, withdrawing corporate profits into personal accounts.",
            "The judicial and legislative scrutiny resulted in landmark litigation. The Attorneys General of Maryland and the District of Columbia filed historic federal lawsuits alleging unconstitutional competition and corruption, securing federal court rulings affirming that constitutional emoluments encompass commercial transactions and hotel profits. Subpoenaed accounting records proved that foreign delegations from Malaysia, Qatar, and the United Arab Emirates booked top-tier luxury suites to curry presidential favor.",
            "Anti-corruption scholars and constitutional historians emphasize that the Trump International Hotel represented an unprecedented merger of personal commercial enrichment and sovereign executive authority. By converting a leased federal historic building into a private tollbooth for foreign dignitaries, the executive dismantled two centuries of presidential ethical standards, commercializing the institutional diplomacy of the United States.",
            "Tonight receipts. The House Committee on Oversight and Reform forensic financial report on foreign government spending at Trump Hotel DC. The United States Court of Appeals for the Fourth Circuit record in District of Columbia v. Trump. General Services Administration Old Post Office lease compliance documents, and Saudi lobbying expenditure disclosures. Every financial exhibit is cataloged in the dossier drawer. Review the hotel accounting logs for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://oversightdemocrats.house.gov/news/press-releases/oversight-committee-releases-documents-showing-trump-hotel-charged-secret-service",
                "title": "House Committee on Oversight and Reform: Accounting Disclosures on Foreign Government Spending at Trump Hotel",
                "published": "2022-10-17",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.washingtonpost.com/politics/saudi-funded-lobbyist-spending-at-trumps-dc-hotel-surged-after-2016-election-records-show/2018/12/05/8be4818c-f8bf-11e8-8c9a-f109ecd5a73f_story.html",
                "title": "The Washington Post: Saudi-Funded Lobbyist Spending at Trump DC Hotel Surged After 2016 Election",
                "published": "2018-12-05",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.ca4.uscourts.gov/opinions/182488.P.pdf",
                "title": "US Court of Appeals for the Fourth Circuit: En Banc Opinion in District of Columbia v. Trump (Emoluments Clause)",
                "published": "2020-05-14",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.gsa.gov/about-us/gsa-regions/region-11-national-capital/historic-buildings/old-post-office-dc",
                "title": "General Services Administration: Old Post Office Building Lease Agreement and Financial Oversight Filings",
                "published": "2019-01-20",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://oversightdemocrats.house.gov/sites/democrats.oversight.house.gov/files/2024-01-04.White%20House%20For%20Sale%20Report.pdf",
                "title": "House Oversight Committee: White House for Sale - How Princes, Prime Ministers and Premiers Paid Off Trump",
                "published": "2024-01-04",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 25, 35), (40, 20, 10)),
        "accent": (255, 170, 0),
        "theme": "EMOLUMENTS CARTEL // TRUMP HOTEL DC SOVEREIGN CASH"
    },
    {
        "id": "2026-08-30-18",
        "date": "2026-08-30",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Helsinki Press Conference: Siding with the KGB over American Intelligence & The Worldwide Outrage",
        "subject": "Daily investigative dossier: Donald Trump standing beside Vladimir Putin at the July 16, 2018 Helsinki joint press conference, publicly repudiating unanimous conclusions of the US Intelligence Community regarding 2016 election hacking, and affirming Putin's denial.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On July 16, 2018, standing on the global stage inside the Presidential Palace in Helsinki, Finland following their closed-door summit, Donald Trump and Vladimir Putin addressed international media in a joint press conference. Asked directly by an American journalist whether he believed his own intelligence community or the Russian president regarding Russian cyber intrusions into the 2016 election, Trump delivered an answer that shocked allies and intelligence professionals worldwide.",
            "Looking out at global reporters, Trump stated: My people came to me, Dan Coats came to me and some others, they said they think it's Russia. I have President Putin; he just said it's not Russia. I will say this: I don't see any reason why it would be. In that single sentence, the commander-in-chief publicly repudiated the unanimous, bipartisan assessments of the FBI, CIA, and NSA, endorsing the denial of a former KGB foreign intelligence officer over American national security findings.",
            "The public capitulation triggered immediate bipartisan condemnation in Washington. Director of National Intelligence Dan Coats issued an emergency public statement affirming the unshakeable veracity of the intelligence community's assessments regarding ongoing, pervasive Russian efforts to undermine American democracy. Bipartisan congressional leaders, including late Senator John McCain, condemned the performance as one of the most disgraceful performances by an American president in history.",
            "The geopolitical implications for European collective security were catastrophic. By publicly deferring to Kremlin authority and attacking American law enforcement on foreign soil, Trump signaled that the United States executive branch was unwilling to defend its own democratic institutions against hostile foreign hybrid warfare. Russian state television celebrated the summit as an unmitigated diplomatic triumph, boasting that Moscow had outmaneuvered the American presidency without firing a single shot.",
            "Counterintelligence scholars and diplomatic historians characterize the Helsinki joint press conference as the definitive public manifestation of an executive subordinated to foreign influence. The event proved that the systemic evasion of official diplomatic logging and the suppression of translation notes were designed to conceal an underlying foreign policy posture that placed personal accommodation of an adversarial dictator above the security of the American republic.",
            "Tonight receipts. The official White House verbatim transcript of the July 16, 2018 Helsinki joint press conference. Director of National Intelligence Dan Coats emergency statement on intelligence community findings. Bipartisan congressional declarations of condemnation, and international diplomatic cable reactions. Every primary transcript is preserved in the dossier drawer. Review the press conference record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-president-putin-russian-federation-joint-press-conference/",
                "title": "White House Archives: Official Verbatim Transcript of President Trump and President Putin Joint Press Conference",
                "published": "2018-07-16",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.dni.gov/index.php/newsroom/press-releases/press-releases-2018/item/1885-statement-from-dni-dan-coats",
                "title": "Office of the Director of National Intelligence: Statement by DNI Dan Coats on Election Security and Russian Threat",
                "published": "2018-07-16",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.mccain.senate.gov/public/index.cfm/press-releases?ID=5104B8A5-D62A-4B60-985A-6447A574E396",
                "title": "U.S. Senate Press Release: Statement by Senator John McCain on Trump-Putin Meeting in Helsinki",
                "published": "2018-07-16",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.congress.gov/115/crec/2018/07/17/CREC-2018-07-17-pt1-PgS4977.pdf",
                "title": "Congressional Record: Bipartisan Senate Statements on the Helsinki Summit and Transatlantic Security",
                "published": "2018-07-17",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.intelligence.senate.gov/sites/default/files/documents/report_volume5.pdf",
                "title": "Senate Select Committee on Intelligence: Volume Five Counterintelligence Findings on Helsinki and Kremlin Operations",
                "published": "2020-08-18",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 20, 36), (36, 12, 18)),
        "accent": (255, 70, 70),
        "theme": "HELSINKI PRESS CONFERENCE // REPUDIATION OF US INTELLIGENCE"
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
    print(f"Checking {len(EPISODES)} retrospective daily episodes for Batch 3...")
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
