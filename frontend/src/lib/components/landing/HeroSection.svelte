<script lang="ts">
	import { ArrowUpRight } from 'lucide-svelte';
	import Button from '$lib/components/ui/button/button.svelte';
	import hero_3d from '$lib/imgs/3d_14.svg';

	let text1: string = 'Agentic AI';
	let text2: string = 'Hackathon';
	let text3: string = 'Build and innovate Agentic AI solutions with our immersive week-long hackathon'
	
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

<section id="hero" class="relative mx-auto mt-32 max-w-7xl px-6 text-center md:px-8">
	<div class="container flex flex-col lg:flex-row lg:space-x-8">
    <div class="relative flex flex-col justify-center left-container order-1 w-auto lg:w-[60%]">
      <h1
        class="-translate-y-4 animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text py-6 text-4xl font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40 sm:text-6xl md:text-7xl lg:text-8xl"
      >
        {text1}<br class="hidden md:block" /> {text2}
      </h1>
      <p
        class="lg:mb-12 -translate-y-4 animate-fade-in text-balance lg:text-right tracking-tight text-gray-400 opacity-0 [--animation-delay:400ms] text-md md:text-xl"
      >
        {text3}
      </p>
    </div>

    <div 
	class="relative right-container flex justify-center items-center order-2 mt-8 lg:mt-0 w-full lg:w-[40%]"
	on:mousemove={handleMove}
	on:mouseleave={reset}
	role="presentation"
	>
	<img
		bind:this={heroEl}
		src={hero_3d}
		alt="hero 3d"
		class="transition-transform duration-300 ease-out"
		style={`transform: translate(${x}px, ${y}px) scale(${scale});`}
	/>
	</div>

  </div>
	
	<a href="https://vision.hack2skill.com/event/genaiexchange?tab=cloudAiLab&utm_source=hack2skill&utm_medium=homepage">
		<Button
			class="-translate-y-4 animate-fade-in gap-1 rounded-lg text-white opacity-0 ease-in-out [--animation-delay:600ms] dark:text-black"
		>
			<span>RSVP </span>
			<ArrowUpRight
				class="ml-1 size-4 transition-transform duration-300 ease-in-out group-hover:translate-x-1"
			/>
		</Button>
	</a>



</section>
