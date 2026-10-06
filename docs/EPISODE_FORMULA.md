# ZeroFilter: The 3-Minute Hourly Episode Formula

## 0. Sourcing & Dating Rules — NON-NEGOTIABLE (owner, 2026-10-06)

"Make sure we're not creating fake quotes or fake news." Enforced in code by
`engine/editorial.mjs`: an episode that breaks a rule cannot pass the tests
and cannot be deployed. The 151 episodes made before these rules are held in
`data/held/` and are off the site.

1. **Write from real, published items only.** Each hour's script is written
   from news items, papers and statements that already exist and were
   published BEFORE that hour. A topic list is not a source; never invent an
   event, a number, a vote, a strike, a study or a result.
2. **Every claim paragraph cites its sources** (P0–P4, at least one each) in
   the episode's `sources` array: `{ para, url, title, published, speaker? }`,
   https links, `published` on or before the episode date. The site shows them.
3. **No source, no quote.** A real person (Yuri Shvets included) is quoted or
   paraphrased only from something they actually published, and that source
   carries `speaker: "<their name>"`. No "as Shvets pointed out…" without the
   link to where he said it. If he said nothing on the topic this hour, he is
   not in the episode.
4. **Never dated ahead.** An episode is stamped with the hour it is actually
   published. Producing a batch for "tomorrow 09:00" is fabricating the news
   before it happens.
5. **Opinion is labelled as opinion.** Rex's takes, jokes and profanity are
   fine; they must not be phrased as facts the sources don't support.
6. **Science claims match the paper.** Cite the paper (Nature, Science, PRL,
   arXiv…) and say what it showed — contested findings (e.g. PEAR, Stargate)
   are presented with the critique next to the claim.
7. **Cite only what was collected.** Each episode names its ingest snapshot
   (`"ingest": "YYYY-MM-DD-HH"`, made by `node engine/ingest.mjs` at that
   hour from `data/feeds.json`). P0/P1 news sources and every quote must be
   URLs in that snapshot; a quote must come from the speaker's own feed.
   Older stable references (papers, archives) are allowed in P2–P4 with
   `kind: "reference"`.

---

## 1. Episode Blueprint (180 Seconds / ~460 Words)
ZeroFilter is an hourly, compressed, high-impact intelligence brief. Every release runs for exactly **3 minutes (180 seconds)** spoken at a brisk, energetic pace (~150–160 words per minute).

There is zero filler, zero corporate PR fluff, and zero local trivia ("car hit a tree in Milwaukee"). Every paragraph hits high-stakes reality.

```
+---------------------------------------------------------------------------------------+
| MINUTE 1 (0:00 - 1:00) : GEOPOLITICAL FIRESTORM (50% US / 50% GLOBAL)                  |
| - 50% US: Corruption & hypocrisy exposed on BOTH sides (MAGA authoritarians & corporate |
|   establishment Democrats). White Christian nationalism dismantled.                  |
| - 50% Global: Frontline defense of Ukraine, Taiwan, anti-authoritarian axis, and      |
|   uncompromising exposure of radical theocratic subversion / Islamization.            |
+---------------------------------------------------------------------------------------+
| MINUTE 2 (1:00 - 2:00) : FRONTIER SCIENCE & HIGH-TECH BREAKTHROUGHS                   |
| - AI frontier models, algorithmic autonomy & compute scaling.                         |
| - Quantum physics: Wheeler's delayed-choice (half-mirrored experiment), entanglement, |
|   macroscopic superposition, observer effect & reality emergence.                     |
| - Genetic engineering: CRISPR-Cas12/Cas9 breakthroughs, synthetic biology, longevity. |
+---------------------------------------------------------------------------------------+
| MINUTE 3 (2:00 - 3:00) : ESOTERIC FRONTIERS & CONSCIOUSNESS SCIENCE                  |
| - Declassified intelligence: CIA Project Stargate, coordinate remote viewing (CRV).   |
| - Rigorous anomaly labs: Princeton Engineering Anomalies Research (PEAR), micro-PK.  |
| - Foundational theorists: Thomas Campbell (My Big TOE), Robert Monroe (Gateway / Hemi-|
|   Sync), Alan Watts philosophical insights, simulation hypothesis (Nick Bostrom).    |
| - Sign-off: Punchy, cynical, razor-sharp reality anchor.                             |
+---------------------------------------------------------------------------------------+
```

---

## 2. Minute-by-Minute Editorial Rules

### Minute 1: Geopolitics & Political Corruption (0:00 - 1:00)
* **The 50/50 Split:** Exactly 30 seconds focused on US power structures, and 30 seconds on critical global battlegrounds.
* **Quoting analysts (Yuri Shvets and others):** only from what they actually published, linked as a `speaker` source (rule 0.3). Never as a standing "wire" that supplies facts the episode does not source.
* **Equal-Opportunity Cynicism:**
  * **MAGA / White Christian Nationalism:** Call out theocratic fascism, attacks on judicial independence, Kremlin-aligned isolationist grift, book bans, and cult-like devotion to authoritarian demagogues.
  * **Corporate / Establishment Democrats:** Tear apart cowardly inaction, insider trading, donor capture, performative identity politics, and bureaucratic corruption. No partisan excuses.
* **Global Frontlines:**
  * **Ukraine:** Unwavering factual backing for Ukrainian sovereignty against Russian fascist aggression; expose western appeasers, weapons delivery bottlenecks, and corrupt delays.
  * **Anti-Theocracy & Anti-Islamization:** Direct, fearless exposure of radical Islamist extremism, sharia courts subverting secular law, human rights repression, and cowardice in Western media refusing to name the threat.

### Minute 2: Frontier Science (1:00 - 2:00)
* **Pure Hard Evidence:** No pop-science clickbait. Cite peer-reviewed papers (Nature, Science, arXiv, PRL).
* **Quantum Reality:**
  * Wheeler's delayed-choice half-mirrored interferometer experiment (the photon has no definite path until measured; Jacques et al., Science 2007 — not retrocausation).
  * Quantum entanglement and Bell inequality violations.
  * Quantum computing error correction and topological qubits.
* **Genetic Engineering & AI:**
  * Next-gen gene editing (base editing, prime editing, epigenetic rejuvenation).
  * Frontier AI architectures, reasoning tokens, autonomous code synthesis.

### Minute 3: Consciousness & Esoteric Anomalies (2:00 - 3:00)
* **Demystified & Evidence-Backed:**
  * Declassified CIA/DIA documents from Project Stargate (Ingo Swann, Pat Price, Hal Puthoff at SRI).
  * PEAR Lab (Robert Jahn and Brenda Dunne at Princeton): Statistical anomalies in random event generators (REGs) influenced by conscious intention.
  * Thomas Campbell's *My Big TOE* (Theory of Everything): Reality as an informational simulation, consciousness as the fundamental substrate.
  * Robert Monroe & The Monroe Institute: Gateway Experience, Hemi-Sync binaural audio brain synchronization, non-local awareness.
  * Alan Watts & Eastern non-dualism meeting Western physics: Reality as a unified process, the illusion of the isolated ego.
  * Nick Bostrom's Simulation Hypothesis: Probabilistic arguments for living in a high-fidelity digital universe.
* **Dosing Strategy:** Each hourly episode features **one specific frontier concept** paired with concrete details, avoiding information overload while building an interconnected mental model over weeks of broadcasting.

---

## 3. Paragraph Structure
Each 3-minute episode contains **6 structured paragraphs**:
1. **P0 (Lead-In / US Politics):** ~75 words.
2. **P1 (Global Frontline / Ukraine / Theocracy Exposed):** ~75 words.
3. **P2 (AI & Frontier Compute):** ~75 words.
4. **P3 (Quantum Physics / Half-Mirrored Reality):** ~75 words.
5. **P4 (Esoteric / Remote Viewing / Consciousness):** ~85 words.
6. **P5 (Synthesis / Razor-Sharp Sign-off):** ~75 words.

Total word count: **450–480 words**.
Total duration: **180 seconds (3:00 min)**.
