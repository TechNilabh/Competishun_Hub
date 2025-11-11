<script lang='ts'>
  import about_image from '$lib/imgs/cube8.svg';
	import { Button } from '../ui/button';
	import WordFadein from "../ui/text/WordFadein.svelte";
  let title = "About";
  let des:string = "The National Talent Hackathon 2026 is a national-level coding and innovation competition organized by the Department of Computer Science and Engineering at NIT Silchar, bringing together college students from across India to showcase their technical skills and creativity. Through three competitive rounds—ranging from aptitude and coding assessments to AI/ML-focused problem solving and an offline grand finale at the NIT Silchar campus—the event challenges participants to innovate and build real-world solutions. With free accommodation for finalists, opportunities for academic interaction, and attractive prizes and certifications, the hackathon offers a high-impact platform for students aspiring to gain national recognition and push the boundaries of technological excellence.";

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
      <Button href='/about' >
        <span class="font-medium">Know More</span>
      </Button>
    </div>
  </div>
  

</section>
