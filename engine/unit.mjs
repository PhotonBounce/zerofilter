// unit.mjs — Automated test suite for ZeroFilter release manifests and engine

import { readFileSync, existsSync } from "node:fs";
import { resolve, join } from "node:path";
import { parseEpisodes, validateEpisode, MIN_DURATION, MAX_DURATION } from "../web/js/episodes.js";
import { CATEGORIES } from "../web/js/categories.js";

const ROOT = resolve(import.meta.dirname, "..");
let passed = 0, failed = 0;

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
}

// 3. Frontend structure
console.log("\n3. Validating Frontend Assets:");
ok("index.html exists", existsSync(join(ROOT, "web/index.html")));
ok("style.css exists", existsSync(join(ROOT, "web/style.css")));
ok("studio.css exists", existsSync(join(ROOT, "web/css/studio.css")));
ok("app.js exists", existsSync(join(ROOT, "web/js/app.js")));
ok("episodes.js exists", existsSync(join(ROOT, "web/js/episodes.js")));
ok("categories.js exists", existsSync(join(ROOT, "web/js/categories.js")));

console.log(`\nResults: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
