<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { gsap } from "gsap";
  import { InertiaPlugin } from "gsap/InertiaPlugin";

  gsap.registerPlugin(InertiaPlugin);

  // Throttle function
  const throttle = (func: (...args: any[]) => void, limit: number) => {
    let lastCall = 0;
    return function (this: unknown, ...args: any[]) {
      const now = performance.now();
      if (now - lastCall >= limit) {
        lastCall = now;
        func.apply(this, args);
      }
    };
  };

  interface Dot {
    cx: number;
    cy: number;
    xOffset: number;
    yOffset: number;
    _inertiaApplied: boolean;
  }

  // Props
  export let dotSize = 16;
  export let gap = 20;
  export let baseColor = "#5227FF";
  export let activeColor = "#5227FF";
  export let proximity = 150;
  export let speedTrigger = 100;
  export let shockRadius = 250;
  export let shockStrength = 5;
  export let maxSpeed = 5000;
  export let resistance = 750;
  export let returnDuration = 2;
  export let className = "";
  export let style: any = {};

  let wrapperEl: HTMLDivElement;
  let canvasEl: HTMLCanvasElement;

  let dots: Dot[] = [];

  const pointer = {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    speed: 0,
    lastTime: 0,
    lastX: 0,
    lastY: 0
  };

  function hexToRgb(hex: string) {
    const m = hex.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
    if (!m) return { r: 0, g: 0, b: 0 };
    return {
      r: parseInt(m[1], 16),
      g: parseInt(m[2], 16),
      b: parseInt(m[3], 16)
    };
  }

  let circlePath: Path2D | null = null;
  let baseRgb = hexToRgb(baseColor);
  let activeRgb = hexToRgb(activeColor);

  function buildGrid() {
    if (!wrapperEl || !canvasEl) return;

    const { width, height } = wrapperEl.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    canvasEl.width = width * dpr;
    canvasEl.height = height * dpr;
    canvasEl.style.width = width + "px";
    canvasEl.style.height = height + "px";

    const ctx = canvasEl.getContext("2d");
    if (ctx) ctx.scale(dpr, dpr);

    const cols = Math.floor((width + gap) / (dotSize + gap));
    const rows = Math.floor((height + gap) / (dotSize + gap));
    const cell = dotSize + gap;

    const gridW = cell * cols - gap;
    const gridH = cell * rows - gap;

    const startX = (width - gridW) / 2 + dotSize / 2;
    const startY = (height - gridH) / 2 + dotSize / 2;

    const newDots: Dot[] = [];
    for (let y = 0; y < rows; y++) {
      for (let x = 0; x < cols; x++) {
        newDots.push({
          cx: startX + x * cell,
          cy: startY + y * cell,
          xOffset: 0,
          yOffset: 0,
          _inertiaApplied: false
        });
      }
    }
    dots = newDots;
  }

  onMount(() => {
    if (window.Path2D) {
      circlePath = new Path2D();
      circlePath.arc(0, 0, dotSize / 2, 0, Math.PI * 2);
    }

    baseRgb = hexToRgb(baseColor);
    activeRgb = hexToRgb(activeColor);

    buildGrid();

    // Resize observer
    const ro = new ResizeObserver(() => buildGrid());
    ro.observe(wrapperEl);

    // Drawing loop
    let rafId: number;
    const proxSq = proximity * proximity;

    function draw() {
      if (!canvasEl) return;

      const ctx = canvasEl.getContext("2d");
      if (!ctx || !circlePath) return;

      ctx.clearRect(0, 0, canvasEl.width, canvasEl.height);

      for (const dot of dots) {
        const ox = dot.cx + dot.xOffset;
        const oy = dot.cy + dot.yOffset;

        const dx = dot.cx - pointer.x;
        const dy = dot.cy - pointer.y;
        const dsq = dx * dx + dy * dy;

        let style = baseColor;

        if (dsq <= proxSq) {
          const dist = Math.sqrt(dsq);
          const t = 1 - dist / proximity;
          const r = Math.round(baseRgb.r + (activeRgb.r - baseRgb.r) * t);
          const g = Math.round(baseRgb.g + (activeRgb.g - baseRgb.g) * t);
          const b = Math.round(baseRgb.b + (activeRgb.b - baseRgb.b) * t);
          style = `rgb(${r},${g},${b})`;
        }

        ctx.save();
        ctx.translate(ox, oy);
        ctx.fillStyle = style;
        ctx.fill(circlePath);
        ctx.restore();
      }

      rafId = requestAnimationFrame(draw);
    }

    draw();

    // Pointer movement
    const onMove = (e: MouseEvent) => {
      const now = performance.now();
      const dt = pointer.lastTime ? now - pointer.lastTime : 16;

      const dx = e.clientX - pointer.lastX;
      const dy = e.clientY - pointer.lastY;

      let vx = (dx / dt) * 1000;
      let vy = (dy / dt) * 1000;
      let speed = Math.hypot(vx, vy);

      if (speed > maxSpeed) {
        const s = maxSpeed / speed;
        vx *= s;
        vy *= s;
        speed = maxSpeed;
      }

      pointer.lastTime = now;
      pointer.lastX = e.clientX;
      pointer.lastY = e.clientY;
      pointer.vx = vx;
      pointer.vy = vy;
      pointer.speed = speed;

      const rect = canvasEl.getBoundingClientRect();
      pointer.x = e.clientX - rect.left;
      pointer.y = e.clientY - rect.top;

      for (const dot of dots) {
        const dist = Math.hypot(dot.cx - pointer.x, dot.cy - pointer.y);
        if (speed > speedTrigger && dist < proximity && !dot._inertiaApplied) {
          dot._inertiaApplied = true;

          gsap.killTweensOf(dot);

          const pushX = dot.cx - pointer.x + vx * 0.005;
          const pushY = dot.cy - pointer.y + vy * 0.005;

          gsap.to(dot, {
            inertia: { xOffset: pushX, yOffset: pushY, resistance },
            onComplete: () => {
              gsap.to(dot, {
                xOffset: 0,
                yOffset: 0,
                duration: returnDuration,
                ease: "elastic.out(1,0.75)"
              });
              dot._inertiaApplied = false;
            }
          });
        }
      }
    };

    const onClick = (e: MouseEvent) => {
      const rect = canvasEl.getBoundingClientRect();
      const cx = e.clientX - rect.left;
      const cy = e.clientY - rect.top;

      for (const dot of dots) {
        const dist = Math.hypot(dot.cx - cx, dot.cy - cy);
        if (dist < shockRadius && !dot._inertiaApplied) {
          dot._inertiaApplied = true;

          gsap.killTweensOf(dot);

          const falloff = Math.max(0, 1 - dist / shockRadius);
          const pushX = (dot.cx - cx) * shockStrength * falloff;
          const pushY = (dot.cy - cy) * shockStrength * falloff;

          gsap.to(dot, {
            inertia: { xOffset: pushX, yOffset: pushY, resistance },
            onComplete: () => {
              gsap.to(dot, {
                xOffset: 0,
                yOffset: 0,
                duration: returnDuration,
                ease: "elastic.out(1,0.75)"
              });
              dot._inertiaApplied = false;
            }
          });
        }
      }
    };

    const throttledMove = throttle(onMove, 50);
    window.addEventListener("mousemove", throttledMove);
    window.addEventListener("click", onClick);

    onDestroy(() => {
      ro.disconnect();
      cancelAnimationFrame(rafId);
      window.removeEventListener("mousemove", throttledMove);
      window.removeEventListener("click", onClick);
    });
  });
</script>

<section class={`p-4 flex items-center justify-center h-full w-full relative ${className}`} style={style}>
  <div bind:this={wrapperEl} class="w-full h-full relative">
    <canvas bind:this={canvasEl} class="absolute inset-0 w-full h-full pointer-events-none"></canvas>
  </div>
</section>
