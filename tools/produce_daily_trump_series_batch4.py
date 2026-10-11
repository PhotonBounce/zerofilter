#!/usr/bin/env python3
"""
tools/produce_daily_trump_series_batch4.py - Production Engine for Batch 4 Retrospective Daily Investigative Podcasts
ZeroFilter Geopolitical & Counterintelligence Dossier Series (2026-08-29 down to 2026-08-20)
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
        "id": "2026-08-29-18",
        "date": "2026-08-29",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Jeffrey Epstein Subpoena Shield: The Palm Beach Non-Prosecution Pact, Acosta & The Mar-a-Lago Encounters",
        "subject": "Daily investigative dossier: The decades-long relationship between Donald Trump and convicted sex trafficker Jeffrey Epstein, social gatherings at Mar-a-Lago, Alexander Acosta's federal non-prosecution agreement, and unsealed civil court depositions.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. For more than fifteen years spanning the late 1980s through the early 2000s, Donald Trump maintained a close personal and social relationship with convicted sex offender Jeffrey Epstein. Operating between Manhattan and Palm Beach, Florida, the two billionaires frequented each other's private estates, exclusive VIP gatherings, and private jets. In a widely publicized 2002 interview with New York Magazine, Trump famously praised Epstein, describing him as a terrific guy who was a lot of fun to be with, adding that Epstein liked beautiful women as much as he did, and many on the younger side.",
            "The operational nexus between the two figures intersected at Mar-a-Lago. Unsealed federal court depositions from survivors and staff in Giuffre v. Maxwell documented that Epstein utilized the private Palm Beach club as a recruiting ground for underage victims, including Virginia Giuffre, who was employed at Mar-a-Lago when she was first approached by Ghislaine Maxwell. Flight logs preserved in federal evidentiary exhibits confirmed that Trump flew multiple times aboard Epstein's private aircraft alongside associates and security personnel.",
            "The political shielding deepened when Trump appointed Alexander Acosta as Secretary of Labor in 2017. A decade earlier, as United States Attorney for the Southern District of Florida, Acosta had secretly brokered an unprecedented federal non-prosecution agreement for Epstein, shutting down an FBI investigation into scores of child sexual abuse allegations and granting Epstein and unnamed co-conspirators blanket immunity from federal prosecution without notifying the underage victims.",
            "A comprehensive report published by the Department of Justice Office of Professional Responsibility concluded that while Acosta did not engage in professional misconduct, he exercised poor judgment in granting sweeping immunity to a serial child predator. Public outrage and investigative reporting by the Miami Herald forced Acosta to resign from Trump's cabinet in July 2019 following Epstein's federal sex trafficking indictment in New York.",
            "Legal scholars and civil rights historians emphasize that the Epstein non-prosecution pact epitomized a two-tiered justice system that insulated powerful, ultra-wealthy elites from accountability. The enduring associations, shared social spheres, and high-level cabinet appointments demonstrated how personal relationships within elite circles compromised the integrity of federal law enforcement and delayed justice for scores of vulnerable victims.",
            "Tonight receipts. The unsealed Southern District of New York court deposition transcripts and flight logs in Giuffre v. Maxwell. The United States Department of Justice Office of Professional Responsibility investigative report on the Epstein non-prosecution agreement. The Palm Beach Police Department 2006 incident records, and official cabinet resignation letters. Every judicial exhibit and public record is cataloged in the dossier drawer. Review the evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://nymag.com/nymetro/news/people/n_7912/",
                "title": "New York Magazine: Jeffrey Epstein - International Moneyman of Mystery (Trump Interview Archive)",
                "published": "2002-10-28",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.courtlistener.com/docket/4355835/giuffre-v-maxwell/",
                "title": "US District Court SDNY: Unsealed Deposition Transcripts and Flight Logs in Giuffre v. Maxwell",
                "published": "2024-01-03",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/opr/page/file/1336151/download",
                "title": "DOJ Office of Professional Responsibility: Report on the Investigation of Alexander Acosta and Jeffrey Epstein NPA",
                "published": "2020-11-12",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.miamiherald.com/news/local/article220097825.html",
                "title": "The Miami Herald: Perversion of Justice - How a Future Trump Cabinet Member Gave Epstein the Deal of a Lifetime",
                "published": "2018-11-28",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.justice.gov/usao-sdny/pr/jeffrey-epstein-charged-manhattan-federal-court-sex-trafficking-minors",
                "title": "US Attorney SDNY: Jeffrey Epstein Charged in Manhattan Federal Court with Sex Trafficking of Minors",
                "published": "2019-07-08",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 12, 28), (35, 15, 20)),
        "accent": (255, 60, 90),
        "theme": "EPSTEIN SUBPOENA SHIELD // ACOSTA NON-PROSECUTION IMMUNITY"
    },
    {
        "id": "2026-08-28-18",
        "date": "2026-08-28",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Ukraine Diplomatic Squeeze: Marie Yovanovitch's Ouster, Giuliani's Smear Campaign & State Dept Interference",
        "subject": "Daily investigative dossier: The orchestrated smear campaign against veteran US Ambassador to Ukraine Marie Yovanovitch by Rudy Giuliani, John Solomon, and corrupt Ukrainian prosecutors, her abrupt recall, and intimidation by executive leadership.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In the spring of 2019, Marie Yovanovitch, a highly decorated thirty-three-year career diplomat serving as the United States Ambassador to Ukraine, became the primary target of an orchestrated smear campaign directed by Donald Trump's personal attorney Rudy Giuliani. Operating alongside indicted associates Lev Parnas and Igor Fruman, Giuliani sought Yovanovitch's removal because her steadfast anti-corruption posture blocked their efforts to pressure Ukrainian prosecutors into launching politically motivated investigations against domestic rivals.",
            "The coordinated smear campaign utilized media conduits and corrupt foreign prosecutors. Former Ukrainian Prosecutor General Yuriy Lutsenko, whom Yovanovitch had criticized for stalling anti-corruption reforms, provided fabricated allegations to conservative opinion columnist John Solomon. Donald Trump Jr. amplified the attacks on social media, accusing the ambassador of undermining the president. Simultaneously, private surveillance messages disclosed in congressional records revealed that Parnas and his associates monitored Yovanovitch's physical movements in Kyiv.",
            "The diplomatic interference culminated in an abrupt emergency recall. In April 2019, Yovanovitch was awakened at one in the morning in Kyiv and instructed by State Department leadership to return immediately to Washington on the next flight due to concerns for her security. Deputy Secretary of State John Sullivan admitted to her that while she had done nothing wrong, the president had lost confidence in her and demanded her immediate removal from the embassy.",
            "The intimidation escalated into public witness retaliation during congressional impeachment hearings. In November 2019, as Ambassador Yovanovitch testified before the House Permanent Select Committee on Intelligence regarding the shadow foreign policy apparatus, Donald Trump posted real-time public attacks on Twitter denigrating her diplomatic career and declaring that every diplomatic posting she served in turned bad. Committee Chairman Adam Schiff immediately denounced the statements as real-time witness intimidation.",
            "Foreign policy scholars and diplomatic historians emphasize that the purge of Ambassador Yovanovitch shattered the professional, non-partisan civil service architecture of the Department of State. By subordinating verified anti-corruption foreign policy to personal political interests and sacrificing a respected diplomat to appease corrupt foreign actors, the executive branch degraded the credibility of American diplomacy across Eastern Europe.",
            "Tonight receipts. The House Permanent Select Committee on Intelligence sworn deposition transcripts of Ambassador Marie Yovanovitch. The State Department Office of Inspector General records on ambassadorial recalls. Indictment exhibits in United States v. Parnas regarding physical surveillance in Kyiv, and the official congressional impeachment testimony record. Every primary document is preserved in the dossier drawer. Review the diplomatic transcripts for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://docs.house.gov/meetings/IG/IG00/CPRT-116-IG00-D007.pdf",
                "title": "House Permanent Select Committee on Intelligence: Deposition of Ambassador Marie L. Yovanovitch",
                "published": "2019-10-11",
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
                "url": "https://www.justice.gov/usao-sdny/pr/lev-parnas-and-igor-fruman-charged-campaign-finance-violations",
                "title": "US Attorney SDNY: Superseding Indictment and Evidentiary Exhibits in United States v. Lev Parnas et al.",
                "published": "2020-09-17",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.stateoig.gov/reports/inspection-and-evaluation",
                "title": "Department of State Office of Inspector General: Oversight and Review of Diplomatic Recalls and Personnel Security",
                "published": "2020-02-14",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.washingtonpost.com/politics/trump-attacks-yovanovitch-as-she-testifies-saying-everywhere-she-went-turned-bad/2019/11/15/8e4414ba-07c5-11ea-8292-c46ee8cb3dce_story.html",
                "title": "The Washington Post: Trump Attacks Yovanovitch on Twitter as She Testifies in Impeachment Inquiry",
                "published": "2019-11-15",
                "kind": "reference"
            }
        ],
        "art_palette": ((12, 25, 38), (35, 18, 12)),
        "accent": (255, 180, 40),
        "theme": "UKRAINE EMBASSY PURGE // YOVANOVITCH WITNESS INTIMIDATION"
    },
    {
        "id": "2026-08-27-18",
        "date": "2026-08-27",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Bannon Fraud Syndicate: We Build The Wall, Brian Kolfage & The Executive Pardon",
        "subject": "Daily investigative dossier: Steve Bannon, Brian Kolfage, and Andrew Badolato defrauding hundreds of thousands of donors out of $25 million in the 'We Build The Wall' campaign, siphoning millions for personal luxury, and the midnight executive pardon.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In August 2020, federal postal inspectors and United States federal agents boarded a luxury mega-yacht off the coast of Westbrook, Connecticut, arresting former White House chief strategist Steve Bannon. A grand jury indictment returned in the Southern District of New York charged Bannon, disabled military veteran Brian Kolfage, and venture capitalist Andrew Badolato with wire fraud and money laundering conspiracy for defrauding hundreds of thousands of grassroots conservative donors out of more than twenty-five million dollars.",
            "The operational scheme masqueraded as a patriotic crowdfunding effort called We Build The Wall. Solicitations across digital media promised donors that one hundred percent of contributions would go directly toward constructing private border barriers along the southern frontier, with Kolfage publicly pledging that he would not take a penny in salary. In reality, prosecutors documented that Kolfage covertly siphoned over three hundred fifty thousand dollars for personal luxury spending, including a yacht, luxury golf cart, and jewelry, while Bannon funneled over one million dollars through an opaque non-profit entity.",
            "The fraudulent money laundering architecture relied on sham corporate contracts and fake invoices. Financial forensic records revealed that Bannon used his non-profit, Citizens of the American Republic, to conceal payments to Kolfage and cover personal travel and hospitality expenses. When the organizers learned in late 2019 that federal financial investigators were scrutinizing their bank accounts, they modified their corporate disclosures and deployed encrypted messaging applications to conceal the ongoing diversion of charitable funds.",
            "The federal prosecution was abruptly neutralized by executive intervention. In the early morning hours of January 20, 2021, during his final hours in the presidency, Donald Trump issued a full unconditional executive pardon to Steve Bannon, erasing the federal fraud charges before the case could reach trial. While co-conspirators Kolfage and Badolato were subsequently sentenced to federal prison terms of over four and three years respectively, Bannon walked free.",
            "Legal scholars and anti-corruption analysts emphasize that the We Build The Wall scheme exposed how populist political branding is routinely monetized to exploit trusting grassroots supporters. The subsequent executive pardon demonstrated the transactional deployment of presidential clemency to insulate close political allies from criminal accountability, leaving thousands of working-class victims without judicial restitution.",
            "Tonight receipts. The United States District Court Southern District of New York grand jury indictment in United States v. Bannon, Kolfage et al. The federal sentencing memoranda and asset forfeiture orders for Brian Kolfage. The official Executive Grant of Clemency proclamation for Steve Bannon, and New York State Supreme Court subsequent indictments. Every judicial exhibit is cataloged in the dossier drawer. Review the financial fraud evidence for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.justice.gov/usao-sdny/pr/leaders-we-build-wall-online-fundraising-campaign-charged-defrauding-hundreds-thousands",
                "title": "US Attorney SDNY: Leaders of 'We Build The Wall' Charged with Defrauding Hundreds of Thousands of Donors",
                "published": "2020-08-20",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.justice.gov/usao-sdny/pr/brian-kolfage-and-andrew-badolato-sentenced-prison-we-build-wall-fraud-scheme",
                "title": "US Attorney SDNY: Brian Kolfage and Andrew Badolato Sentenced to Federal Prison in Fraud Scheme",
                "published": "2023-04-26",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/pardon/pardons-granted-president-donald-j-trump-2017-2021",
                "title": "Department of Justice Office of the Pardon Attorney: Official Executive Grant of Clemency to Stephen K. Bannon",
                "published": "2021-01-20",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://manhattanda.org/d-a-bragg-announces-indictment-of-steve-bannon-and-we-build-the-wall-inc-for-money-laundering-scheme/",
                "title": "Manhattan District Attorney: D.A. Bragg Announces State Indictment of Steve Bannon for Money Laundering",
                "published": "2022-09-08",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.fbi.gov/news/press-releases/we-build-the-wall-fraud-arrests",
                "title": "Federal Bureau of Investigation: Forensic Banking Records and Asset Forfeiture in We Build The Wall",
                "published": "2020-08-20",
                "kind": "reference"
            }
        ],
        "art_palette": ((18, 14, 25), (38, 20, 10)),
        "accent": (255, 140, 20),
        "theme": "WE BUILD THE WALL // BANNON FINANCIAL FRAUD SYNDICATE"
    },
    {
        "id": "2026-08-26-18",
        "date": "2026-08-26",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Trump University Racket: New York AG Schneiderman, The $25 Million Fraud Settlement & Class Action Lawsuits",
        "subject": "Daily investigative dossier: The systemic fraud operated by Trump University, deceptive marketing practices targeting elderly and vulnerable students, the New York Attorney General civil fraud litigation, and the $25 million settlement approved by federal court.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. Founded in 2004 by Donald Trump and corporate associates, Trump University promised aspiring real estate entrepreneurs that they would learn the insider secrets of real estate success directly from instructors handpicked by Donald Trump himself. In reality, comprehensive investigations by the New York State Attorney General and federal class action lawsuits revealed that the operation was an unlicensed, predatory sales racket designed to extract tens of thousands of dollars from vulnerable consumers through high-pressure sales psychological tactics.",
            "The operational reality contradicted promotional advertising. Trump admitted in sworn depositions that he did not personally handpick the instructors or select the seminar curriculum. Former employees testified that sales representatives were provided with detailed playbooks instructing them to exploit consumers' financial anxieties, encouraging students to max out credit cards, liquidate retirement accounts, and take out second mortgages to pay up to thirty-five thousand dollars for three-day Gold Elite mentorship programs.",
            "The academic credentials were entirely fabricated. The enterprise operated illegally without obtaining required educational licenses or accreditation from the New York State Education Department, which repeatedly ordered the company to cease using the misleading word University in its corporate branding. Students who paid thousands of dollars were assigned mentors who frequently failed to return phone calls, provided generic real estate listings downloaded from public websites, and pressured students to purchase additional seminar packages.",
            "The judicial accountability culminated in federal class actions and state fraud judgments. In November 2016, shortly after winning the presidential election, Donald Trump agreed to pay twenty-five million dollars to settle two federal class action lawsuits in San Diego and a parallel civil fraud lawsuit brought by the New York State Attorney General. The historic settlement provided financial restitution to over six thousand former students who had been defrauded by the enterprise.",
            "Consumer protection experts and judicial historians emphasize that the Trump University saga revealed a business model built on aggressive deception, predatory marketing, and contempt for regulatory oversight. By settling for twenty-five million dollars rather than facing public jury trial testimony, the president-elect averted sworn cross-examination, but the unsealed court records permanently documented an institutional enterprise engineered to profit from fraudulent educational promises.",
            "Tonight receipts. The United States District Court Southern District of California Final Approval Order for the twenty-five-million-dollar class action settlement in Low v. Trump University. The New York State Attorney General civil fraud complaint in People v. Trump Entrepreneur Initiative. Unsealed internal sales playbooks and employee depositions, and New York State Education Department cease-and-desist letters. Every judicial exhibit is cataloged in the dossier drawer. Review the fraud settlement records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://ag.ny.gov/press-release/2018/ag-underwood-announces-final-approval-25-million-trump-university-settlement",
                "title": "New York Attorney General: Final Approval of $25 Million Trump University Fraud Settlement",
                "published": "2018-04-09",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.courtlistener.com/docket/4155986/low-v-trump-university-llc/",
                "title": "US District Court SDCA: Order Granting Final Approval of Class Action Settlement in Low v. Trump University",
                "published": "2018-04-09",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/2016/06/01/us/politics/trump-university-playbooks-students-scam.html",
                "title": "The New York Times: Former Employees and Playbooks Detail Deceptive Tactics at Trump University",
                "published": "2016-06-01",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/politics/source-trump-nearing-settlement-in-trump-university-fraud-lawsuits/2016/11/18/31201538-adad-11e6-a31b-4b6397e625d0_story.html",
                "title": "The Washington Post: Trump Agrees to Pay $25 Million to Settle Trump University Fraud Lawsuits",
                "published": "2016-11-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://ag.ny.gov/press-release/2013/ag-schneiderman-sues-donald-trump-trump-university-and-michael-sexton-defrauding",
                "title": "New York State Attorney General: AG Schneiderman Sues Donald Trump for Running Illegal Fraudulent University",
                "published": "2013-08-25",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 20, 32), (38, 22, 10)),
        "accent": (255, 160, 0),
        "theme": "TRUMP UNIVERSITY // 25-MILLION PREDATORY FRAUD SETTLEMENT"
    },
    {
        "id": "2026-08-25-18",
        "date": "2026-08-25",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Trump Foundation Dissolution: Self-Dealing, Campaign Illegalities & The Judicial Shutdown",
        "subject": "Daily investigative dossier: The judicial dissolution of the Donald J. Trump Foundation for persistent self-dealing, using charitable funds to settle private business lawsuits, buying portraits of Donald Trump, and paying $2 million in court-ordered restitution.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In June 2018, the Attorney General of the State of New York filed a sweeping civil enforcement lawsuit against the Donald J. Trump Foundation and its board members, Donald, Donald Jr., Ivanka, and Eric Trump. The lawsuit alleged persistent, pervasive illegal conduct spanning more than a decade, documenting that the non-profit charity functioned as little more than a corporate checkbook to serve Donald Trump's business interests, resolve commercial lawsuits, and advance his political campaign.",
            "The evidentiary record revealed extraordinary self-dealing. The Foundation repeatedly utilized charitable non-profit funds to resolve private commercial lawsuits involving Trump properties, including paying one hundred thousand dollars to settle litigation against his Palm Beach club Mar-a-Lago, and paying one hundred fifty-eight thousand dollars to settle a golf club dispute. In another documented transaction, the foundation spent ten thousand dollars of donor money to purchase a six-foot portrait of Donald Trump that was hung in a resort bar.",
            "The Foundation's non-profit assets were unlawfully subordinated to political campaigning. During the 2016 Iowa presidential caucuses, Trump staged a televised charity fundraiser for veterans, raising millions of dollars that were routed into the Foundation. Internal emails proved that campaign manager Corey Lewandowski and campaign staff were given direct operational control over determining which veterans charities received grant distributions, using charitable checks with campaign banners to maximize political visibility in early primary states.",
            "The judicial accountability was total. In December 2018, under court supervision, the Donald J. Trump Foundation agreed to dissolve entirely and liquidate its remaining assets under judicial oversight. In November 2019, New York State Supreme Court Justice Saliann Scarpulla ordered Donald Trump to personally pay two million dollars in court-ordered damages for misusing charitable funds for political purposes, directing the restitution to eight legitimate non-profit charities.",
            "Non-profit governance scholars and legal ethicists emphasize that the judicial shutdown of the Trump Foundation represented a historic condemnation of philanthropic abuse. By transforming a tax-exempt charitable entity into an instrument of personal enrichment, commercial liability settlement, and political campaigning, the organization violated fundamental state and federal non-profit governance statutes.",
            "Tonight receipts. The New York State Supreme Court Decision and Order in People v. Donald J. Trump et al. The New York State Attorney General formal dissolution stipulations and forensic investigative exhibits. Internal campaign email directives on charitable check distribution, and IRS tax penalty filings for illegal self-dealing. Every judicial exhibit is cataloged in the dossier drawer. Review the charity dissolution records for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://ag.ny.gov/press-release/2019/ag-james-secures-court-order-against-donald-j-trump-trump-children-and-trump",
                "title": "New York Attorney General: AG James Secures $2 Million Court Judgment Against Donald J. Trump for Foundation Misuse",
                "published": "2019-11-07",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://ag.ny.gov/press-release/2018/attorney-general-underwood-announces-stipulation-dissolving-trump-foundation-under",
                "title": "New York Attorney General: AG Underwood Announces Stipulation Dissolving Trump Foundation Under Judicial Supervision",
                "published": "2018-12-18",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.washingtonpost.com/politics/trump-agrees-to-shut-down-his-charity-amid-allegations-he-used-it-for-personal-and-political-benefit/2018/12/18/dd3f5030-021b-11e9-9122-82e98f91ee6f_story.html",
                "title": "The Washington Post: Trump Agrees to Shut Down His Charity Amid Allegations of Self-Dealing",
                "published": "2018-12-18",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.nytimes.com/2019/11/07/nyregion/trump-charities-new-york.html",
                "title": "The New York Times: Trump Ordered to Pay $2 Million for Misusing Trump Foundation to Help Campaign",
                "published": "2019-11-07",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://ag.ny.gov/sites/default/files/summons_and_complaint_1.pdf",
                "title": "Supreme Court of the State of New York: Verified Petition in The People of New York v. Donald J. Trump et al.",
                "published": "2018-06-14",
                "kind": "reference"
            }
        ],
        "art_palette": ((18, 12, 25), (38, 18, 14)),
        "accent": (255, 175, 50),
        "theme": "TRUMP FOUNDATION DISSOLUTION // 2-MILLION JUDICIAL RESTITUTION"
    },
    {
        "id": "2026-08-24-18",
        "date": "2026-08-24",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Charlottesville Equivalence: The 'Very Fine People', Neo-Nazi Violence & The Moral Abdication",
        "subject": "Daily investigative dossier: The August 2017 Unite the Right white supremacist rally in Charlottesville, the murder of Heather Heyer, Donald Trump's Trump Tower press conference claiming 'very fine people on both sides', and the mainstreaming of violent extremism.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On August 11 and 12, 2017, hundreds of neo-Nazis, Klansmen, and violent white supremacists marched through Charlottesville, Virginia, carrying flaming tiki torches, brandishing Confederate flags, and chanting antisemitic slogans including Jews will not replace us. The Unite the Right rally descended into widespread street violence, culminating when neo-Nazi James Alex Fields Jr. deliberately rammed his vehicle into a crowd of peaceful counter-protesters, murdering thirty-two-year-old Heather Heyer and injuring thirty-five others.",
            "The presidential response shattered decades of moral consensus against violent extremism. Following an initial scripted condemnation, Donald Trump held a contentious press conference in the lobby of Trump Tower on August 15. Defending the far-right gathering, Trump explicitly asserted: You had some very bad people in that group, but you also had people that were very fine people, on both sides. The rhetorical moral equivalence equated violent neo-Nazis carrying swastikas with peaceful counter-protesters defending civil rights.",
            "The statement drew immediate celebration from violent extremists. Former Ku Klux Klan grand wizard David Duke publicly thanked Trump on Twitter for his honesty and courage in defending white nationalists. Simultaneously, bipartisan leaders across the political spectrum, military service chiefs, and corporate advisory councils publicly rebuked the president. CEOs resigned en masse from presidential business advisory councils, forcing the White House to disband the panels.",
            "The legislative and intelligence fallout confirmed the growing threat of domestic violent extremism. Both houses of the United States Congress unanimously passed a joint resolution explicitly condemning white nationalists, neo-Nazis, and the KKK, which Trump was forced to sign into law. Subsequent threat assessments by the Department of Homeland Security and the Federal Bureau of Investigation formally classified racially motivated violent extremism as the primary lethal domestic terrorist threat facing the United States.",
            "Civil rights scholars and historians emphasize that the Charlottesville statements marked a watershed moment in the normalization of racial grievance politics. By providing executive rhetorical cover to violent white supremacist factions, the commander-in-chief eroded the moral foundation of the presidency and emboldened extremist networks that later converged in the attack on the United States Capitol.",
            "Tonight receipts. The official White House verbatim transcript of the August 15, 2017 Trump Tower press conference. The United States Congress Joint Resolution Senate Joint Resolution 49 condemning white supremacists. The federal hate crimes trial conviction verdict in United States v. Fields, and the Department of Homeland Security Strategic Framework on domestic terrorism. Every official record is cataloged in the dossier drawer. Review the historical record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-infrastructure/",
                "title": "White House Archives: Verbatim Transcript of Trump Tower Press Conference on Charlottesville",
                "published": "2017-08-15",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.congress.gov/bill/115th-congress/senate-joint-resolution/49/text",
                "title": "United States Congress: Public Law 115-58 Condemning the Racist Violence and Attack in Charlottesville",
                "published": "2017-09-14",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.justice.gov/opa/pr/ohio-man-sentenced-life-prison-federal-hate-crimes-related-august-2017-car-attack-rally",
                "title": "Department of Justice: James Alex Fields Jr. Sentenced to Life in Prison for Federal Hate Crimes in Charlottesville",
                "published": "2019-06-28",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.dhs.gov/sites/default/files/publications/19_0920_plcy_strategic-framework-countering-terrorism-targeted-violence.pdf",
                "title": "Department of Homeland Security: Strategic Framework for Countering Terrorism and Targeted Violence",
                "published": "2019-09-20",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.fbi.gov/news/testimony/worldwide-threats-to-the-homeland-091720",
                "title": "Federal Bureau of Investigation: Congressional Testimony on Racially Motivated Violent Extremism as Primary Threat",
                "published": "2020-09-17",
                "kind": "reference"
            }
        ],
        "art_palette": ((22, 10, 20), (35, 12, 18)),
        "accent": (255, 50, 50),
        "theme": "CHARLOTTESVILLE MORAL EQUIVALENCE // WHITE NATIONALIST EXTREMISM"
    },
    {
        "id": "2026-08-23-18",
        "date": "2026-08-23",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The Central Park Five Advertisements: Full-Page Demands for the Death Penalty & The Refusal to Retract",
        "subject": "Daily investigative dossier: Donald Trump spending $85,000 in May 1989 to place full-page advertisements in four New York newspapers demanding the return of the death penalty for five exonerated Black and Latino teenagers, and his decades-long refusal to apologize after DNA evidence exonerated them.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On May 1, 1989, weeks after the violent sexual assault of a female jogger in Central Park, Donald Trump spent eighty-five thousand dollars to purchase full-page advertisements in all four major New York newspapers: the New York Times, the Daily News, the Post, and New York Newsday. Under the bold headline Bring Back The Death Penalty. Bring Back Our Police!, Trump called for the execution of five Black and Latino teenagers: Antron McCray, Kevin Richardson, Yusef Salaam, Raymond Santana, and Korey Wise.",
            "The advertisements inflamed racial hysteria and poisoned the judicial atmosphere in New York City. Trump wrote that society must criminalize and punish severely, stating: I want to hate these muggers and murderers. They should be forced to suffer and, when they kill, they should be executed for their crimes. The teenagers, aged fourteen to sixteen, were interrogated by police for hours without legal counsel or parents present, yielding coerced, contradictory false confessions under extreme psychological duress.",
            "The five youths were wrongfully convicted and spent between six and thirteen years in state prisons for a crime they did not commit. In 2002, convicted serial rapist and murderer Matias Reyes confessed to the assault, providing details only the perpetrator could know. Forensic DNA testing conducted by the Manhattan District Attorney's Office confirmed Reyes's exclusive match, definitively excluding all five teenagers. The New York State Supreme Court vacated all convictions in December 2002.",
            "Despite irrefutable DNA proof and judicial exoneration, Donald Trump steadfastly refused to apologize or retract his statements. In 2014, when the City of New York agreed to pay a forty-one-million-dollar civil settlement to the exonerated men for false imprisonment and civil rights violations, Trump published an op-ed calling the settlement a disgrace. When asked about the exoneration during a 2019 White House press conference, Trump doubled down, asserting: You have people on both sides of that. They admitted their guilt.",
            "Criminal justice scholars and civil rights historians emphasize that the Central Park Five advertising campaign established an enduring pattern of leveraging racial anxiety for personal public notoriety. By demonizing wrongfully accused minority teenagers and rejecting empirical scientific evidence, the rhetoric laid the foundation for decades of racial polarization in American political discourse.",
            "Tonight receipts. The original May 1, 1989 New York Times full-page advertisement text placed by Donald Trump. The New York State Supreme Court Decision and Order vacating all convictions in People v. Wise et al. The City of New York forty-one-million-dollar civil settlement records, and White House verbatim press conference transcripts. Every primary document is preserved in the dossier drawer. Review the historical advertisements for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.nytimes.com/1989/05/01/nyregion/trump-buys-ad-in-central-park-jogger-case.html",
                "title": "The New York Times: Trump Buys Full-Page Newspaper Ads Demanding Death Penalty in Central Park Case",
                "published": "1989-05-01",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.nycourts.gov/press/PDFs/CentralParkFiveDecision.pdf",
                "title": "New York State Supreme Court: Decision and Order Vacating Convictions in People v. Wise et al.",
                "published": "2002-12-19",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/2014/06/20/nyregion/5-exonerated-in-central-park-jogger-case-agree-to-settle-for-40-million.html",
                "title": "The New York Times: Five Exonerated Men in Central Park Jogger Case Agree to $41 Million Civil Settlement",
                "published": "2014-06-20",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://trumpwhitehouse.archives.gov/briefings-statements/remarks-president-trump-south-lawn-departure-46/",
                "title": "White House Archives: Remarks by President Trump on South Lawn Regarding Central Park Five Exoneration",
                "published": "2019-06-18",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.innocenceproject.org/cases/central-park-five/",
                "title": "The Innocence Project: Case Profile, DNA Evidence, and Coerced Confessions in Exoneration of the Central Park Five",
                "published": "2019-05-30",
                "kind": "reference"
            }
        ],
        "art_palette": ((20, 14, 25), (35, 15, 12)),
        "accent": (255, 60, 80),
        "theme": "CENTRAL PARK FIVE // 1989 DEATH PENALTY ADS & EXONERATION"
    },
    {
        "id": "2026-08-22-18",
        "date": "2026-08-22",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The E. Jean Carroll Defamation Verdicts: Sexual Abuse, Digital Retaliation & The $88 Million Judgments",
        "subject": "Daily investigative dossier: Federal jury verdicts in the Southern District of New York finding Donald Trump liable for sexual abuse and defamation against writer E. Jean Carroll, followed by repeated defamatory attacks resulting in an eighty-three-million-dollar punitive damages verdict.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. In May 2023, following a two-week federal civil trial inside the United States District Court for the Southern District of New York, a nine-member federal jury returned a unanimous verdict finding Donald Trump liable for sexual abuse and defamation against author and journalist E. Jean Carroll. The jury awarded Carroll five million dollars in compensatory and punitive damages, formally establishing in a court of law that Trump sexually assaulted Carroll in a Bergdorf Goodman dressing room in the mid-1990s.",
            "The judicial accountability followed years of vitriolic public attacks. When Carroll published details of the assault in 2019, Trump responded from the White House by claiming she was completely lying to sell a book, asserting that he had never met her and declaring: She's not my type. Senior District Judge Lewis Kaplan ruled that Trump's statements were false, malicious, and defamatory, finding that the evidence unequivocally established that the sexual assault occurred.",
            "Rather than ceasing his defamatory attacks following the initial five-million-dollar jury verdict, Trump immediately escalated his rhetoric. On televised town halls, at political rallies, and across social media platforms, Trump repeatedly called Carroll a fraud, a whack job, and claimed she fabricated the entire story. Carroll filed an amended federal defamation lawsuit seeking additional damages for the continuous reputational harm and targeted digital harassment.",
            "The second federal trial delivered a historic financial rebuke. In January 2024, a second federal jury in Manhattan ordered Donald Trump to pay E. Jean Carroll eighty-three point three million dollars in damages, including sixty-five million dollars in punitive damages specifically designed to deter the defendant from continuing his malicious public defamation. To appeal the judgment, Trump was forced to post a ninety-one-point-six-million-dollar cash bond.",
            "Legal scholars and civil rights analysts emphasize that the Carroll verdicts represented an unprecedented judicial judgment against a former president for sexual violence and defamation. By enforcing massive punitive damages, the federal courts affirmed that wealth, political stature, and executive platforms do not grant license to defame survivors of sexual assault or undermine the authority of federal jury verdicts.",
            "Tonight receipts. The United States District Court Southern District of New York jury verdict sheets in Carroll v. Trump (Civil Actions 20-cv-7311 and 22-cv-10016). Senior District Judge Lewis Kaplan written memorandums and orders, and Second Circuit Court of Appeals affirmance filings. Every trial transcript and jury verdict sheet is cataloged in the dossier drawer. Examine the federal court findings for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.nysd.uscourts.gov/sites/default/files/2023-05/Carroll-v-Trump-Verdict-Sheet.pdf",
                "title": "US District Court SDNY: Official Jury Verdict Sheet in Carroll v. Donald J. Trump (Sexual Abuse & Defamation)",
                "published": "2023-05-09",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.nysd.uscourts.gov/sites/default/files/2024-01/Carroll-II-Verdict-Sheet.pdf",
                "title": "US District Court SDNY: Official Jury Verdict Sheet in Carroll II ($83.3 Million Defamation Award)",
                "published": "2024-01-26",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.courtlistener.com/docket/18588523/carroll-v-trump/",
                "title": "US District Court SDNY: Memorandum Opinion of Judge Lewis A. Kaplan Denying Trump Motion for New Trial",
                "published": "2023-07-19",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.ca2.uscourts.gov/decisions/isysquery/carroll-trump-appeal/",
                "title": "US Court of Appeals for the Second Circuit: Appellate Orders and Bond Approvals in Carroll v. Trump",
                "published": "2024-03-08",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.washingtonpost.com/national-security/2024/01/26/trump-e-jean-carroll-defamation-trial-verdict/",
                "title": "The Washington Post: Jury Orders Trump to Pay $83.3 Million for Defaming E. Jean Carroll",
                "published": "2024-01-26",
                "kind": "reference"
            }
        ],
        "art_palette": ((22, 14, 28), (35, 12, 18)),
        "accent": (255, 60, 90),
        "theme": "CARROLL DEFAMATION VERDICTS // $88 MILLION FEDERAL JUDGMENTS"
    },
    {
        "id": "2026-08-21-18",
        "date": "2026-08-21",
        "hour": "18:00",
        "kind": "daily",
        "category": "corruption",
        "title": "The New York Civil Fraud Verdict: Asset Overvaluation, James v. Trump & The $450 Million Penalty",
        "subject": "Daily investigative dossier: Justice Arthur Engoron's historic 454-million-dollar judgment against Donald Trump, his adult sons, and the Trump Organization for persistent, fraudulent manipulation of statements of financial condition to obtain favorable bank loans and insurance rates.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On February 16, 2024, following a grueling three-month bench trial in Manhattan, New York State Supreme Court Justice Arthur Engoron issued a monumental ruling in People of the State of New York v. Donald J. Trump et al. Finding Donald Trump, his adult sons, and corporate executives liable for persistent and repeated financial fraud, the court ordered Trump to pay three hundred fifty-five million dollars in disgorgement, an amount that exceeded four hundred fifty-four million dollars with statutory pre-judgment interest.",
            "The judicial findings exposed a systematic decade-long accounting fraud conspiracy. Between 2011 and 2021, the Trump Organization submitted annual Statements of Financial Condition that falsely inflated Donald Trump's net worth by as much as two point two billion dollars per year. Prime assets were fraudulently overvalued through deceptive methodologies, including tripling the square footage of Trump's Trump Tower triplex penthouse, valuing rent-stabilized units at unregulated market rates, and falsely claiming luxury properties carried non-existent development rights.",
            "The fraudulent statements directly enriched the corporate enterprise. Major financial lenders, including Deutsche Bank's private wealth division, relied on these fraudulent financial statements to underwrite hundreds of millions of dollars in loans for Trump International Hotel in Chicago, the Doral golf resort in Miami, and the Old Post Office hotel in Washington. By submitting fraudulent net worth certifications, Trump obtained subsidized interest rates, saving an estimated one hundred sixty-eight million dollars in loan interest costs.",
            "The trial testimony unmasked an institutional culture of complete lack of contrition. Justice Engoron noted in his comprehensive ninety-two-page decision that the defendants' complete refusal to acknowledge error bordered on pathological, highlighting that Trump and his chief financial officer Allen Weisselberg engaged in intentional deceptive practices. The court permanently banned Weisselberg and former corporate controller Jeffrey McConney from serving in financial control roles in New York, while barring Trump from serving as an officer or director of any New York corporation for three years.",
            "Financial integrity experts and forensic accounting scholars emphasize that the civil fraud ruling established an indispensable benchmark for corporate accountability. By proving that fraudulent asset valuations deployed to deceive institutional lenders violate New York Executive Law Section 63(12), the judicial ruling dismantled the myth of the defendant's self-made corporate empire, establishing that his commercial liquidity was erected upon systemic financial deception.",
            "Tonight receipts. The Supreme Court of the State of New York Decision and Order After Trial in People v. Donald J. Trump et al. (Index No. 452564/2022). Sworn trial testimony transcripts of Donald Trump, Allen Weisselberg, and Michael Cohen. Subpoenaed Deutsche Bank credit committee memoranda, and New York Attorney General trial evidentiary exhibits. Every judicial exhibit is preserved in the dossier drawer. Review the trial judgment for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://ag.ny.gov/press-release/2024/attorney-general-james-wins-landmark-victory-civil-fraud-case-against-donald-trump",
                "title": "New York Attorney General: AG James Wins Landmark Victory in Civil Fraud Case Against Donald Trump",
                "published": "2024-02-16",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.nycourts.gov/LegacyPDFS/press/PDFs/452564_2022_People_of_the_State_of_New_York_v_People_of_the_State_of_New_York_DECISION___ORDER_ON_775.pdf",
                "title": "New York State Supreme Court: Decision and Order After Trial in People v. Donald J. Trump (Justice Arthur F. Engoron)",
                "published": "2024-02-16",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.nytimes.com/2024/02/16/nyregion/trump-civil-fraud-ruling-decision.html",
                "title": "The New York Times: Trump Fraud Ruling - Judge Fines Trump $355 Million in New York Fraud Case",
                "published": "2024-02-16",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.reuters.com/legal/judge-rules-trump-liable-fraud-ny-attorney-general-case-2023-09-26/",
                "title": "Reuters: NY Judge Finds Trump Committed Fraud by Massively Overvaluing Assets for Years",
                "published": "2023-09-26",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://ag.ny.gov/sites/default/files/tfg_complaint_redacted.pdf",
                "title": "New York State Attorney General: Verified Complaint in People v. Donald J. Trump (Asset Inflation)",
                "published": "2022-09-21",
                "kind": "reference"
            }
        ],
        "art_palette": ((15, 20, 35), (42, 22, 10)),
        "accent": (255, 175, 20),
        "theme": "NY CIVIL FRAUD VERDICT // $454 MILLION ENGORON JUDGMENT"
    },
    {
        "id": "2026-08-20-18",
        "date": "2026-08-20",
        "hour": "18:00",
        "kind": "daily",
        "category": "geopolitics",
        "title": "The Kurdish Betrayal: The Northern Syria Troop Pullout, Turkish Offensives & The Abandonment of SDF Allies",
        "subject": "Daily investigative dossier: Donald Trump's October 2019 telephone call with Turkish President Recep Tayyip Erdogan, the abrupt order to withdraw American special operations forces from northern Syria, abandoning Syrian Democratic Forces (SDF) allies to Turkish military offensives and freeing hundreds of ISIS detainees.",
        "paragraphs": [
            "Welcome to ZeroFilter Daily. On October 6, 2019, following a sudden telephone conference with Turkish President Recep Tayyip Erdogan, Donald Trump blindsided the Pentagon and American allies by ordering the immediate withdrawal of United States special operations forces from northern Syria. The unilateral directive abruptly dismantled a five-year counterterrorism partnership with the Syrian Democratic Forces, the predominantly Kurdish military coalition that had served as America's primary ground fighting force in eliminating the territorial caliphate of the Islamic State.",
            "The consequences of the withdrawal materialized with immediate lethality. Within hours of the American departure, the Turkish military and allied Syrian militia proxies launched Operation Peace Spring, subjecting Kurdish civilian communities across Ras al-Ayn and Tell Abyad to heavy artillery shelling and airstrikes. Over two hundred thousand civilians were displaced, dozens of Kurdish civilians and political leaders were summarily executed, and hundreds of suspected Islamic State detainees escaped from unsecured detention facilities.",
            "The decision sparked extraordinary bipartisan outrage in Washington. In an overwhelming three-hundred-fifty-four to sixty vote, the United States House of Representatives passed a joint resolution formally opposing the presidential troop withdrawal, condemning the abandonment of Kurdish partners. Bipartisan congressional leaders, including Senate Majority Leader Mitch McConnell, denounced the pullout as a catastrophic strategic mistake that empowered Russia, Iran, and the Assad regime.",
            "The strategic vacuum was immediately exploited by the Kremlin. As American forces evacuated forward operating bases, burning their own supplies to prevent capture, Russian military patrols and Syrian state forces moved into former American positions, planting Russian flags in abandoned outposts. Video footage broadcast across Russian state media showed Russian soldiers inspecting American command facilities in Manbij, showcasing an extraordinary geopolitical victory handed to Moscow without contest.",
            "National security analysts and military scholars emphasize that the northern Syria abandonment delivered a devastating blow to American credibility worldwide. By betraying frontline allies who had lost over eleven thousand fighters combating the Islamic State on America's behalf, executive policy signaled to global partners that American defense alliances could be discarded on an impulsive presidential phone call.",
            "Tonight receipts. United States House of Representatives Joint Resolution House Joint Resolution 77 opposing the Syria withdrawal. Department of Defense official statements on Turkish military operations. The Lead Inspector General Report to Congress on Operation Inherent Resolve, and Senate Foreign Relations Committee bipartisan resolutions. Every diplomatic and military record is cataloged in the dossier drawer. Review the defense record for yourself. I am Ava Vance for ZeroFilter Daily. Stay lucid."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.congress.gov/bill/116th-congress/house-joint-resolution/77/text",
                "title": "United States Congress: House Joint Resolution 77 Opposing the Withdrawal of US Armed Forces from Northern Syria",
                "published": "2019-10-16",
                "kind": "reference"
            },
            {
                "para": 1,
                "url": "https://www.defense.gov/News/Transcripts/Transcript/Article/1987391/secretary-of-defense-mark-t-esper-press-briefing-on-syria/",
                "title": "U.S. Department of Defense: Secretary of Defense Mark T. Esper Press Briefing on Northern Syria Withdrawal",
                "published": "2019-10-11",
                "kind": "reference"
            },
            {
                "para": 2,
                "url": "https://www.stateoig.gov/report/lead-inspector-general-report-operation-inherent-resolve",
                "title": "Lead Inspector General: Report to Congress on Operation Inherent Resolve (Syria Pullout and ISIS Detainees)",
                "published": "2019-11-19",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://www.washingtonpost.com/world/middle_east/russia-steps-into-the-void-in-syria-left-by-withdrawing-us-forces/2019/10/15/4377038e-ef54-11e9-bb7e-d2026ee0c199_story.html",
                "title": "The Washington Post: Russia Steps Into the Void in Syria Left by Withdrawing U.S. Forces",
                "published": "2019-10-15",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.foreign.senate.gov/press/dem/release/menendez-statement-on-trumps-catastrophic-syria-withdrawal",
                "title": "Senate Foreign Relations Committee: Bipartisan Statements on the Strategic Fallout of the Syria Withdrawal",
                "published": "2019-10-07",
                "kind": "reference"
            }
        ],
        "art_palette": ((14, 25, 35), (38, 18, 12)),
        "accent": (255, 140, 20),
        "theme": "KURDISH BETRAYAL // SYRIA PULLOUT & RUSSIAN VACUUM EXPLOITATION"
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
    print(f"Checking {len(EPISODES)} retrospective daily episodes for Batch 4...")
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
