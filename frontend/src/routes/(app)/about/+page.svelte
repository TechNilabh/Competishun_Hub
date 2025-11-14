<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import hero from "$lib/imgs/cube8.svg";

  // Content
  const title = "National Talent Hackathon 2026";
  const tagline =
    "A multi-stage national coding initiative led by the Department of Computer Science & Engineering, NIT Silchar — designed to assess clarity of thought, engineering discipline, and real-world AI/ML problem-solving.";

  const facts = [
    { label: "Organizer", value: "Dept. of CSE, NIT Silchar" },
    { label: "Team Size", value: "Up to 3 members" },
    { label: "Registration", value: "Till 30 Dec 2025" },
    { label: "Fee", value: "₹2000 / team" },
    { label: "Finale Venue", value: "NIT Silchar Campus (Offline)" }
  ];

  const prizes = [
    { place: "1st", amount: "₹50,000" },
    { place: "2nd", amount: "₹40,000" },
    { place: "3rd", amount: "₹30,000" }
  ];

  const certificates = [
    "Participation Certificate",
    "Appreciation Certificate (≥50% or Top 75%)",
    "Outstanding Performance Certificate (Top 10%)"
  ];

  const rounds = [
    {
      title: "Round 1 — Screening",
      when: "January 2026 (2nd week)",
      mode: "Online",
      details: "MCQs, aptitude evaluation, and foundational coding tasks."
    },
    {
      title: "Round 2 — AI/ML Coding",
      when: "February 2026 (1st week)",
      mode: "Online",
      details: "Coding challenges and focused AI/ML-driven problem statements."
    },
    {
      title: "Round 3 — Grand Finale",
      when: "February 2026 (last week)",
      mode: "Offline",
      details: "Real-time problem solving at NIT Silchar with curated test data."
    }
  ];

  const rankings = [
    { label: "NIRF Engineering 2024", value: "Rank 40" },
    { label: "NIRF Overall 2024", value: "Rank 92" },
    { label: "QS Asia 2025", value: "Rank 541" },
    { label: "Green Metric 2022", value: "Rank 205" }
  ];

  const perks = [
    "Free accommodation during finale",
    "Campus & local exposure",
    "Faculty interactions & Gala Dinner"
  ];

  // Parallax
  let rootEl: HTMLElement;
  let mouseX = 0, mouseY = 0, scrollY = 0, frame = 0;

  function handleMouse(e: MouseEvent) {
    const r = rootEl.getBoundingClientRect();
    mouseX = (e.clientX - (r.left + r.width / 2)) / r.width;
    mouseY = (e.clientY - (r.top + r.height / 2)) / r.height;
    requestFrame();
  }

  function handleScroll() {
    scrollY = window.scrollY;
    requestFrame();
  }

  function requestFrame() {
    if (!frame) frame = requestAnimationFrame(applyParallax);
  }

  function applyParallax() {
    frame = 0;
    const layers = rootEl.querySelectorAll("[data-depth]");
    layers.forEach((el: Element) => {
      const htmlEl = el as HTMLElement;
      const d = parseFloat(htmlEl.dataset.depth || "0");
      const tx = mouseX * d * 14;
      const ty = mouseY * d * 14 + scrollY * d * 0.12;
      htmlEl.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
    });
  }

  onMount(() => {
    if (typeof window === "undefined") return;

    const onScroll = () => {
      scrollY = window.scrollY;
      requestFrame();
    };

    window.addEventListener("scroll", onScroll, { passive: true });

    onScroll();

    return () => {
      window.removeEventListener("scroll", onScroll);
    };
  });


  onDestroy(() => {
    window.removeEventListener("scroll", handleScroll);
    if (frame) cancelAnimationFrame(frame);
  });

  function onRegister() {
    window.location.href = "/register";
  }
</script>


<section
  id="about"
  bind:this={rootEl}
  class="relative mx-auto max-w-6xl px-6 md:px-10 pt-36 pb-36"
  on:mousemove={handleMouse}
  role="presentation"
>

  <!-- Parallax Outline Shapes -->
  <img src={hero} alt="" aria-hidden="true"
    class="hidden md:block absolute -top-32 -left-20 w-40 opacity-10 dark:opacity-15
           contrast-0 invert-0 mix-blend-multiply dark:mix-blend-lighten"
    data-depth="0.2" />

  <img src={hero} alt="" aria-hidden="true"
    class="hidden md:block absolute top-60 -right-16 w-32 opacity-10 dark:opacity-15
           contrast-0 mix-blend-multiply dark:invert"
    data-depth="0.45" />

  <img src={hero} alt="" aria-hidden="true"
    class="hidden md:block absolute bottom-10 left-1/2 -translate-x-1/2 w-28
           opacity-5 dark:opacity-10 contrast-0"
    data-depth="0.7" />


  <!-- Title Section -->
  <div class="max-w-4xl mx-auto text-center">

    <h1 class="font-mono text-4xl md:text-6xl font-bold tracking-[-0.015em] leading-[1.08]">
      {title}
    </h1>

    <p class="mt-6 font-sans text-[17px] md:text-[18px] leading-8 text-black/75 dark:text-white/75 max-w-3xl mx-auto">
      {tagline}
    </p>

    <button
      on:click={onRegister}
      class="mt-10 font-mono tracking-tight text-sm px-6 py-3 border border-black/10 dark:border-white/20
             hover:bg-black/5 dark:hover:bg-white/10 transition-colors">
      Register
    </button>
  </div>


  <!-- Facts -->
  <div class="mt-32 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-10">
    {#each facts as f}
      <div class="text-center">
        <div class="font-mono text-xs tracking-[0.1em] text-black/60 dark:text-white/60 uppercase">
          {f.label}
        </div>
        <div class="mt-3 font-sans text-lg tracking-tight">
          {f.value}
        </div>
      </div>
    {/each}
  </div>


  <!-- NIT Silchar -->
  <div class="mt-40 max-w-3xl mx-auto text-left">
    <h2 class="font-mono text-2xl md:text-3xl font-semibold tracking-tight">
      About NIT Silchar
    </h2>

    <p class="mt-6 font-sans text-[16px] leading-8 text-black/75 dark:text-white/75">
      Established in 1967 and declared an Institute of National Importance under the NIT Act 2007,
      NIT Silchar is recognized nationwide for engineering rigor, research depth, and academic distinction.
    </p>

    <div class="mt-10 space-y-3">
      {#each rankings as r}
        <div class="font-mono text-sm flex justify-between border-b border-black/10 dark:border-white/10 pb-3">
          <span>{r.label}</span>
          <span>{r.value}</span>
        </div>
      {/each}
    </div>
  </div>


  <!-- Rounds -->
  <div class="mt-40 max-w-3xl mx-auto">
    <h2 class="font-mono text-2xl md:text-3xl font-semibold tracking-tight">
      Competition Structure
    </h2>

    <div class="mt-12 space-y-16">
      {#each rounds as r}
        <div>
          <div class="font-mono text-base tracking-tight">{r.title}</div>

          <div class="mt-2 flex gap-6 text-sm text-black/60 dark:text-white/60 font-mono">
            <span>{r.mode}</span>
            <span>{r.when}</span>
          </div>

          <p class="mt-4 font-sans text-[16px] leading-7 text-black/70 dark:text-white/70">
            {r.details}
          </p>
        </div>
      {/each}
    </div>
  </div>


  <!-- Prizes / Certificates -->
  <div class="mt-40 grid md:grid-cols-2 gap-20 max-w-4xl mx-auto">

    <div>
      <h2 class="font-mono text-2xl md:text-3xl font-semibold tracking-tight">
        Prizes
      </h2>

      <div class="mt-10 space-y-6">
        {#each prizes as p}
          <div class="font-mono text-base flex justify-between border-b border-black/10 dark:border-white/10 pb-4">
            <span>{p.place}</span>
            <span>{p.amount}</span>
          </div>
        {/each}
      </div>
    </div>

    <div>
      <h2 class="font-mono text-2xl md:text-3xl font-semibold tracking-tight">
        Certificates
      </h2>

      <ul class="mt-10 space-y-5 font-sans text-[16px] leading-7">
        {#each certificates as c}
          <li class="font-mono text-sm pb-2 border-b border-black/10 dark:border-white/10">
            {c}
          </li>
        {/each}
      </ul>
    </div>

  </div>


  <!-- Perks -->
  <div class="mt-40 max-w-3xl mx-auto">
    <h2 class="font-mono text-2xl md:text-3xl font-semibold tracking-tight">
      What participants receive
    </h2>

    <ul class="mt-10 space-y-5">
      {#each perks as perk}
        <li class="font-mono text-sm text-black/80 dark:text-white/80">
          {perk}
        </li>
      {/each}
    </ul>
  </div>


  <!-- Footer Note -->
  <div class="mt-40 text-center font-mono text-xs text-black/50 dark:text-white/50">
    Account details and registration link will be provided by the organizers.
  </div>

</section>

<style>
  [data-depth] {
    will-change: transform;
    transition: transform 120ms ease-out;
  }
</style>
