// episodes.js — Episode schema validator and timing utilities for ZeroFilter

export const EPISODE_DURATION_TARGET = 180; // 3 minutes
export const MIN_DURATION = 150;
export const MAX_DURATION = 210;

export function validateEpisode(ep) {
  if (!ep || typeof ep !== "object") return null;
  if (!ep.id || typeof ep.id !== "string") return null;
  if (!ep.title || typeof ep.title !== "string") return null;
  if (!ep.subject || typeof ep.subject !== "string") return null;
  if (!Array.isArray(ep.paragraphs) || ep.paragraphs.length < 3) return null;

  const seconds = Number(ep.seconds) || EPISODE_DURATION_TARGET;
  const thumb = typeof ep.thumb === "string" ? ep.thumb : `thumbs/${ep.id}.webp`;
  const cover_video = typeof ep.cover_video === "string" ? ep.cover_video : `thumbs/${ep.id}.mp4`;
  const audio = typeof ep.audio === "string" ? ep.audio : `audio/${ep.id}.mp3`;

  const frames = Array.isArray(ep.art?.frames) ? ep.art.frames.map((f, i) => ({
    t: Number.isFinite(Number(f.t)) && f.t !== null && f.t !== "" ? Number(f.t) : i * (seconds / (ep.art.frames.length || 1)),
    src: f.src,
    caption: f.caption || ""
  })) : [];

  return {
    ...ep,
    seconds,
    thumb,
    cover_video,
    audio,
    art: { frames }
  };
}

// Newest first: the hero shows episodes[0], so the order must not depend on
// how the manifest happens to be written.
export function parseEpisodes(data) {
  const list = Array.isArray(data) ? data : (data?.episodes || []);
  return list.map(validateEpisode).filter(Boolean)
    .sort((a, b) => `${b.date || ""} ${b.hour || ""}`.localeCompare(`${a.date || ""} ${a.hour || ""}`));
}

// Start time (s) of each paragraph. Uses ep.cues when the voice engine wrote
// real timings; otherwise estimates by word count (paragraphs run 46-92 words,
// so an equal split drifts by 20+ seconds).
export function cueStarts(ep) {
  const n = ep.paragraphs.length;
  if (Array.isArray(ep.cues) && ep.cues.length === n && ep.cues.every(Number.isFinite)) return ep.cues.slice();
  const words = ep.paragraphs.map((p) => p.split(/\s+/).filter(Boolean).length);
  const total = words.reduce((a, b) => a + b, 0) || 1;
  const starts = [];
  let acc = 0;
  for (const w of words) { starts.push((acc / total) * ep.seconds); acc += w; }
  return starts;
}

export function paragraphAt(starts, t) {
  let idx = 0;
  for (let i = 0; i < starts.length; i++) if (t >= starts[i]) idx = i;
  return idx;
}

export function escapeHtml(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

export function formatTime(seconds) {
  const s = Math.max(0, Math.floor(seconds || 0));
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return `${m}:${rem < 10 ? "0" : ""}${rem}`;
}
