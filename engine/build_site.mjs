// build_site.mjs — assembles what the public sites serve, into dist/.
//
//   node engine/build_site.mjs            # writes dist/
//
// Only the player, its assets, and the media of episodes that pass the
// editorial gate are copied. Held episodes' audio and art stay in the repo
// but never reach photon-bounce.com or GitHub Pages. Fails (exit 1) if the
// feed contains an episode the gate refuses, so a deploy cannot ship it.

import { cpSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { parseEpisodes } from "../web/js/episodes.js";
import { editorialProblems, provenanceProblems } from "./editorial.mjs";

const ROOT = resolve(import.meta.dirname, "..");
const WEB = join(ROOT, "web");
const DIST = join(ROOT, "dist");

const SHELL = [
  "index.html", "style.css", ".htaccess",
  "css/studio.css",
  "js/app.js", "js/episodes.js", "js/categories.js", "js/ambient.js", "js/telemetry-canvas.js",
  "assets/ava_vance.webp", "assets/rex_vance.webp", "assets/studio_bunker.webp", "assets/test_rex.mp3",
];

const FEEDS = JSON.parse(readFileSync(join(ROOT, "data/feeds.json"), "utf8")).feeds;
const manifest = JSON.parse(readFileSync(join(WEB, "data/episodes.json"), "utf8"));
const episodes = parseEpisodes(manifest);
let refused = 0;
for (const ep of episodes) {
  const snapPath = ep.ingest ? join(ROOT, "data/ingest", `${ep.ingest}.json`) : null;
  const snapshot = snapPath && existsSync(snapPath) ? JSON.parse(readFileSync(snapPath, "utf8")) : null;
  const problems = [...editorialProblems(ep), ...provenanceProblems(ep, snapshot, Date.now(), FEEDS)];
  if (problems.length) {
    refused++;
    console.error(`REFUSED ${ep.id}: ${problems.join("; ")}`);
  }
}
if (refused) {
  console.error(`${refused} episode(s) in web/data/episodes.json fail the editorial gate; nothing built.`);
  process.exit(1);
}

rmSync(DIST, { recursive: true, force: true });
const copy = (rel) => {
  const from = join(WEB, rel);
  if (!existsSync(from)) throw new Error(`missing ${rel}`);
  mkdirSync(dirname(join(DIST, rel)), { recursive: true });
  cpSync(from, join(DIST, rel));
};
SHELL.forEach(copy);
for (const ep of episodes) {
  [ep.audio, ep.thumb, ep.cover_video, ...ep.art.frames.map((f) => f.src)].filter(Boolean).forEach(copy);
}
// Every module the shell imports must ship with it: a missing one 404s on
// the host and the whole player fails to start (2026-10-08: ambient.js and
// telemetry-canvas.js were imported by app.js but never copied).
for (const rel of SHELL.filter((f) => f.endsWith(".js"))) {
  const code = readFileSync(join(DIST, rel), "utf8");
  for (const [, spec] of code.matchAll(/(?:import|from)\s*\(?\s*["'](\.{1,2}\/[^"']+)["']/g)) {
    if (!existsSync(join(dirname(join(DIST, rel)), spec))) {
      console.error(`${rel} imports ${spec}, which is not in the build (add it to SHELL)`);
      process.exit(1);
    }
  }
}
// Same for the page's own images and scripts (assets/ava_vance.webp 404ed).
for (const [, ref] of readFileSync(join(DIST, "index.html"), "utf8").matchAll(/(?:src|href)="((?:assets|css|js)\/[^"]+)"|url\('((?:assets)\/[^']+)'\)/g).map((m) => [m[0], m[1] || m[2]])) {
  if (!existsSync(join(DIST, ref))) {
    console.error(`index.html references ${ref}, which is not in the build (add it to SHELL)`);
    process.exit(1);
  }
}
mkdirSync(join(DIST, "data"), { recursive: true });
writeFileSync(join(DIST, "data/episodes.json"), JSON.stringify(manifest, null, 2));
console.log(`dist/ built: ${episodes.length} published episode(s), player shell of ${SHELL.length} files.`);
