<script lang="ts">
  import { onMount } from "svelte";
  import { theme } from '$lib/stores/theme';

  export let className: string = "";
  export let quantity: number = 100;
  export let staticity: number = 50;
  export let ease: number = 50;
  export let size: number = 0.4;
  export let sizeVariation: number = 0.5;
  export let color: string = $theme === 'dark' ? "#ffffff" : "#000000"; 
  export let trailOpacity: number = 0;
  export let trailColor: string = $theme === 'dark' ? "#000000" : "#ffffff";
  export let glowSize: number = 0;
  export let connectDistance: number = 0;
  export let connectColor: string = $theme === 'dark' ? "#ffffff" : "#000000"; 
  export let connectOpacity: number = 0.2;
  export let vx: number = 0;
  export let vy: number = 0;

  $: {
    color = $theme === 'dark' ? "#ffffff" : "#000000";
    trailColor = $theme === 'dark' ? "#000000" : "#ffffff";
    connectColor = $theme === 'dark' ? "#ffffff" : "#000000";
    rgb = hexToRgb(color);
    trailRgb = hexToRgb(trailColor);
    connectRgb = hexToRgb(connectColor);
  }

  let canvasRef: HTMLCanvasElement;
  let canvasContainerRef: HTMLDivElement;
  let context: CanvasRenderingContext2D | null = null;
  type Circle = {
    x: number;
    y: number;
    translateX: number;
    translateY: number;
    size: number;
    alpha: number;
    targetAlpha: number;
    dx: number;
    dy: number;
    magnetism: number;
  };

  let circles: Circle[] = [];
  let mouse = { x: 0, y: 0 };
  let canvasSize = { w: 0, h: 0 };
  const dpr = typeof window !== "undefined" ? window.devicePixelRatio : 1;

  let rgb = hexToRgb(color);
  let trailRgb = hexToRgb(trailColor);
  let connectRgb = hexToRgb(connectColor);

  $: {
    rgb = hexToRgb(color);
    trailRgb = hexToRgb(trailColor);
    connectRgb = hexToRgb(connectColor);
  }

  function hexToRgb(hex: string): number[] {
    hex = hex.replace("#", "");
    if (hex.length === 3) {
      hex = hex.split("").map(c => c + c).join("");
    }
    const num = parseInt(hex, 16);
    return [num >> 16, (num >> 8) & 255, num & 255];
  }

  function circleParams(): Circle {
    return {
      x: Math.random() * canvasSize.w,
      y: Math.random() * canvasSize.h,
      translateX: -10,
      translateY: 10,
      size: size * (1 - sizeVariation + Math.random() * 2 * sizeVariation),
      alpha: 0,
      targetAlpha: Math.random() * 0.6 + 1,
      dx: (Math.random() - 0.5) * 0.1,
      dy: (Math.random() - 0.5) * 0.1,
      magnetism: 0.1 + Math.random() * 0.8
    };
  }

  function resizeCanvas() {
    if (canvasContainerRef && canvasRef && context) {
      canvasSize.w = canvasContainerRef.offsetWidth;
      canvasSize.h = canvasContainerRef.offsetHeight;
      canvasRef.width = canvasSize.w * dpr;
      canvasRef.height = canvasSize.h * dpr;
      canvasRef.style.width = `${canvasSize.w}px`;
      canvasRef.style.height = `${canvasSize.h}px`;
      context.scale(dpr, dpr);
    }
  }

  function clearContext() {
    if (context) {
      if (trailOpacity > 0) {
        context.fillStyle = `rgba(${trailRgb.join(", ")}, ${trailOpacity})`;
        context.fillRect(0, 0, canvasSize.w, canvasSize.h);
      } else {
        context.clearRect(0, 0, canvasSize.w, canvasSize.h);
      }
    }
  }

  function drawCircle(circle: Circle, update = false) {
    if (!context) return;

    context.save();
    context.translate(circle.translateX, circle.translateY);

    if (glowSize > 0) {
      context.shadowBlur = glowSize;
      context.shadowColor = `rgba(${rgb.join(", ")}, ${circle.alpha})`;
    }

    context.beginPath();
    context.arc(circle.x, circle.y, circle.size, 0, Math.PI * 2);
    context.fillStyle = `rgba(${rgb.join(", ")}, ${circle.alpha})`;
    context.fill();
    context.restore();

    if (!update) circles.push(circle);
  }

  function drawConnections() {
    if (!context || connectDistance <= 0) return;

    const connectDistSq = connectDistance ** 2;
    context.lineWidth = 0.5;

    for (let i = 0; i < circles.length; i++) {
      for (let j = i + 1; j < circles.length; j++) {
        const a = circles[i];
        const b = circles[j];
        const dx = (a.x + a.translateX) - (b.x + b.translateX);
        const dy = (a.y + a.translateY) - (b.y + b.translateY);
        const distSq = dx * dx + dy * dy;

        if (distSq < connectDistSq) {
          const alpha = (1 - Math.sqrt(distSq) / connectDistance) * connectOpacity;
          context.beginPath();
          context.moveTo(a.x + a.translateX, a.y + a.translateY);
          context.lineTo(b.x + b.translateX, b.y + b.translateY);
          context.strokeStyle = `rgba(${connectRgb.join(", ")}, ${alpha})`;
          context.stroke();
        }
      }
    }
  }

  function animate() {
    clearContext();
    
    circles.forEach((circle, i) => {
      const edge = [
        circle.x + circle.translateX - circle.size,
        canvasSize.w - circle.x - circle.translateX - circle.size,
        circle.y + circle.translateY - circle.size,
        canvasSize.h - circle.y - circle.translateY - circle.size,
      ];
      const closestEdge = Math.min(...edge);
      const remapEdge = Math.min(Math.max(closestEdge / 20, 0), 1);
      circle.alpha = Math.min(circle.alpha + 0.02, circle.targetAlpha * remapEdge);

      circle.x += circle.dx + vx;
      circle.y += circle.dy + vy;
      
      const mouseDistX = mouse.x - (circle.x + circle.translateX);
      const mouseDistY = mouse.y - (circle.y + circle.translateY);
      circle.translateX += (mouseDistX / (staticity / circle.magnetism)) / ease;
      circle.translateY += (mouseDistY / (staticity / circle.magnetism)) / ease;

      if (circle.x < -circle.size || circle.x > canvasSize.w + circle.size ||
          circle.y < -circle.size || circle.y > canvasSize.h + circle.size) {
        circles[i] = circleParams();
      }

      drawCircle(circle, true);
    });

    drawConnections();
    requestAnimationFrame(animate);
  }

  function onMouseMove(e: MouseEvent) {
    const rect = canvasRef.getBoundingClientRect();
    mouse.x = e.clientX - rect.left - canvasSize.w / 2;
    mouse.y = e.clientY - rect.top - canvasSize.h / 2;
  }

  onMount(() => {
    context = canvasRef.getContext("2d");
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    window.addEventListener("mousemove", onMouseMove);
    animate();

    return () => {
      window.removeEventListener("resize", resizeCanvas);
      window.removeEventListener("mousemove", onMouseMove);
    };
  });

  $: if (canvasRef) {
    circles = Array.from({ length: quantity }, circleParams);
  }
</script>

<div class={className} bind:this={canvasContainerRef} aria-hidden="true">
  <canvas bind:this={canvasRef} class="size-full" />
</div>

<style>
  .size-full {
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
</style>