<script lang='ts'>
  import about_image from '$lib/imgs/cube8.svg';
	import WordFadein from "../ui/text/WordFadein.svelte";
  let title = "About";
  let des:string = "Agentic AI 2025 is a five-day hackathon hosted in collaboration with GDG NITS and ML Club NIT Silchar, running from 11 to 15 November and focused on building innovative, real-world solutions with emerging agentic AI systems. Participants team up for an intensive Vibe Coding–driven build sprint, develop prototypes, and get hands-on guidance throughout the event, culminating in an exclusive Google Expert speaker session on 15 November that dives into cutting-edge AI insights and industry perspectives. It’s the perfect space for developers and students to learn, collaborate, and push the boundaries of what’s possible with AI.";

  let heroEl: HTMLImageElement;
	let x = 0;
	let y = 0;
	let scale = 1;

	function handleMove(e: MouseEvent) {
	const rect = heroEl.getBoundingClientRect();
	const offsetX = e.clientX - (rect.left + rect.width / 2);
	const offsetY = e.clientY - (rect.top + rect.height / 2);

	x = offsetX * 0.05;  
	y = offsetY * 0.05;

	const dist = Math.sqrt(offsetX**2 + offsetY**2);
	const maxDist = Math.max(rect.width, rect.height) / 2;

	scale = 1 + (1 - Math.min(dist / maxDist, 1)) * 0.12;
	}

	function reset() {
	x = 0;
	y = 0;
	scale = 1;
	}

</script>

<section id="about" class="relative mx-auto mt-28 max-w-7xl px-6 text-center md:px-8 
  flex flex-col justify-center items-center
">
  <div class="text-2xl sm:text-3xl lg:text-4xl text-center animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40">{title}</div>
  
  <div class="container p-2 flex flex-col md:flex-row justify-center items-center gap-3">
    <div class="left w-auto"
      on:mousemove={handleMove}
      on:mouseleave={reset}
      role="presentation"
    >
      <img 
        bind:this={heroEl}
        src={about_image} alt="about"
        class="transition-transform duration-300 ease-out"
		    style={`transform: translate(${x}px, ${y}px) scale(${scale});`}
      >
    </div>
    <div class="right md:w-[60%]">
      <WordFadein words={des} />
    </div>
  </div>

</section>
