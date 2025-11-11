<script lang='ts'>
  import Particles from '$lib/components/magic/Stars/Stars.svelte';
    export let title = "Title";
    export let description = "Description.";
</script>

<div
  class="relative flex p-4 text-center md:p-6 lg:p-8 flex-col items-center justify-center overflow-hidden rounded-lg border bg-background md:shadow-xl"
>
    <span
    class="pointer-events-none whitespace-pre-wrap bg-gradient-to-b from-gray-900 to-gray-600 bg-clip-text text-center text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-semibold font-poppins leading-tight text-transparent 
            dark:from-gray-100 dark:to-gray-400 pb-3 xl:pb-5"
    >
    {title}
    </span>

    <p class="pointer-events-none whitespace-pre-wrap text-justify text-xs md:text-sm lg:text-base xl:text-lg bg-gradient-to-b from-gray-800 to-gray-500 bg-clip-text font-medium font-poppins leading-relaxed text-transparent
            dark:from-gray-200 dark:to-gray-400">
    {description}
    </p>
    <Particles className="absolute inset-0" quantity={350} color={"000000"} />
</div>