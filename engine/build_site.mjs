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
import { editorialProblems } from "./editorial.mjs";

const ROOT = resolve(import.meta.dirname, "..");
const WEB = join(ROOT, "web");
const DIST = join(ROOT, "dist");

const SHELL = [
  "index.html", "style.css", ".htaccess",
  "css/studio.css",
  "js/app.js", "js/episodes.js", "js/categories.js",
  "assets/rex_vance.webp", "assets/studio_bunker.webp", "assets/test_rex.mp3",
];

const manifest = JSON.parse(readFileSync(join(WEB, "data/episodes.json"), "utf8"));
const episodes = parseEpisodes(manifest);
let refused = 0;
for (const ep of episodes) {
  const problems = editorialProblems(ep);
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
mkdirSync(join(DIST, "data"), { recursive: true });
writeFileSync(join(DIST, "data/episodes.json"), JSON.stringify(manifest, null, 2));
console.log(`dist/ built: ${episodes.length} published episode(s), player shell of ${SHELL.length} files.`);
