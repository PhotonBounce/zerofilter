// unit.mjs — Automated test suite for ZeroFilter release manifests and engine

import { readFileSync, existsSync, readdirSync } from "node:fs";
import { resolve, join } from "node:path";
import { createHash } from "node:crypto";
import { parseEpisodes, validateEpisode, cueStarts, paragraphAt, escapeHtml, MIN_DURATION, MAX_DURATION } from "../web/js/episodes.js";
import { webpSize, mp3Info, isMp4 } from "./media.mjs";
import { editorialProblems, provenanceProblems } from "./editorial.mjs";
import { parseFeed, inWindow, hourId, clockSkewMs, MAX_CLOCK_SKEW_MS } from "./ingest.mjs";
import { CATEGORIES } from "../web/js/categories.js";

const ROOT = resolve(import.meta.dirname, "..");
const FEEDS = JSON.parse(readFileSync(join(ROOT, "data/feeds.json"), "utf8")).feeds;
let passed = 0, failed = 0, warned = 0;

// Story art and covers fill a 16:9 stage with object-fit: cover. Both sizes the
// generators produce (1376x768 and 1280x720) are fine; a portrait or tiny image
// is not.
const MIN_ART_W = 1280, ART_ASPECT = 16 / 9, ASPECT_TOLERANCE = 0.02;
// The manifest duration drives the seek bar and the cue maths; it must agree
// with the audio file to within this many seconds.
const DURATION_TOLERANCE = 1.5;

function warn(title) {
  console.warn(`  ! ${title}`);
  warned++;
}
const read = (rel) => readFileSync(join(ROOT, "web", rel));
const md5 = (buf) => createHash("md5").update(buf).digest("hex");

function ok(title, condition) {
  if (condition) {
    console.log(`  ✓ ${title}`);
    passed++;
  } else {
    console.error(`  ✗ ${title}`);
    failed++;
  }
}

console.log("=== ZeroFilter Test Suite ===");

// 1. Manifest verification
console.log("\n1. Validating web/data/episodes.json:");
const manifestPath = join(ROOT, "web/data/episodes.json");
ok("episodes.json exists", existsSync(manifestPath));

const raw = JSON.parse(readFileSync(manifestPath, "utf8"));
const episodes = parseEpisodes(raw);
// The feed may be empty: nothing is published until it passes the editorial gate.
ok(`every manifest entry is a valid episode (${episodes.length} published)`, episodes.length === (raw.episodes || raw).length);

// 1b. Editorial gate — no fake quotes, no fake news, nothing dated ahead.
console.log("\n1b. Editorial gate (engine/editorial.mjs):");
for (const ep of episodes) {
  const snapPath = ep.ingest ? join(ROOT, "data/ingest", `${ep.ingest}.json`) : null;
  const snapshot = snapPath && existsSync(snapPath) ? JSON.parse(readFileSync(snapPath, "utf8")) : null;
  const problems = [...editorialProblems(ep), ...provenanceProblems(ep, snapshot, Date.now(), FEEDS)];
  ok(`[${ep.id}] passes the editorial gate${problems.length ? ": " + problems.join("; ") : ""}`, problems.length === 0);
}
for (const f of existsSync(join(ROOT, "data/held")) ? readdirSync(join(ROOT, "data/held")).filter((n) => n.endsWith(".json")) : []) {
  const held = JSON.parse(readFileSync(join(ROOT, "data/held", f), "utf8"));
  // Compared by content, not id: a real episode may later be written for an
  // hour a held one had claimed (2026-10-08-00 was one of the 151).
  const published = new Set(episodes.map((e) => e.paragraphs.join("\n")));
  ok(`held episodes in ${f} (${held.episodes.length}) are not in the published feed`, held.episodes.every((e) => !published.has((e.paragraphs || []).join("\n"))));
}

// 2. Strict episode schema & duration rules
console.log("\n2. Validating 3-Minute Formula Rules:");
for (const ep of episodes) {
  console.log(`\n  Checking episode [${ep.id}]: "${ep.title}"`);
  
  ok("duration within 3-minute target bounds (150s - 210s)", ep.seconds >= MIN_DURATION && ep.seconds <= MAX_DURATION);
  ok("has exactly 6 structured paragraphs", ep.paragraphs.length === 6);
  
  const totalWords = ep.paragraphs.join(" ").split(/\s+/).filter(Boolean).length;
  ok(`word count in target broadcast range (~400-520 words, actual: ${totalWords})`, totalWords >= 380 && totalWords <= 550);
  
  ok("category is valid in taxonomy", Object.prototype.hasOwnProperty.call(CATEGORIES, ep.category));
  ok("thumb path matches standard thumbs/<id>.webp", ep.thumb === `thumbs/${ep.id}.webp`);
  ok("cover_video matches thumbs/<id>.mp4", ep.cover_video === `thumbs/${ep.id}.mp4`);
  ok("has at least 4 story art frames", ep.art?.frames?.length >= 4);

  // Validate frame timestamp ordering
  let prevT = -1;
  let monotonic = true;
  for (const f of ep.art.frames) {
    if (f.t < prevT) { monotonic = false; break; }
    prevT = f.t;
  }
  ok("art frame timestamps are monotonically increasing", monotonic);

  // --- Media integrity: the files the manifest points at ---
  const audioPath = join(ROOT, "web", ep.audio);
  ok(`audio file exists (${ep.audio})`, existsSync(audioPath));
  if (existsSync(audioPath)) {
    const info = mp3Info(readFileSync(audioPath));
    ok("audio is a decodable MP3 (frame headers found)", !!info);
    if (info) {
      ok(`manifest seconds (${ep.seconds}) matches audio length (${info.seconds.toFixed(1)}s) within ${DURATION_TOLERANCE}s`,
        Math.abs(info.seconds - ep.seconds) <= DURATION_TOLERANCE);
    }
  }
  for (const rel of [ep.thumb, ...ep.art.frames.map((f) => f.src)]) {
    const p = join(ROOT, "web", rel);
    if (!existsSync(p)) { ok(`image exists (${rel})`, false); continue; }
    const size = webpSize(readFileSync(p));
    ok(`${rel} is a 16:9 WebP at least ${MIN_ART_W}px wide${size ? ` (got ${size.width}x${size.height})` : " (unreadable header)"}`,
      !!size && size.width >= MIN_ART_W && Math.abs(size.width / size.height / ART_ASPECT - 1) <= ASPECT_TOLERANCE);
  }
  const mp4 = join(ROOT, "web", ep.cover_video);
  ok(`cover video is an MP4 (${ep.cover_video})`, existsSync(mp4) && isMp4(readFileSync(mp4)));

  // --- Sync: every frame and cue must land inside the audio ---
  ok("every art frame starts before the audio ends", ep.art.frames.every((f) => f.t >= 0 && f.t < ep.seconds));
  ok("first art frame starts at 0s", ep.art.frames[0]?.t === 0);
  const starts = cueStarts(ep);
  ok("cue starts are increasing, begin at 0 and end before the audio does",
    starts[0] === 0 && starts.every((s, i) => i === 0 || s > starts[i - 1]) && starts.at(-1) < ep.seconds);
  if (ep.cues) ok("manifest cues (from voice.py) have one entry per paragraph", ep.cues.length === ep.paragraphs.length);
  if (ep.art.frames.length === ep.paragraphs.length) {
    const drift = Math.max(...ep.art.frames.map((f, i) => Math.abs(f.t - starts[i])));
    ok(`one frame per paragraph: each frame within 3s of its paragraph start (max drift ${drift.toFixed(1)}s)`, drift <= 3);
  }

  // --- Formula budget (warning until the pilots are re-cut): ~150 wpm at
  // +10% edge-tts measured on the pilots, so 180s needs ~450 words.
  if (totalWords < 430 || totalWords > 490) warn(`${totalWords} words: the 180s formula needs 430-490 at the measured ~150 wpm`);

  // --- Art variety (warning: needs new art, not a code fix) ---
  const hashes = ep.art.frames.map((f) => existsSync(join(ROOT, "web", f.src)) ? md5(read(f.src)) : f.src);
  const unique = new Set(hashes).size;
  if (unique < ep.art.frames.length) warn(`only ${unique} distinct images among ${ep.art.frames.length} story frames`);
}

// 2b. Manifest-wide checks
console.log("\n2b. Manifest-wide checks:");
ok("episode ids are unique", new Set(episodes.map((e) => e.id)).size === episodes.length);
ok("parseEpisodes returns newest first (hero shows the latest release)",
  episodes.every((e, i) => i === 0 || `${episodes[i - 1].date} ${episodes[i - 1].hour}` >= `${e.date} ${e.hour}`));

// 2c. Engine unit checks on synthetic input (edge cases)
console.log("\n2c. Timing & schema edge cases:");
const synth = validateEpisode({ id: "x", title: "t", subject: "s", seconds: 120,
  paragraphs: ["a b", "c d e f", "g h"], art: { frames: [{ t: 0, src: "a" }, { t: "abc", src: "b" }, { src: "c" }] } });
ok("word-weighted cue starts: [0, 30, 90] for 2/4/2 words over 120s",
  JSON.stringify(cueStarts(synth)) === JSON.stringify([0, 30, 90]));
ok("paragraphAt picks the paragraph that is playing", paragraphAt([0, 30, 90], 29.9) === 0 && paragraphAt([0, 30, 90], 30) === 1 && paragraphAt([0, 30, 90], 500) === 2);
ok("explicit cues win over the estimate", JSON.stringify(cueStarts({ ...synth, cues: [0, 10, 20] })) === "[0,10,20]");
ok("cues of the wrong length fall back to the estimate", cueStarts({ ...synth, cues: [0, 10] })[1] === 30);
ok("a non-numeric frame t falls back to an even spread instead of NaN", synth.art.frames[1].t === 40 && synth.art.frames[2].t === 80);
ok("frame t of 0 on a later frame is kept, not replaced", validateEpisode({ ...synth, art: { frames: [{ t: 0 }, { t: 0 }] } }).art.frames[1].t === 0);
ok("escapeHtml neutralises markup in titles", escapeHtml(`<img src=x onerror="a">&'`) === "&lt;img src=x onerror=&quot;a&quot;&gt;&amp;&#39;");
ok("validateEpisode rejects a missing id", validateEpisode({ title: "t", subject: "s", paragraphs: ["a", "b", "c"] }) === null);
ok("1376x768 and 1280x720 both pass the 16:9 rule", [[1376, 768], [1280, 720]].every(([w, h]) => Math.abs(w / h / ART_ASPECT - 1) <= ASPECT_TOLERANCE));
// Editorial rules on synthetic episodes
const NOW = Date.parse("2026-10-06T15:00:00Z");
const src = (para, extra = {}) => ({ para, url: "https://example.org/a", title: "t", published: "2026-10-06", ...extra });
const good = { id: "g", date: "2026-10-06", hour: "14:00", title: "t", subject: "s",
  paragraphs: ["a", "b", "c", "d", "e", "f"], sources: [0, 1, 2, 3, 4].map((p) => src(p)) };
ok("gate: a sourced, past-dated episode passes", editorialProblems(good, NOW).length === 0);
ok("gate: an episode stamped one hour ahead fails", editorialProblems({ ...good, hour: "16:00" }, NOW).some((x) => x.includes("future")));
ok("gate: an episode dated next week fails", editorialProblems({ ...good, date: "2026-10-12" }, NOW).some((x) => x.includes("future")));
ok("gate: a claim paragraph without a source fails", editorialProblems({ ...good, sources: good.sources.slice(1) }, NOW).includes("P0 has no source"));
ok("gate: the sign-off (P5) needs no source", !editorialProblems(good, NOW).some((x) => x.startsWith("P5")));
ok("gate: naming Shvets without a speaker source fails",
  editorialProblems({ ...good, paragraphs: ["As Yuri Shvets revealed, x", "b", "c", "d", "e", "f"] }, NOW).some((x) => x.includes("Shvets")));
ok("gate: naming Shvets WITH a speaker source passes",
  editorialProblems({ ...good, paragraphs: ["As Yuri Shvets said, x", "b", "c", "d", "e", "f"],
    sources: [...good.sources, src(0, { speaker: "Yuri Shvets" })] }, NOW).length === 0);
ok("gate: Shvets in the title needs a speaker source", editorialProblems({ ...good, title: "Yuri Shvets PAC Disclosures" }, NOW).some((x) => x.includes("title")));
ok("gate: a source dated after the episode fails", editorialProblems({ ...good, sources: [...good.sources, src(2, { published: "2026-10-09" })] }, NOW).some((x) => x.includes("after")));
ok("gate: a non-https source fails", editorialProblems({ ...good, sources: [...good.sources, src(1, { url: "javascript:alert(1)" })] }, NOW).some((x) => x.includes("https")));
{
  const unverified = join(ROOT, "data/held/episodes-unverified.json");
  ok("gate: every unverified held episode would be refused today",
    !existsSync(unverified) || JSON.parse(readFileSync(unverified, "utf8")).episodes.every((e) => editorialProblems(e, NOW).length > 0));
  const fabricated = join(ROOT, "data/held/episodes-fabricated-archive.json");
  ok("gate: every held 'archive' episode is refused by provenance",
    !existsSync(fabricated) || JSON.parse(readFileSync(fabricated, "utf8")).episodes.every((e) => {
      const sp = join(ROOT, "data/ingest", `${e.ingest}.json`);
      return provenanceProblems(e, existsSync(sp) ? JSON.parse(readFileSync(sp, "utf8")) : null, Date.now(), FEEDS).length > 0;
    }));
}
// Ingest: feed parsing and the hour window
const RSS = `<rss><channel><item><title>Strike on &amp; depot</title><link>https://ex.org/a</link>
  <pubDate>Tue, 06 Oct 2026 17:30:00 GMT</pubDate><description><![CDATA[<p>Body &amp; more</p>]]></description></item>
  <item><title>Old</title><link>https://ex.org/old</link><pubDate>Mon, 28 Sep 2026 10:00:00 GMT</pubDate></item>
  <item><title>Insecure</title><link>http://ex.org/h</link><pubDate>Tue, 06 Oct 2026 18:00:00 GMT</pubDate></item>
  <item><title>Later</title><link>https://ex.org/late</link><pubDate>Tue, 06 Oct 2026 19:10:00 GMT</pubDate></item></channel></rss>`;
const ATOM = `<feed xmlns:media="http://search.yahoo.com/mrss/"><entry><title>Briefing</title>
  <link rel="alternate" href="https://www.youtube.com/watch?v=abc"/><published>2026-10-06T16:00:00+00:00</published>
  <media:group><media:description>What he said</media:description></media:group></entry></feed>`;
const RDF = `<rdf:RDF><item rdf:about="https://arxiv.org/abs/1"><title>Paper</title><link>https://arxiv.org/abs/1</link>
  <dc:date>2026-10-05T00:00:00Z</dc:date></item></rdf:RDF>`;
const rss = parseFeed(RSS), atom = parseFeed(ATOM), rdf = parseFeed(RDF);
ok("parseFeed reads RSS 2.0 (entities, CDATA, dates)", rss.length === 4 && rss[0].title === "Strike on & depot" && rss[0].summary === "Body & more" && rss[0].published === "2026-10-06T17:30:00.000Z");
ok("parseFeed reads Atom / YouTube (link href, media:description)", atom[0]?.url === "https://www.youtube.com/watch?v=abc" && atom[0].summary === "What he said");
ok("parseFeed reads RSS 1.0 / RDF (dc:date)", rdf[0]?.url === "https://arxiv.org/abs/1" && rdf[0].published === "2026-10-05T00:00:00.000Z");
const H = Date.parse("2026-10-06T19:00:00Z");
const kept = inWindow(rss, H, 24).map((i) => i.url);
ok("inWindow keeps only https items from before the hour and within max age", JSON.stringify(kept) === JSON.stringify(["https://ex.org/a"]));
ok("hourId names the snapshot file by UTC hour", hourId(H) === "2026-10-06-19");
const realNow = Date.parse("2026-10-06T20:38:00Z");
const hdrs = ["Tue, 06 Oct 2026 20:38:00 GMT", "Tue, 06 Oct 2026 20:38:02 GMT", "garbage"];
ok("clock check: a PC 2 h fast is caught (the 2026-10-06 cause of future-dated episodes)",
  clockSkewMs(hdrs, realNow + 2 * 3600e3) > MAX_CLOCK_SKEW_MS);
ok("clock check: a PC within a few seconds passes", Math.abs(clockSkewMs(hdrs, realNow + 3000)) < MAX_CLOCK_SKEW_MS);
ok("clock check: no readable server time gives null (ingest then refuses)", clockSkewMs(["x"], realNow) === null);

// Provenance: cite only what was collected
const snap = { hour: "2026-10-06T19:00:00.000Z", captured_at: "2026-10-06T19:01:00.000Z",
  feeds: [{ id: "bbc-world", status: "ok", count: 2 }, { id: "shvets-youtube", status: "ok", count: 1 }], items: [
  { feed: "bbc-world", url: "https://ex.org/a", kind: "news" }, { feed: "bbc-world", url: "https://ex.org/b", kind: "news" },
  { feed: "shvets-youtube", url: "https://www.youtube.com/watch?v=abc", kind: "speaker", speaker: "Yuri Shvets" }] };
const pep = { ...good, hour: "19:00", ingest: "2026-10-06-19", sources: [
  src(0, { url: "https://ex.org/a" }), src(1, { url: "https://ex.org/b" }), src(2, { url: "https://arxiv.org/abs/1", kind: "reference" }),
  src(3, { url: "https://doi.org/x", kind: "reference" }), src(4, { url: "https://cia.gov/y", kind: "reference" })] };
const NOW2 = Date.parse("2026-10-06T19:30:00Z");
ok("provenance: news from the snapshot + references passes", provenanceProblems(pep, snap, NOW2).length === 0);
ok("provenance: an episode without a snapshot fails", provenanceProblems({ ...pep, ingest: undefined }, snap, NOW2).length === 1);
ok("provenance: a news URL that was never collected fails",
  provenanceProblems({ ...pep, sources: [src(0, { url: "https://made.up/story" }), ...pep.sources.slice(1)] }, snap, NOW2).some((x) => x.includes("not in the ingest")));
ok("provenance: a quote must come from the speaker's own collected feed",
  provenanceProblems({ ...pep, sources: [...pep.sources, src(0, { url: "https://ex.org/a", speaker: "Yuri Shvets" })] }, snap, NOW2).some((x) => x.includes("own feed")) &&
  provenanceProblems({ ...pep, sources: [...pep.sources, src(0, { url: "https://www.youtube.com/watch?v=abc", speaker: "Yuri Shvets" })] }, snap, NOW2).length === 0);
ok("provenance: an unmarked, uncollected science source fails",
  provenanceProblems({ ...pep, sources: [...pep.sources.slice(0, 2), src(2, { url: "https://x.org/p" })] }, snap, NOW2).some((x) => x.includes("reference")));
ok("provenance: a snapshot from after the episode hour fails", provenanceProblems({ ...pep, hour: "18:00" }, snap, NOW2).some((x) => x.includes("after the episode")));
ok("provenance: a malformed captured_at fails (the 2026-10-07 hand-made archive snapshots)",
  provenanceProblems(pep, { ...snap, captured_at: "2026-10-06T19:00:05:00.000Z" }, NOW2).some((x) => x.includes("not a valid time")));
ok("provenance: a snapshot written long after its hour fails (backfilled 'archive')",
  provenanceProblems(pep, { ...snap, captured_at: "2026-10-07T23:00:00.000Z" }, Date.parse("2026-10-08T00:00:00Z")).some((x) => x.includes("within")));
ok("provenance: item counts must match what the snapshot reports per feed",
  provenanceProblems(pep, { ...snap, feeds: [{ id: "bbc-world", status: "ok", count: 10 }, snap.feeds[1]] }, NOW2).some((x) => x.includes("holds 2")));
ok("provenance: an item from a feed the snapshot does not report fails",
  provenanceProblems(pep, { ...snap, feeds: [snap.feeds[1]] }, NOW2).some((x) => x.includes("does not report")));
ok("provenance: a speaker item must come from that speaker's configured feed",
  provenanceProblems(pep, snap, NOW2, FEEDS).length === 0 &&
  provenanceProblems(pep, { ...snap, items: snap.items.map((i) => i.speaker ? { ...i, feed: "bbc-world" } : i),
    feeds: [{ id: "bbc-world", status: "ok", count: 3 }] }, NOW2, FEEDS).some((x) => x.includes("speaker")));
ok("webpSize rejects a non-WebP buffer", webpSize(Buffer.from("RIFF0000WAVEfmt                 ")) === null);
ok("mp3Info rejects random bytes", mp3Info(Buffer.alloc(4096, 0x11)) === null);

// 3. Frontend structure
console.log("\n3. Validating Frontend Assets:");
ok("index.html exists", existsSync(join(ROOT, "web/index.html")));
ok("style.css exists", existsSync(join(ROOT, "web/style.css")));
ok("studio.css exists", existsSync(join(ROOT, "web/css/studio.css")));
ok("app.js exists", existsSync(join(ROOT, "web/js/app.js")));
ok("episodes.js exists", existsSync(join(ROOT, "web/js/episodes.js")));
ok("categories.js exists", existsSync(join(ROOT, "web/js/categories.js")));

console.log(`\nResults: ${passed} passed, ${failed} failed, ${warned} warnings`);
if (failed > 0) process.exit(1);
