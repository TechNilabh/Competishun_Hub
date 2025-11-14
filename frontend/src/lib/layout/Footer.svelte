<script lang="ts">
	import DotGrid from '$lib/components/magic/Animations/DotGrid.svelte';
	import { Camera, ThumbsUp, AtSign } from 'lucide-svelte';

	

	import logo_white from '$lib/imgs/AgenticAILogo_white.svg'

	const footerNavs = [
		{
			label: 'Contact',
			items: [
				{
					href: 'mailto:tahmidchoudhury019@gmail.com',
					name: 'Organize'
				}
			]
		}
	];

	const footerSocials: {href: string; name: string; icon: string}[] = [
		// {
		// 	href: '',
		// 	name: 'Discord',
		// 	icon: DiscordSvg
		// },
		// {
		// 	href: '',
		// 	name: 'Twitter',
		// 	icon: TwitterSvg
		// }
	];
</script>


<footer class="relative overflow-hidden mt-32 text-center flex flex-col items-center  shrink-0 isolate z-10">

	<!-- Light mode DotGrid -->
	<div class="block dark:hidden absolute -z-10 inset-0 pointer-events-none h-full">
		<DotGrid baseColor="#EEE" activeColor="#FFFFFF" className="h-full w-full" dotSize={5} gap={15} returnDuration={1}/>
	</div>

	<!-- Dark mode DotGrid -->
	<div class="hidden dark:block absolute -z-10 inset-0 pointer-events-none">
		<DotGrid baseColor="#111" activeColor="#FF00FF" className="h-full w-full" dotSize={5} gap={15} returnDuration={1}/>
	</div>


	<!-- FOOTER CONTENT -->
	<div class="relative z-10 flex flex-col items-center justify-center py-16 px-6">

		<!-- TITLE -->
		<h1 class="-translate-y-4 animate-fade-in bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text py-6 text-3xl font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40 sm:text-4xl md:text-5xl lg:text-6xl">
			National Talent <span class="-translate-y-4 animate-fade-in bg-black bg-clip-text py-6 text-3xl font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:bg-white sm:text-4xl md:text-5xl lg:text-6xl">2025</span>
		</h1>

		<!-- CONTACT US -->
		<div class="text-center mb-6">
			<h2 class="-translate-y-4 animate-fade-in bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text py-6 text-sm font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40 ">CONTACT&nbsp;US</h2>

			<div class="flex gap-6 justify-center text-3xl">
				<a href="/"><Camera /></a>
				<a href="/"><ThumbsUp /></a>
				<a href="/"><AtSign /></a>
			</div>
		</div>

		<!-- COLLABORATION -->
		<p class="mt-10 text-xs tracking-widest opacity-80">
			Made In Collaboration with @Tahmid019
		</p>

	</div>
</footer>


