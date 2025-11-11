<script lang="ts">
	import { ArrowRightIcon } from "lucide-svelte";
	import { Button } from "../ui/button";
	import ParticleCard from "../ui/card/ParticleCard.svelte";

    let title = "Under construction"
    let des = "Meanwhile you can checkout the official documentations from Intel."
</script>

<section id="docs" class="relative mx-auto mt-28 max-w-7xl px-6 text-center md:px-8">
    <!-- <span
    class="pointer-events-none whitespace-pre-wrap bg-gradient-to-b from-gray-900 to-gray-600 bg-clip-text text-center text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-semibold font-poppins leading-tight text-transparent 
            dark:from-gray-100 dark:to-gray-400 pb-3 xl:pb-5"
    >
        Documentations
    </span> -->
    <a href="https://ia801901.us.archive.org/28/items/bitsavers_intelISISIssemblyLanguageProgrammingManualMay81_7150831/9800301-04_8080_8085_Assembly_Language_Programming_Manual_May81.pdf">
		<Button
			class="-translate-y-4 animate-fade-in gap-1 rounded-lg text-white opacity-0 ease-in-out [--animation-delay:600ms] dark:text-black"
		>
			<span>Official Doc </span>
			<ArrowRightIcon
				class="ml-1 size-4 transition-transform duration-300 ease-in-out group-hover:translate-x-1"
			/>
		</Button>
	</a>
    <div class="m-5" />
    <ParticleCard title={title} description={des} />
</section>