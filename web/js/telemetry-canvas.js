// web/js/telemetry-canvas.js — Interactive Cyber-Radar & Telemetry Background

export function initTelemetryBackground(canvasId = "bg-telemetry-canvas") {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let w = (canvas.width = window.innerWidth);
  let h = (canvas.height = window.innerHeight);

  let mouseX = w / 2;
  let mouseY = h / 2;
  let targetMouseX = w / 2;
  let targetMouseY = h / 2;

  window.addEventListener("resize", () => {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
  });

  window.addEventListener("mousemove", (e) => {
    targetMouseX = e.clientX;
    targetMouseY = e.clientY;
  });

  // Telemetry nodes
  const nodes = [];
  const NODE_COUNT = 36;
  for (let i = 0; i < NODE_COUNT; i++) {
    nodes.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 2 + 1,
      alpha: Math.random() * 0.4 + 0.1,
      pulse: Math.random() * Math.PI,
    });
  }

  let radarAngle = 0;

  function render() {
    // Smooth mouse parallax
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    ctx.clearRect(0, 0, w, h);

    // Subtle Grid
    ctx.strokeStyle = "rgba(0, 229, 255, 0.025)";
    ctx.lineWidth = 1;
    const gridSize = 64;
    const offsetX = (mouseX * 0.02) % gridSize;
    const offsetY = (mouseY * 0.02) % gridSize;

    ctx.beginPath();
    for (let x = offsetX; x < w; x += gridSize) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
    }
    for (let y = offsetY; y < h; y += gridSize) {
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
    }
    ctx.stroke();

    // Radar Center on right side of viewport
    const radarCx = w * 0.85 + (mouseX - w / 2) * 0.03;
    const radarCy = h * 0.45 + (mouseY - h / 2) * 0.03;
    const radarRadius = Math.max(w, h) * 0.55;

    // Draw radar rings
    ctx.strokeStyle = "rgba(0, 229, 255, 0.04)";
    for (let r = 80; r < radarRadius; r += 120) {
      ctx.beginPath();
      ctx.arc(radarCx, radarCy, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Sweeping Radar Beam
    radarAngle += 0.012;
    if (radarAngle > Math.PI * 2) radarAngle -= Math.PI * 2;

    const sweepGrad = ctx.createRadialGradient(
      radarCx,
      radarCy,
      10,
      radarCx,
      radarCy,
      radarRadius
    );
    sweepGrad.addColorStop(0, "rgba(0, 229, 255, 0.08)");
    sweepGrad.addColorStop(0.8, "rgba(0, 229, 255, 0.015)");
    sweepGrad.addColorStop(1, "rgba(0, 229, 255, 0)");

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(radarCx, radarCy);
    ctx.arc(radarCx, radarCy, radarRadius, radarAngle - 0.25, radarAngle);
    ctx.closePath();
    ctx.fillStyle = sweepGrad;
    ctx.fill();
    ctx.restore();

    // Draw & link telemetry nodes
    for (let i = 0; i < nodes.length; i++) {
      const p = nodes[i];
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;
      p.pulse += 0.03;

      const currentAlpha = p.alpha + Math.sin(p.pulse) * 0.15;
      ctx.fillStyle = `rgba(0, 229, 255, ${Math.max(0.05, currentAlpha)})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();

      // Connect nearby nodes
      for (let j = i + 1; j < nodes.length; j++) {
        const p2 = nodes[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          ctx.strokeStyle = `rgba(0, 229, 255, ${0.05 * (1 - dist / 130)})`;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(render);
  }

  requestAnimationFrame(render);

  // 3D Parallax Tilt for Hero Spotlight
  const hero = document.getElementById("hero-spotlight");
  if (hero) {
    document.addEventListener("mousemove", (e) => {
      const rect = hero.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / (window.innerWidth / 2);
      const dy = (e.clientY - cy) / (window.innerHeight / 2);
      hero.style.transform = `rotateY(${dx * 2.5}deg) rotateX(${-dy * 2.5}deg)`;
    });
  }
}
