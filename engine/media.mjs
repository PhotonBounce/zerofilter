// media.mjs — zero-dependency readers for the media the manifest points at.
// Used by unit.mjs so a release cannot ship with art of the wrong size or a
// manifest duration that disagrees with the audio file.

// WebP: RIFF....WEBP then a VP8 / VP8L / VP8X chunk. Returns {width, height} or null.
export function webpSize(buf) {
  if (buf.length < 30 || buf.toString("ascii", 0, 4) !== "RIFF" || buf.toString("ascii", 8, 12) !== "WEBP") return null;
  const chunk = buf.toString("ascii", 12, 16);
  if (chunk === "VP8 ") {
    if (buf[23] !== 0x9d || buf[24] !== 0x01 || buf[25] !== 0x2a) return null;
    return { width: buf.readUInt16LE(26) & 0x3fff, height: buf.readUInt16LE(28) & 0x3fff };
  }
  if (chunk === "VP8L") {
    if (buf[20] !== 0x2f) return null;
    const b = buf.readUInt32LE(21);
    return { width: (b & 0x3fff) + 1, height: ((b >> 14) & 0x3fff) + 1 };
  }
  if (chunk === "VP8X") {
    return { width: buf.readUIntLE(24, 3) + 1, height: buf.readUIntLE(27, 3) + 1 };
  }
  return null;
}

const MP3_BITRATES = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]; // MPEG-1 Layer III
const MP3_BITRATES_V2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]; // MPEG-2/2.5 Layer III
const MP3_RATES = { 3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000] };

// MP3: walks every frame header and sums frame durations, so it is exact for
// CBR and VBR alike. Returns {seconds, frames, bitrateKbps, sampleRate} or null.
export function mp3Info(buf) {
  let i = 0;
  if (buf.toString("ascii", 0, 3) === "ID3") {
    const size = (buf[6] << 21) | (buf[7] << 14) | (buf[8] << 7) | buf[9];
    i = 10 + size;
  }
  let seconds = 0, frames = 0, first = null;
  while (i + 4 <= buf.length) {
    if (buf[i] !== 0xff || (buf[i + 1] & 0xe0) !== 0xe0) { i++; continue; }
    const ver = (buf[i + 1] >> 3) & 3, layer = (buf[i + 1] >> 1) & 3;
    const brIdx = buf[i + 2] >> 4, srIdx = (buf[i + 2] >> 2) & 3, pad = (buf[i + 2] >> 1) & 1;
    if (ver === 1 || layer !== 1 || brIdx === 0 || brIdx === 15 || srIdx === 3) { i++; continue; }
    const kbps = (ver === 3 ? MP3_BITRATES : MP3_BITRATES_V2)[brIdx];
    const rate = MP3_RATES[ver][srIdx];
    const samples = ver === 3 ? 1152 : 576;
    const len = Math.floor((samples / 8) * kbps * 1000 / rate) + pad;
    if (len < 4) { i++; continue; }
    if (!first) first = { bitrateKbps: kbps, sampleRate: rate };
    seconds += samples / rate;
    frames++;
    i += len;
  }
  return frames ? { seconds, frames, ...first } : null;
}

// MP4: true when the file starts with an ftyp box (cheap integrity check).
export function isMp4(buf) {
  return buf.length > 12 && buf.toString("ascii", 4, 8) === "ftyp";
}
