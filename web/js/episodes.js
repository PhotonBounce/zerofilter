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
    t: Number(f.t) || i * (seconds / (ep.art.frames.length || 1)),
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

export function parseEpisodes(data) {
  const list = Array.isArray(data) ? data : (data?.episodes || []);
  return list.map(validateEpisode).filter(Boolean);
}

export function formatTime(seconds) {
  const s = Math.max(0, Math.floor(seconds || 0));
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return `${m}:${rem < 10 ? "0" : ""}${rem}`;
}
