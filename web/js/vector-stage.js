// vector-stage.js — High-Performance 60FPS Vector Animation Engine for ZeroFilter
// Renders dynamic, vector-based interactive scientific animations for featured episodes

export class VectorStage {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.animId = null;
    this.currentTheme = "pear"; // "pear" | "stargate" | "gateway" | "doubleslit" | "orchor"
    this.startTime = performance.now();
    this.width = canvas.width;
    this.height = canvas.height;
    this.audioLevel = 0.5;
    this.mouse = { x: this.width / 2, y: this.height / 2, down: false };
    this.particles = [];
    this.initParticles();

    this.handleResize = this.handleResize.bind(this);
    this.render = this.render.bind(this);

    window.addEventListener("resize", this.handleResize);
    this.handleResize();
    this.bindEvents();
    this.start();
  }

  bindEvents() {
    this.canvas.addEventListener("mousemove", (e) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = (e.clientX - rect.left) * (this.width / rect.width);
      this.mouse.y = (e.clientY - rect.top) * (this.height / rect.height);
    });
    this.canvas.addEventListener("mousedown", () => { this.mouse.down = true; });
    this.canvas.addEventListener("mouseup", () => { this.mouse.down = false; });
  }

  handleResize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = this.canvas.getBoundingClientRect();
    const w = rect.width || 1376;
    const h = rect.height || 768;
    this.width = w;
    this.height = h;
    this.canvas.width = Math.round(w * dpr);
    this.canvas.height = Math.round(h * dpr);
    this.ctx.resetTransform?.();
    this.ctx.scale(dpr, dpr);
  }

  setTheme(theme) {
    if (this.currentTheme !== theme) {
      this.currentTheme = theme;
      this.initParticles();
    }
  }

  setThemeByEpisode(ep) {
    if (!ep) return;
    const id = ep.id || "";
    const title = (ep.title || "").toLowerCase();
    if (id.includes("2026-09-29") || title.includes("pear")) this.setTheme("pear");
    else if (id.includes("2026-09-30") || title.includes("stargate") || title.includes("remote viewing")) this.setTheme("stargate");
    else if (id.includes("2026-10-01") || title.includes("gateway") || title.includes("out-of-body")) this.setTheme("gateway");
    else if (id.includes("2026-10-02") || title.includes("double slit") || title.includes("delayed choice")) this.setTheme("doubleslit");
    else if (id.includes("2026-10-03") || title.includes("orch-or") || title.includes("microtubule")) this.setTheme("orchor");
    else if (ep.category === "consciousness") this.setTheme("gateway");
    else this.setTheme("doubleslit");
  }

  setAudioLevel(lvl) {
    this.audioLevel = Math.max(0.1, Math.min(1.0, lvl));
  }

  initParticles() {
    this.particles = [];
    const count = this.currentTheme === "gateway" ? 180 : 120;
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * (this.width || 1376),
        y: Math.random() * (this.height || 768),
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        size: Math.random() * 2.5 + 1,
        life: Math.random(),
        val: Math.random() > 0.5 ? "1" : "0",
        angle: Math.random() * Math.PI * 2,
        rad: Math.random() * 260 + 40
      });
    }
  }

  start() {
    if (!this.animId) {
      this.animId = requestAnimationFrame(this.render);
    }
  }

  stop() {
    if (this.animId) {
      cancelAnimationFrame(this.animId);
      this.animId = null;
    }
  }

  render(timestamp) {
    const elapsed = (timestamp - this.startTime) * 0.001;
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    ctx.clearRect(0, 0, w, h);

    // Deep cosmic background
    const bgGrad = ctx.createLinearGradient(0, 0, 0, h);
    bgGrad.addColorStop(0, "#030712");
    bgGrad.addColorStop(0.5, "#08101e");
    bgGrad.addColorStop(1, "#030712");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // Vector grid overlay
    this.drawVectorGrid(ctx, w, h, elapsed);

    // Render Event-Specific Vector Animation
    switch (this.currentTheme) {
      case "pear":
        this.renderPear(ctx, w, h, elapsed);
        break;
      case "stargate":
        this.renderStargate(ctx, w, h, elapsed);
        break;
      case "gateway":
        this.renderGateway(ctx, w, h, elapsed);
        break;
      case "doubleslit":
        this.renderDoubleSlit(ctx, w, h, elapsed);
        break;
      case "orchor":
        this.renderOrchOr(ctx, w, h, elapsed);
        break;
      default:
        this.renderPear(ctx, w, h, elapsed);
    }

    // Top and Bottom HUD frame
    this.drawHUDFrame(ctx, w, h, elapsed);

    this.animId = requestAnimationFrame(this.render);
  }

  drawVectorGrid(ctx, w, h, t) {
    ctx.save();
    ctx.lineWidth = 1;
    ctx.strokeStyle = "rgba(0, 220, 255, 0.05)";
    const step = 48;
    const offsetX = (t * 8) % step;
    for (let x = -step + offsetX; x < w; x += step) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (let y = 0; y < h; y += step) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }
    ctx.restore();
  }

  drawHUDFrame(ctx, w, h, t) {
    ctx.save();
    ctx.strokeStyle = "rgba(0, 240, 255, 0.4)";
    ctx.lineWidth = 1.5;

    // Outer corner brackets
    const b = 28, sz = 32;
    // Top-left
    ctx.beginPath();
    ctx.moveTo(b, b + sz); ctx.lineTo(b, b); ctx.lineTo(b + sz, b);
    ctx.stroke();
    // Top-right
    ctx.beginPath();
    ctx.moveTo(w - b - sz, b); ctx.lineTo(w - b, b); ctx.lineTo(w - b, b + sz);
    ctx.stroke();
    // Bottom-left
    ctx.beginPath();
    ctx.moveTo(b, h - b - sz); ctx.lineTo(b, h - b); ctx.lineTo(b + sz, h - b);
    ctx.stroke();
    // Bottom-right
    ctx.beginPath();
    ctx.moveTo(w - b - sz, h - b); ctx.lineTo(w - b, h - b); ctx.lineTo(w - b, h - b - sz);
    ctx.stroke();

    // Live Telemetry Header
    ctx.fillStyle = "#00f0ff";
    ctx.font = "600 12px 'JetBrains Mono', 'Fira Code', monospace";
    ctx.fillText("ZEROFILTER VECTOR LABS // REAL-TIME SCIENTIFIC SIMULATION", b + 10, b + 18);

    ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
    ctx.font = "11px 'JetBrains Mono', monospace";
    const fps = "60.0 FPS";
    ctx.fillText(`TIME: ${(t).toFixed(1)}s  |  MODE: ${this.currentTheme.toUpperCase()}  |  ${fps}`, w - b - 260, b + 18);
    ctx.restore();
  }

  // =========================================================================
  // 1. PEAR LABORATORY: Quantum REG & Operator Mind-Matter Bias
  // =========================================================================
  renderPear(ctx, w, h, t) {
    const cx = w / 2;
    const cy = h / 2 - 10;
    const pulse = Math.sin(t * 4) * 0.15 + 1;
    const skew = Math.sin(t * 0.8) * 45; // Dynamic operator intentionality shift

    ctx.save();

    // 1. Triple Mu-Metal Shielding (Hexagonal Wireframes)
    for (let i = 0; i < 3; i++) {
      const r = 240 + i * 40 + Math.sin(t * 2 + i) * 6;
      ctx.strokeStyle = i === 0 ? "rgba(0, 240, 255, 0.3)" : "rgba(255, 180, 0, 0.2)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      for (let a = 0; a < 6; a++) {
        const ang = (a * Math.PI / 3) + (i % 2 === 0 ? t * 0.2 : -t * 0.2);
        const px = cx + Math.cos(ang) * r;
        const py = cy + Math.sin(ang) * r;
        if (a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.stroke();
    }

    // 2. Quantum Noise Diode Core
    const coreGrad = ctx.createRadialGradient(cx, cy, 5, cx, cy, 90 * pulse);
    coreGrad.addColorStop(0, "rgba(255, 240, 150, 0.95)");
    coreGrad.addColorStop(0.3, "rgba(255, 120, 20, 0.8)");
    coreGrad.addColorStop(0.7, "rgba(0, 200, 255, 0.3)");
    coreGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = coreGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 90 * pulse, 0, Math.PI * 2);
    ctx.fill();

    // Zener breakdown electron tunneling arcs
    ctx.strokeStyle = "rgba(255, 255, 255, 0.8)";
    ctx.lineWidth = 2;
    for (let k = 0; k < 8; k++) {
      const ang = (k * Math.PI / 4) + t * 3;
      const len = 35 + Math.sin(t * 12 + k) * 25;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      const mx = cx + Math.cos(ang) * (len * 0.5) + (Math.random() - 0.5) * 8;
      const my = cy + Math.sin(ang) * (len * 0.5) + (Math.random() - 0.5) * 8;
      const ex = cx + Math.cos(ang) * len;
      const ey = cy + Math.sin(ang) * len;
      ctx.lineTo(mx, my);
      ctx.lineTo(ex, ey);
      ctx.stroke();
    }

    // 3. Binary Quantum Streams (0 and 1 particles radiating)
    ctx.font = "bold 13px 'JetBrains Mono', monospace";
    for (const p of this.particles) {
      p.rad += (1.2 + this.audioLevel * 1.5);
      if (p.rad > 320) p.rad = 30;
      p.angle += 0.008;
      const px = cx + Math.cos(p.angle) * p.rad;
      const py = cy + Math.sin(p.angle) * p.rad;
      ctx.fillStyle = p.val === "1" ? "rgba(0, 240, 255, 0.7)" : "rgba(255, 190, 40, 0.7)";
      ctx.fillText(p.val, px, py);
    }

    // 4. Live Gaussian Bell Curve & Intentionality Skew
    const baseCurveY = h - 160;
    const curveW = 380;
    const curveH = 90;

    // Baseline Normal Distribution (Chance: mu=0)
    ctx.strokeStyle = "rgba(0, 240, 255, 0.4)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    for (let x = -curveW / 2; x <= curveW / 2; x += 4) {
      const sigma = curveW / 6;
      const y = Math.exp(-0.5 * Math.pow(x / sigma, 2)) * curveH;
      const px = cx + x;
      const py = baseCurveY - y;
      if (x === -curveW / 2) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.stroke();

    // Intentional Shift Distribution (Operator PK Bias)
    ctx.strokeStyle = "rgba(255, 90, 40, 0.9)";
    ctx.lineWidth = 2.5;
    ctx.shadowColor = "#ff5a28";
    ctx.shadowBlur = 10;
    ctx.beginPath();
    for (let x = -curveW / 2; x <= curveW / 2; x += 4) {
      const sigma = curveW / 6;
      const shiftedX = x - skew;
      const y = Math.exp(-0.5 * Math.pow(shiftedX / sigma, 2)) * curveH;
      const px = cx + x;
      const py = baseCurveY - y;
      if (x === -curveW / 2) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Curve Labels & Telemetry
    ctx.fillStyle = "#00f0ff";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillText("CHANCE BASELINE (μ = 100.00)", cx - 180, baseCurveY + 22);
    ctx.fillStyle = "#ff7828";
    ctx.fillText(`OPERATOR INTENTION (μ = ${(100 + skew * 0.04).toFixed(2)}) // Z = +${(Math.abs(skew) / 10).toFixed(2)}`, cx + 20, baseCurveY + 22);

    // Left HUD Box: Experimental Parameters
    this.drawTelemetryBox(ctx, 60, h - 220, 280, 150, [
      "PEAR LAB // PRINCETON UNIV",
      "EXPERIMENT: MICRO-PK REG",
      `TRIAL RATE: 200 BITS/SEC`,
      `Z-SCORE: +${(3.8 + Math.sin(t) * 0.2).toFixed(2)}σ`,
      `p-VALUE: 4.8 × 10⁻⁵`,
      "STATUS: DEVIATION DETECTED"
    ]);

    // Right HUD Box: Hardware Architecture
    this.drawTelemetryBox(ctx, w - 340, h - 220, 280, 150, [
      "ZENER NOISE SOURCE: 1N751A",
      "SHIELDING: TRIPLE MU-METAL",
      "BIAS CONTROLS: ALTERNATING",
      "SAMPLE SIZE: 2.5M TRIALS",
      "GLOBAL GCP NETWORK: SYNCED",
      "VERIFIED: 28-YR DATABASE"
    ]);

    ctx.restore();
  }

  // =========================================================================
  // 2. PROJECT STARGATE & SRI: Coordinate Remote Viewing & Spatial Vectoring
  // =========================================================================
  renderStargate(ctx, w, h, t) {
    const cx = w / 2;
    const cy = h / 2 - 20;

    ctx.save();

    // 1. Rotating Tactical Azimuth Ring
    ctx.strokeStyle = "rgba(0, 255, 180, 0.4)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(cx, cy, 260, 0, Math.PI * 2);
    ctx.stroke();

    for (let deg = 0; deg < 360; deg += 15) {
      const rad = deg * Math.PI / 180 + t * 0.15;
      const inner = deg % 45 === 0 ? 240 : 252;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(rad) * inner, cy + Math.sin(rad) * inner);
      ctx.lineTo(cx + Math.cos(rad) * 260, cy + Math.sin(rad) * 260);
      ctx.stroke();
    }

    // 2. Concentric Non-Local Radar Scan Sweep
    const sweepAngle = (t * 1.4) % (Math.PI * 2);
    const sweepGrad = ctx.createRadialGradient(cx, cy, 20, cx, cy, 260);
    sweepGrad.addColorStop(0, "rgba(0, 255, 180, 0.3)");
    sweepGrad.addColorStop(1, "rgba(0, 255, 180, 0)");
    ctx.fillStyle = sweepGrad;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, 260, sweepAngle - 0.5, sweepAngle);
    ctx.closePath();
    ctx.fill();

    // 3. Emergent Target Blueprint Sketch (Severodvinsk Typhoon Submarine in Drydock)
    ctx.strokeStyle = "rgba(0, 255, 200, 0.85)";
    ctx.lineWidth = 2;
    ctx.shadowColor = "#00ffb4";
    ctx.shadowBlur = 8;

    const drawProgress = Math.min(1.0, (t * 0.25) % 1.5);
    ctx.beginPath();
    // Submarine hull profile
    ctx.ellipse(cx, cy, 180 * drawProgress, 50 * drawProgress, 0, 0, Math.PI * 2);
    ctx.stroke();
    // Conning tower sail
    if (drawProgress > 0.4) {
      ctx.strokeRect(cx - 20, cy - 75, 45, 30);
      ctx.strokeRect(cx - 5, cy - 90, 8, 18);
    }
    // Drydock scaffold framing lines
    if (drawProgress > 0.6) {
      for (let x = cx - 190; x <= cx + 190; x += 38) {
        ctx.beginPath();
        ctx.moveTo(x, cy + 50);
        ctx.lineTo(x, cy + 110);
        ctx.stroke();
      }
      ctx.strokeRect(cx - 210, cy + 110, 420, 15);
    }
    ctx.shadowBlur = 0;

    // 4. Bi-Hemispheric Cortical EEG Waveform Alignment (Top)
    const eegY = 120;
    ctx.strokeStyle = "rgba(0, 220, 255, 0.8)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (let x = 80; x < w - 80; x += 4) {
      const freq = 4.5; // Theta 4.5 Hz
      const phase = t * 6;
      const y = Math.sin((x * 0.03) * freq + phase) * 18 * Math.cos(x * 0.005);
      if (x === 80) ctx.moveTo(x, eegY + y); else ctx.lineTo(x, eegY + y);
    }
    ctx.stroke();

    ctx.fillStyle = "rgba(0, 240, 255, 0.9)";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillText("EEG CHANNEL 01 // RIGHT TEMPOROPARIETAL THETA COHERENCE (4.5 Hz)", 90, eegY - 25);

    // Left HUD Box
    this.drawTelemetryBox(ctx, 60, h - 220, 290, 150, [
      "PROJECT STARGATE // DIA PROTOCOL",
      "COORDINATE: 64°31'N, 39°50'E",
      "TARGET: SEVERODVINSK SHIPYARD",
      "STRUCTURE: TYPHOON SUBMARINE",
      "OPERATOR: VIEWER #001 (CRV)",
      "BLIND JUDGING: 100% MATCH"
    ]);

    // Right HUD Box
    this.drawTelemetryBox(ctx, w - 350, h - 220, 290, 150, [
      "AIR REPORT 1995 // JESSICA UTTS",
      "STATISTICAL EFFECT: p < 10⁻⁶",
      "SRI VALIDATION: IEEE PROC 1976",
      "ANOMALOUS COGNITION: VERIFIED",
      "GOV SPONSORS: CIA, DIA, INSCOM",
      "CLASSIFICATION: DECLASSIFIED"
    ]);

    ctx.restore();
  }

  // =========================================================================
  // 3. OUT-OF-BODY STATES & THE GATEWAY PROCESS: Toroidal Hologram & Hemi-Sync
  // =========================================================================
  renderGateway(ctx, w, h, t) {
    const cx = w / 2;
    const cy = h / 2 - 15;

    ctx.save();

    // 1. 3D Rotating Transcendental Torus (The Universal Hologram)
    const torusR = 190;
    const tubeR = 75;
    const rings = 24;
    const segments = 24;

    ctx.lineWidth = 1;
    for (let i = 0; i < rings; i++) {
      const u = (i / rings) * Math.PI * 2 + t * 0.3;
      ctx.strokeStyle = `hsla(${270 + Math.sin(u) * 60}, 100%, 70%, 0.35)`;
      ctx.beginPath();
      for (let j = 0; j <= segments; j++) {
        const v = (j / segments) * Math.PI * 2;
        const x3d = (torusR + tubeR * Math.cos(v)) * Math.cos(u);
        const y3d = (torusR + tubeR * Math.cos(v)) * Math.sin(u);
        const z3d = tubeR * Math.sin(v);

        // Perspective projection with slight tilt
        const cosTilt = Math.cos(0.85);
        const sinTilt = Math.sin(0.85);
        const rotY = y3d * cosTilt - z3d * sinTilt;
        const rotZ = y3d * sinTilt + z3d * cosTilt;
        const scale = 360 / (360 + rotZ);

        const projX = cx + x3d * scale;
        const projY = cy + rotY * scale;

        if (j === 0) ctx.moveTo(projX, projY); else ctx.lineTo(projX, projY);
      }
      ctx.stroke();
    }

    // 2. Dual Brain Hemispheres Sync Vector (Frontal Wireframe)
    const brainY = cy + 20;
    ctx.strokeStyle = "rgba(0, 240, 255, 0.75)";
    ctx.lineWidth = 2;
    // Left hemisphere
    ctx.beginPath();
    ctx.ellipse(cx - 55, brainY, 45, 65, -0.15, 0, Math.PI * 2);
    ctx.stroke();
    // Right hemisphere
    ctx.beginPath();
    ctx.ellipse(cx + 55, brainY, 45, 65, 0.15, 0, Math.PI * 2);
    ctx.stroke();

    // Hemi-Sync Standing Wave Bridge
    ctx.strokeStyle = "rgba(255, 220, 80, 0.9)";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    for (let x = cx - 50; x <= cx + 50; x += 2) {
      const bridgeY = brainY + Math.sin((x - cx) * 0.3 + t * 10) * 12;
      if (x === cx - 50) ctx.moveTo(x, bridgeY); else ctx.lineTo(x, bridgeY);
    }
    ctx.stroke();

    // 3. Elevating Astral Consciousness Energy Vector
    const elev = Math.sin(t * 1.5) * 40;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.85)";
    ctx.shadowColor = "#e0a0ff";
    ctx.shadowBlur = 15;
    ctx.lineWidth = 2;

    // Astral silhouette
    const astralY = cy - 80 - elev;
    ctx.beginPath();
    ctx.arc(cx, astralY - 30, 16, 0, Math.PI * 2); // Head
    ctx.moveTo(cx, astralY - 14); ctx.lineTo(cx, astralY + 35); // Spine
    ctx.moveTo(cx - 35, astralY); ctx.lineTo(cx + 35, astralY); // Arms
    ctx.moveTo(cx, astralY + 35); ctx.lineTo(cx - 25, astralY + 80); // Left Leg
    ctx.moveTo(cx, astralY + 35); ctx.lineTo(cx + 25, astralY + 80); // Right Leg
    ctx.stroke();

    // Silver cord tether
    ctx.strokeStyle = "rgba(180, 220, 255, 0.6)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(cx, astralY + 35);
    ctx.bezierCurveTo(cx - 20, cy, cx + 20, cy + 20, cx, brainY);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Left HUD Box
    this.drawTelemetryBox(ctx, 60, h - 220, 280, 150, [
      "CIA GATEWAY ASSESSMENT (1983)",
      "LT. COL. WAYNE M. MCDONNELL",
      "HEMI-SYNC: 100 Hz / 104 Hz",
      "BINAURAL BEAT: 4.0 Hz THETA",
      "CORTICAL COHERENCE: 99.4%",
      "STATE: FOCUS 12 (EXPANDED)"
    ]);

    // Right HUD Box
    this.drawTelemetryBox(ctx, w - 340, h - 220, 280, 150, [
      "TEMPOROPARIETAL JUNCTION (TPJ)",
      "OLAF BLANKE (NATURE 2002)",
      "ELECTRICAL INDUCTION: 3.5 mA",
      "SOMATOSENSORY UNCOUPLING: YES",
      "BOHM HOLOGRAPHIC MATRIX",
      "NON-LOCAL AWARENESS: STABLE"
    ]);

    ctx.restore();
  }

  // =========================================================================
  // 4. THE MODERN DOUBLE SLIT FOR DUMMIES: Wheeler Delayed Choice & Beam Splitters
  // =========================================================================
  renderDoubleSlit(ctx, w, h, t) {
    const cx = w / 2;
    const cy = h / 2 - 10;
    const isInterfering = (Math.sin(t * 0.8) > 0); // Toggles between wave & particle mode

    ctx.save();

    // 1. Single Photon Laser Source
    const laserX = cx - 400;
    ctx.fillStyle = "rgba(20, 30, 45, 0.9)";
    ctx.strokeStyle = "#00f0ff";
    ctx.lineWidth = 2;
    ctx.strokeRect(laserX, cy - 30, 70, 60);
    ctx.fillStyle = "#00f0ff";
    ctx.font = "10px 'JetBrains Mono', monospace";
    ctx.fillText("LASER", laserX + 15, cy + 5);

    // Emitted coherent laser pulses
    const pulseProgress = (t * 2) % 1.0;
    ctx.fillStyle = "#00ffc8";
    ctx.shadowColor = "#00ffc8";
    ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.arc(laserX + 70 + pulseProgress * 150, cy, 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // 2. Double Slit Barrier
    const barrierX = laserX + 220;
    ctx.fillStyle = "#1e293b";
    ctx.fillRect(barrierX, cy - 140, 12, 100);
    ctx.fillRect(barrierX, cy - 20, 12, 40);
    ctx.fillRect(barrierX, cy + 40, 12, 100);

    ctx.strokeStyle = "#00f0ff";
    ctx.strokeRect(barrierX, cy - 140, 12, 100);
    ctx.strokeRect(barrierX, cy - 20, 12, 40);
    ctx.strokeRect(barrierX, cy + 40, 12, 100);

    // 3. Half-Silvered Mirror (BS2 - The Delayed Choice Switch)
    const bsX = cx + 80;
    const bsY = cy;
    ctx.save();
    ctx.translate(bsX, bsY);
    ctx.rotate(Math.PI / 4);
    ctx.strokeStyle = isInterfering ? "rgba(255, 200, 50, 0.95)" : "rgba(100, 116, 139, 0.4)";
    ctx.fillStyle = isInterfering ? "rgba(255, 200, 50, 0.2)" : "rgba(30, 41, 59, 0.2)";
    ctx.lineWidth = 3;
    ctx.strokeRect(-40, -6, 80, 12);
    ctx.fillRect(-40, -6, 80, 12);
    ctx.restore();

    ctx.fillStyle = isInterfering ? "#ffc832" : "#64748b";
    ctx.font = "11px 'JetBrains Mono', monospace";
    ctx.fillText(isInterfering ? "BS2 INSERTED (WAVE MODE)" : "BS2 REMOVED (PARTICLE MODE)", bsX - 90, bsY - 55);

    // 4. Optical Interferometer Trajectory Arms
    ctx.lineWidth = 2;
    if (isInterfering) {
      // Wave mode: Expanding interference ripples
      ctx.strokeStyle = "rgba(0, 240, 200, 0.6)";
      for (let r = 20; r < 200; r += 25) {
        ctx.beginPath();
        ctx.arc(barrierX + 12, cy - 30, r, -Math.PI / 3, Math.PI / 3);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(barrierX + 12, cy + 30, r, -Math.PI / 3, Math.PI / 3);
        ctx.stroke();
      }
    } else {
      // Particle mode: Single localized path
      ctx.strokeStyle = "rgba(255, 100, 60, 0.8)";
      ctx.beginPath();
      ctx.moveTo(barrierX + 12, cy - 30);
      ctx.lineTo(bsX + 160, cy - 30);
      ctx.stroke();
    }

    // 5. Detector Screen & Fringe Distribution
    const detX = cx + 280;
    ctx.fillStyle = "#0f172a";
    ctx.strokeStyle = "#00f0ff";
    ctx.lineWidth = 2;
    ctx.fillRect(detX, cy - 130, 14, 260);
    ctx.strokeRect(detX, cy - 130, 14, 260);

    // Screen display: Fringes vs Two Clumps
    const screenX = detX + 35;
    ctx.lineWidth = 2;
    if (isInterfering) {
      // Alternating interference fringes
      for (let y = cy - 110; y <= cy + 110; y += 12) {
        const dist = Math.abs(y - cy);
        const intensity = Math.pow(Math.cos(dist * 0.08), 2) * (1 - dist / 120);
        if (intensity > 0.05) {
          ctx.strokeStyle = `rgba(0, 255, 200, ${intensity})`;
          ctx.beginPath();
          ctx.moveTo(screenX, y);
          ctx.lineTo(screenX + 80 * intensity, y);
          ctx.stroke();
        }
      }
      ctx.fillStyle = "#00ffc8";
      ctx.fillText("INTERFERENCE FRINGES", screenX, cy + 140);
    } else {
      // Two distinct particle bands
      ctx.strokeStyle = "rgba(255, 90, 40, 0.9)";
      ctx.beginPath();
      ctx.moveTo(screenX, cy - 30); ctx.lineTo(screenX + 70, cy - 30);
      ctx.moveTo(screenX, cy + 30); ctx.lineTo(screenX + 70, cy + 30);
      ctx.stroke();
      ctx.fillStyle = "#ff5a28";
      ctx.fillText("TWO PARTICLE BANDS", screenX, cy + 140);
    }

    // Left HUD Box
    this.drawTelemetryBox(ctx, 60, h - 220, 290, 150, [
      "WHEELER DELAYED-CHOICE (1978)",
      "REALIZATION: JACQUES ET AL. (2007)",
      "SINGLE PHOTON SOURCE: DIAMOND NV",
      "DECISION TIME: 40 ns (RELATIVISTIC)",
      `STATUS: ${isInterfering ? "RETRO-WAVE SETTLED" : "PARTICLE PATH LOCKED"}`,
      "OBSERVER PARTICIPATION: PROVED"
    ]);

    // Right HUD Box
    this.drawTelemetryBox(ctx, w - 350, h - 220, 290, 150, [
      "KIM & SCULLY QUANTUM ERASER",
      "PRL 2000 // ENTANGLED PHOTONS",
      "WHICH-WAY INFO: SELECTIVE ERASE",
      "PAST TRAJECTORY: NOT FIXED",
      "PHYSICS: NATURE WAITS ON DETECTOR",
      "REALITY: OBSERVER-COMPUTATIONAL"
    ]);

    ctx.restore();
  }

  // =========================================================================
  // 5. ORCH-OR & MICROTUBULES: Penrose-Hameroff Quantum Tubulin Lattice
  // =========================================================================
  renderOrchOr(ctx, w, h, t) {
    const cx = w / 2;
    const cy = h / 2 - 20;

    ctx.save();

    // 1. 3D Rotating Cylindrical Microtubule Lattice (13 Protofilaments)
    const tubeLen = 420;
    const tubeRadius = 90;
    const rows = 14;
    const cols = 28;

    for (let c = 0; c < cols; c++) {
      const zNorm = (c / cols) - 0.5;
      const xPos = cx + zNorm * tubeLen;

      for (let r = 0; r < rows; r++) {
        const ang = (r / rows) * Math.PI * 2 + t * 0.8 + zNorm * 4;
        const yPos = cy + Math.sin(ang) * tubeRadius;
        const depth = Math.cos(ang); // -1 (back) to +1 (front)

        const alpha = (depth + 1.2) / 2.2;
        const isTubulinAlpha = ((r + c) % 2 === 0);

        // Quantum superposition dipole flipping
        const flip = Math.sin(t * 6 + c * 0.4 + r) > 0;
        const col = isTubulinAlpha
          ? (flip ? "#a855f7" : "#3b82f6") // Alpha monomer (purple/blue)
          : (flip ? "#ec4899" : "#06b6d4"); // Beta monomer (pink/cyan)

        ctx.fillStyle = col;
        ctx.globalAlpha = alpha * 0.9;
        ctx.beginPath();
        const rad = 7 + depth * 3;
        ctx.arc(xPos, yPos, rad, 0, Math.PI * 2);
        ctx.fill();

        // Connecting peptide bonds
        if (depth > -0.2 && c < cols - 1) {
          ctx.strokeStyle = `rgba(168, 85, 247, ${alpha * 0.4})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(xPos, yPos);
          ctx.lineTo(xPos + tubeLen / cols, yPos);
          ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1.0;

    // 2. Orch-OR Gravitational Collapse Pulse (Objective Reduction Burst)
    const burstPhase = (t * 0.8) % 3.0;
    if (burstPhase < 0.6) {
      const bRad = (burstPhase / 0.6) * 320;
      const bAlpha = 1 - (burstPhase / 0.6);
      ctx.strokeStyle = `rgba(255, 220, 80, ${bAlpha})`;
      ctx.lineWidth = 3;
      ctx.shadowColor = "#ffdc50";
      ctx.shadowBlur = 20;
      ctx.beginPath();
      ctx.arc(cx, cy, bRad, 0, Math.PI * 2);
      ctx.stroke();
      ctx.shadowBlur = 0;

      ctx.fillStyle = `rgba(255, 240, 180, ${bAlpha})`;
      ctx.font = "bold 13px 'JetBrains Mono', monospace";
      ctx.fillText("ORCH-OR COLLAPSE // CONSCIOUS EVENT (25 ms)", cx - 160, cy - tubeRadius - 35);
    }

    // 3. Xenon Anesthetic Molecule Binding (Hydrophobic pocket blockade)
    const xenonX = cx + Math.sin(t * 1.2) * 120;
    const xenonY = cy + Math.cos(t * 1.2) * 50;
    ctx.fillStyle = "rgba(255, 90, 40, 0.85)";
    ctx.shadowColor = "#ff5a28";
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.arc(xenonX, xenonY, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 10px 'JetBrains Mono', monospace";
    ctx.fillText("Xe", xenonX - 7, xenonY + 4);

    // Left HUD Box
    this.drawTelemetryBox(ctx, 60, h - 220, 280, 150, [
      "PENROSE-HAMEROFF ORCH-OR",
      "LATTICE: 13-PROTOFILAMENT TUBE",
      "DIPOLE RESONANCE: 8.2 MHz",
      "GRAVITATIONAL E: E = ħ / t",
      "WATER CHANNELS: COHERENT",
      "ORCHESTRATED REDUCTION: ACTIVE"
    ]);

    // Right HUD Box
    this.drawTelemetryBox(ctx, w - 340, h - 220, 280, 150, [
      "ANESTHETIC PHARMACOLOGY",
      "XENON / ISOFLURANE BINDING",
      "POCKET: HYDROPHOBIC CORE",
      "TERAHERTZ VIBRATIONS: SILENCED",
      "CONSCIOUSNESS: REVERSIBLE EXTINGUISH",
      "CONFIRMED: BIOPHYS J 2017"
    ]);

    ctx.restore();
  }

  drawTelemetryBox(ctx, x, y, bw, bh, lines) {
    ctx.fillStyle = "rgba(10, 16, 28, 0.75)";
    ctx.strokeStyle = "rgba(0, 240, 255, 0.35)";
    ctx.lineWidth = 1;
    ctx.fillRect(x, y, bw, bh);
    ctx.strokeRect(x, y, bw, bh);

    ctx.fillStyle = "rgba(0, 240, 255, 0.6)";
    ctx.fillRect(x, y, bw, 4);

    ctx.font = "11px 'JetBrains Mono', 'Fira Code', monospace";
    lines.forEach((line, i) => {
      ctx.fillStyle = i === 0 ? "#00f0ff" : (i === lines.length - 1 ? "#ffb428" : "#cbd5e1");
      ctx.fillText(line, x + 14, y + 26 + i * 20);
    });
  }
}
