// ingest.mjs — collects the real items an hour's episode may be written from.
//
//   node engine/ingest.mjs                       # the current UTC hour
//   node engine/ingest.mjs --hour 2026-10-06T19  # a specific hour (past or now only)
//
// Writes data/ingest/<YYYY-MM-DD-HH>.json:
//   { hour, captured_at, feeds: [{ id, status, count, error? }],
//     items: [{ feed, kind, speaker?, url, title, published, summary }] }
//
// Only items published BEFORE the hour starts, and no older than the feed's
// max_age_hours, are kept. The writer may cite nothing else for news and
// quotes: engine/editorial.mjs (provenanceProblems) checks every news and
// speaker source of an episode against its snapshot. Zero dependencies.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const ROOT = resolve(import.meta.dirname, "..");

const decode = (s) => s
  .replace(/<!\[CDATA\[([\s\S]*?)\]\]>/g, "$1")
  .replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
  .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(+n))
  .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
  .replace(/&amp;/g, "&");
const strip = (s) => decode(s).replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
const tag = (block, name) => {
  const m = block.match(new RegExp(`<${name}(?:\\s[^>]*)?>([\\s\\S]*?)</${name}>`, "i"));
  return m ? m[1] : "";
};

// RSS 2.0 <item>, RSS 1.0/RDF <item>, Atom <entry> (YouTube included).
export function parseFeed(xml) {
  const items = [];
  const blocks = xml.match(/<(item|entry)(?:\s[^>]*)?>[\s\S]*?<\/\1>/gi) || [];
  for (const b of blocks) {
    let url = strip(tag(b, "link"));
    if (!url) {
      const alt = b.match(/<link[^>]*rel=["']alternate["'][^>]*href=["']([^"']+)["']/i) || b.match(/<link[^>]*href=["']([^"']+)["']/i);
      url = alt ? decode(alt[1]) : "";
    }
    if (!url) url = strip(tag(b, "guid"));
    const when = strip(tag(b, "pubDate") || tag(b, "published") || tag(b, "dc:date") || tag(b, "updated"));
    const t = Date.parse(when);
    items.push({
      url: url.trim(),
      title: strip(tag(b, "title")),
      published: Number.isFinite(t) ? new Date(t).toISOString() : null,
      summary: strip(tag(b, "description") || tag(b, "summary") || tag(b, "media:description") || tag(b, "content")).slice(0, 600),
    });
  }
  return items;
}

// Keeps https items published in [hourStart - maxAge, hourStart).
export function inWindow(items, hourStart, maxAgeHours) {
  const from = hourStart - maxAgeHours * 3600e3;
  return items.filter((it) => /^https:\/\//.test(it.url) && it.published &&
    Date.parse(it.published) < hourStart && Date.parse(it.published) >= from);
}

export function hourId(t) {
  return new Date(t).toISOString().slice(0, 13).replace("T", "-");
}

async function fetchText(url) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 20000);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { "user-agent": "ZeroFilter-ingest/1.0 (+https://photon-bounce.com/zerofilter/)" } });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

async function main() {
  const arg = process.argv.indexOf("--hour");
  const now = Date.now();
  const hourStart = arg > 0
    ? Date.parse(`${process.argv[arg + 1]}:00:00Z`)
    : Math.floor(now / 3600e3) * 3600e3;
  if (!Number.isFinite(hourStart)) throw new Error("--hour must look like 2026-10-06T19");
  if (hourStart > now) throw new Error("refusing to ingest for an hour that has not started");

  const { feeds } = JSON.parse(readFileSync(join(ROOT, "data/feeds.json"), "utf8"));
  const report = [];
  const items = [];
  for (const f of feeds) {
    if (f.enabled === false) { report.push({ id: f.id, status: "disabled" }); continue; }
    try {
      const kept = inWindow(parseFeed(await fetchText(f.url)), hourStart, f.max_age_hours || 24);
      for (const it of kept) items.push({ feed: f.id, kind: f.kind, ...(f.speaker ? { speaker: f.speaker } : {}), ...it });
      report.push({ id: f.id, status: "ok", count: kept.length });
    } catch (err) {
      report.push({ id: f.id, status: "error", error: String(err?.message || err).slice(0, 200) });
    }
  }
  const snapshot = { hour: new Date(hourStart).toISOString(), captured_at: new Date().toISOString(), feeds: report, items };
  mkdirSync(join(ROOT, "data/ingest"), { recursive: true });
  const out = join(ROOT, "data/ingest", `${hourId(hourStart)}.json`);
  writeFileSync(out, JSON.stringify(snapshot, null, 2));
  for (const r of report) console.log(`${r.status.padEnd(8)} ${r.id}${r.count !== undefined ? ` (${r.count})` : ""}${r.error ? `: ${r.error}` : ""}`);
  console.log(`${items.length} items -> ${out}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((err) => { console.error(err.message); process.exit(1); });
}
