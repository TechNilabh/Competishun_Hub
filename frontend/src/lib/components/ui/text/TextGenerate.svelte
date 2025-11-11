<script lang="ts">
	import { Motion } from 'svelte-motion';

	export let delay: number = 0.05;
	export let duration: number = 0.3;
	export let text: string =
		'8085 Microprocessor Emulator: An object-oriented C++ emulator for the Intel 8085, providing a virtual environment for assembly programming, debugging, and learning. Features CLI and Qt GUI.ategies.';
	export let color: string = 'text-white';
	export let sizing: string = 'text-base sm:text-lg lg:text-xl xl:text-xl';
</script>

<p class="mb-4 {color} {sizing}">
	{#each text.split(' ') as item, index}
		<Motion
			initial={{ opacity: 0, filter: 'blur(4px)', rotateX: 90, y: 5 }}
			transition={{
				ease: 'easeOut',
				duration: duration,
				delay: index * delay
			}}
			animate={{
				opacity: 1,
				filter: 'blur(0px)',
				rotateX: 0,
				y: 0
			}}
			let:motion
		>
			<span use:motion class="inline-block whitespace-pre tracking-tighter">
				{item}
			</span>
		</Motion>
	{/each}
</p>
