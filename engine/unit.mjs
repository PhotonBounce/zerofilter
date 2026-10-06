// unit.mjs — Automated test suite for ZeroFilter release manifests and engine

import { readFileSync, existsSync } from "node:fs";
import { resolve, join } from "node:path";
import { createHash } from "node:crypto";
import { parseEpisodes, validateEpisode, cueStarts, paragraphAt, escapeHtml, MIN_DURATION, MAX_DURATION } from "../web/js/episodes.js";
import { webpSize, mp3Info, isMp4 } from "./media.mjs";
import { CATEGORIES } from "../web/js/categories.js";

const ROOT = resolve(import.meta.dirname, "..");
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
ok(`manifest contains valid episodes (found ${episodes.length})`, episodes.length >= 3);

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
