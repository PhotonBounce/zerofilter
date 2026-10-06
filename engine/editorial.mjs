// editorial.mjs — the publishing gate. An episode reaches the site only if
// it passes every rule here (unit.mjs and build_site.mjs both enforce it).
//
// Why it exists (owner, 2026-10-06): the pipeline had produced 151 episodes
// in one morning, stamped up to six days AHEAD of the real date, with news
// written from a topic list and nothing else, and every one putting claims in
// the mouth of a real person (Yuri Shvets) with no source for any of them.
// "Make sure we're not creating fake quotes or fake news ... we have to stop
// doing that." Those episodes are held in data/held/, not deleted.
//
// The rules:
//  1. Never dated in the future. An episode is stamped with the hour it is
//     published, never a slot ahead of the clock.
//  2. Every claim paragraph (P0-P4) cites at least one real, dated source:
//     sources: [{ para, url, title, published: "YYYY-MM-DD", speaker? }]
//     A source must be published on or before the episode's date.
//  3. A paragraph that names a real person as saying, reporting or showing
//     something needs a source with `speaker` set to that person: a link to
//     where THEY said it. No source, no quote.
//  P5 (sign-off / synthesis) is opinion and needs no source.

export const CLAIM_PARAGRAPHS = [0, 1, 2, 3, 4];

// Real people the show quotes. Add a name here before it can be attributed.
export const QUOTED_PEOPLE = Object.freeze({
  "Yuri Shvets": ["Shvets", "Швец"],
});

export function episodeTime(ep) {
  const hour = /^\d{2}:\d{2}$/.test(ep.hour || "") ? ep.hour : "00:00";
  const t = Date.parse(`${ep.date}T${hour}:00Z`);
  return Number.isFinite(t) ? t : NaN;
}

// Returns a list of human-readable problems; [] means publishable.
export function editorialProblems(ep, now = Date.now()) {
  const problems = [];
  const t = episodeTime(ep);
  if (!Number.isFinite(t)) problems.push(`no valid date/hour (${ep.date} ${ep.hour})`);
  else if (t > now) problems.push(`dated in the future (${ep.date} ${ep.hour} UTC)`);

  const sources = Array.isArray(ep.sources) ? ep.sources : [];
  for (const [i, s] of sources.entries()) {
    if (!s || !/^https:\/\/\S+$/.test(s.url || "")) problems.push(`source #${i} has no https url`);
    if (!s?.title) problems.push(`source #${i} has no title`);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s?.published || "")) problems.push(`source #${i} has no published date (YYYY-MM-DD)`);
    else if (ep.date && s.published > ep.date) problems.push(`source #${i} is dated after the episode (${s.published})`);
    if (!Number.isInteger(s?.para) || s.para < 0 || s.para >= (ep.paragraphs?.length || 0)) problems.push(`source #${i} points at no paragraph`);
  }

  for (const p of CLAIM_PARAGRAPHS) {
    if (p >= (ep.paragraphs?.length || 0)) continue;
    if (!sources.some((s) => s?.para === p)) problems.push(`P${p} has no source`);
  }

  (ep.paragraphs || []).forEach((text, p) => {
    for (const [person, names] of Object.entries(QUOTED_PEOPLE)) {
      if (!names.some((n) => text.includes(n))) continue;
      if (!sources.some((s) => s?.para === p && s.speaker === person)) {
        problems.push(`P${p} attributes claims to ${person} without a source where he said it`);
      }
    }
  });
  // The title and summary are claims too ("Yuri Shvets PAC Disclosures").
  const meta = `${ep.title || ""} ${ep.subject || ""}`;
  for (const [person, names] of Object.entries(QUOTED_PEOPLE)) {
    if (names.some((n) => meta.includes(n)) && !sources.some((s) => s?.speaker === person)) {
      problems.push(`title/summary names ${person} but no source quotes him`);
    }
  }
  return problems;
}

export function isPublishable(ep, now = Date.now()) {
  return editorialProblems(ep, now).length === 0;
}

// Provenance: what an episode cites must have been COLLECTED, not remembered.
// Every published episode names the ingest snapshot it was written from
// (ep.ingest = "YYYY-MM-DD-HH", file data/ingest/<that>.json, made by
// engine/ingest.mjs). News paragraphs (P0, P1) and every quote (a source with
// `speaker`) must cite a URL that is in that snapshot — for a quote, an item
// from that speaker's own feed. Other paragraphs may also cite stable
// references (a paper, an archive) marked kind: "reference".
export const NEWS_PARAGRAPHS = [0, 1];

export function provenanceProblems(ep, snapshot, now = Date.now()) {
  if (!ep.ingest) return ["no ingest snapshot named (ep.ingest)"];
  if (!snapshot) return [`ingest snapshot data/ingest/${ep.ingest}.json is missing`];
  const problems = [];
  const snapHour = Date.parse(snapshot.hour);
  if (!Number.isFinite(snapHour) || snapHour > episodeTime(ep)) problems.push(`snapshot hour ${snapshot.hour} is after the episode`);
  if (Date.parse(snapshot.captured_at) > now) problems.push("snapshot captured in the future");
  const byUrl = new Map((snapshot.items || []).map((it) => [it.url, it]));
  for (const [i, s] of (ep.sources || []).entries()) {
    const item = byUrl.get(s?.url);
    if (s?.speaker) {
      if (!item || item.speaker !== s.speaker) problems.push(`source #${i} quotes ${s.speaker} from a URL not collected from ${s.speaker}'s own feed`);
    } else if (NEWS_PARAGRAPHS.includes(s?.para)) {
      if (!item) problems.push(`source #${i} (news, P${s.para}) is not in the ingest snapshot`);
    } else if (!item && s?.kind !== "reference") {
      problems.push(`source #${i} is neither in the snapshot nor marked kind: "reference"`);
    }
  }
  return problems;
}
