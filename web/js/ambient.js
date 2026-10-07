// web/js/ambient.js — ZeroFilter Procedural Cyber-Audio Engine & Ambient Bed

class CyberAudioEngine {
  constructor() {
    this.ctx = null;
    this.ambientGain = null;
    this.sfxGain = null;
    this.droneOsc1 = null;
    this.droneOsc2 = null;
    this.droneFilter = null;
    this.noiseNode = null;
    this.isPlaying = false;
    this.enabled = localStorage.getItem("zf_ambient_enabled") === "true";
    this.baseVolume = 0.18;
  }

  init() {
    if (this.ctx) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    this.ctx = new AudioCtx();

    // Master gains
    this.sfxGain = this.ctx.createGain();
    this.sfxGain.gain.value = 0.25;
    this.sfxGain.connect(this.ctx.destination);

    this.ambientGain = this.ctx.createGain();
    this.ambientGain.gain.value = this.enabled ? this.baseVolume : 0;
    this.ambientGain.connect(this.ctx.destination);

    this.createDroneNetwork();
  }

  ensureContext() {
    this.init();
    if (this.ctx && this.ctx.state === "suspended") {
      this.ctx.resume();
    }
  }

  createDroneNetwork() {
    if (!this.ctx) return;
    
    // Sub-bass root (43.65 Hz - F1)
    this.droneOsc1 = this.ctx.createOscillator();
    this.droneOsc1.type = "sawtooth";
    this.droneOsc1.frequency.value = 43.65;

    // Sub-bass fifth (65.41 Hz - C2)
    this.droneOsc2 = this.ctx.createOscillator();
    this.droneOsc2.type = "sine";
    this.droneOsc2.frequency.value = 65.41;

    // Warm Low-pass Resonant Ladder Filter
    this.droneFilter = this.ctx.createBiquadFilter();
    this.droneFilter.type = "lowpass";
    this.droneFilter.frequency.value = 160;
    this.droneFilter.Q.value = 4.0;

    // Subtle LFO modulating cutoff
    const lfo = this.ctx.createOscillator();
    lfo.type = "sine";
    lfo.frequency.value = 0.08; // Very slow evolving swell
    const lfoGain = this.ctx.createGain();
    lfoGain.gain.value = 40;
    lfo.connect(lfoGain);
    lfoGain.connect(this.droneFilter.frequency);
    lfo.start();

    // Noise bed (subtle telemetry warmth)
    const bufferSize = this.ctx.sampleRate * 2;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    whiteNoise.loop = true;

    const noiseFilter = this.ctx.createBiquadFilter();
    noiseFilter.type = "bandpass";
    noiseFilter.frequency.value = 800;
    noiseFilter.Q.value = 3.0;

    const noiseGain = this.ctx.createGain();
    noiseGain.gain.value = 0.015;

    whiteNoise.connect(noiseFilter);
    noiseFilter.connect(noiseGain);
    noiseGain.connect(this.ambientGain);
    whiteNoise.start();

    this.droneOsc1.connect(this.droneFilter);
    this.droneOsc2.connect(this.droneFilter);
    this.droneFilter.connect(this.ambientGain);

    this.droneOsc1.start();
    this.droneOsc2.start();

    // Start harmonic ambient chord progression
    this.startHarmonicChords();
  }

  startHarmonicChords() {
    if (!this.ctx) return;
    const chords = [
      [87.31, 130.81, 174.61, 261.63], // Fm9 (F2, C3, F3, C4)
      [69.30, 103.83, 138.59, 207.65], // Dbmaj7 (Db2, Ab2, Db3, Ab3)
      [58.27, 87.31, 116.54, 174.61],  // Bbm7 (Bb1, F2, Bb2, F3)
      [65.41, 98.00, 130.81, 196.00],  // Cm7 (C2, G2, C3, G3)
    ];
    let chordIdx = 0;

    const playChordStep = () => {
      if (!this.ctx || !this.ambientGain) return;
      const freqs = chords[chordIdx % chords.length];
      chordIdx++;
      const now = this.ctx.currentTime;
      const duration = 8.0;

      const chordGain = this.ctx.createGain();
      chordGain.gain.setValueAtTime(0.0001, now);
      chordGain.gain.linearRampToValueAtTime(0.06, now + 3.0);
      chordGain.gain.setValueAtTime(0.06, now + duration - 2.5);
      chordGain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

      const filter = this.ctx.createBiquadFilter();
      filter.type = "lowpass";
      filter.frequency.setValueAtTime(320, now);
      filter.frequency.linearRampToValueAtTime(450, now + 4.0);
      filter.frequency.linearRampToValueAtTime(280, now + duration);

      chordGain.connect(filter);
      filter.connect(this.ambientGain);

      freqs.forEach((f) => {
        const osc = this.ctx.createOscillator();
        osc.type = "sine";
        osc.frequency.setValueAtTime(f, now);
        osc.connect(chordGain);
        osc.start(now);
        osc.stop(now + duration + 0.1);
      });

      if (this.ctx.state !== "closed") {
        setTimeout(playChordStep, (duration - 1.5) * 1000);
      }
    };

    playChordStep();
  }

  toggleAmbient(enable) {
    this.ensureContext();
    this.enabled = typeof enable === "boolean" ? enable : !this.enabled;
    localStorage.setItem("zf_ambient_enabled", this.enabled);
    if (!this.ambientGain) return this.enabled;
    
    const target = this.enabled ? this.baseVolume : 0;
    this.ambientGain.gain.setTargetAtTime(target, this.ctx.currentTime, 0.5);
    return this.enabled;
  }

  duck(isSpeaking) {
    if (!this.ctx || !this.ambientGain || !this.enabled) return;
    const target = isSpeaking ? this.baseVolume * 0.35 : this.baseVolume;
    this.ambientGain.gain.setTargetAtTime(target, this.ctx.currentTime, 0.4);
  }

  // Futuristic interface sound effects
  playClick() {
    this.ensureContext();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "triangle";
    osc.frequency.setValueAtTime(1400, now);
    osc.frequency.exponentialRampToValueAtTime(300, now + 0.04);
    gain.gain.setValueAtTime(0.12, now);
    gain.gain.linearRampToValueAtTime(0, now + 0.04);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.04);
  }

  playRadarPing() {
    this.ensureContext();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(1860, now);
    osc.frequency.exponentialRampToValueAtTime(1840, now + 0.4);
    gain.gain.setValueAtTime(0.15, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.45);
  }

  playFrequencyTune() {
    this.ensureContext();
    if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = "sawtooth";
    osc.frequency.setValueAtTime(400, now);
    osc.frequency.exponentialRampToValueAtTime(920, now + 0.09);
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.linearRampToValueAtTime(0, now + 0.09);
    osc.connect(gain);
    gain.connect(this.sfxGain);
    osc.start(now);
    osc.stop(now + 0.09);
  }
}

export const cyberAudio = new CyberAudioEngine();
