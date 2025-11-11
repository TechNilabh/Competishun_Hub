<script lang="ts">
  import { onMount } from 'svelte';
	import ColorButton from '../ui/button/ColorButton.svelte';

  export let data: { targetDate: string };
  const targetDate = data.targetDate;


  let days = 0;
  let hours = 0;
  let minutes = 0;
  let seconds = 0;

  let interval: NodeJS.Timeout;
  let showButton: Boolean = false;

  function updateTimer() {
    const now = new Date().getTime();
    const eventTime = new Date(targetDate).getTime();
    const diff = eventTime - now;

    if (diff <= 0) {
      days = hours = minutes = seconds = 0;
      clearInterval(interval);
      showButton = true;
      return;
    }

    days = Math.floor(diff / (1000 * 60 * 60 * 24));
    hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    seconds = Math.floor((diff % (1000 * 60)) / 1000);
  }

  onMount(() => {
    updateTimer();
    interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  });
</script>

<section class="relative mx-auto mt-32 max-w-7xl px-6 text-center md:px-8">
  <div class="w-full flex flex-col items-center justify-center py-10 px-4  rounded-2xl shadow-xl">
    <h2 class="text-2xl sm:text-3xl lg:text-4xl mb-6 text-center animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text py-6 font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40">
      Event Starts from
    </h2>

    <div class="grid grid-cols-2  sm:grid-cols-4 gap-4 bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text dark:from-white dark:to-white/40 w-full max-w-xl">
      <div class="flex flex-col items-center py-4 hover:scale-[1.07] rounded-xl backdrop-blur-md border border-slate-500/25 transition-all duration-300">
        <span class="text-4xl sm:text-5xl font-semibold ">{days}</span>
        <span class="mt-2 text-sm uppercase tracking-wide">Days</span>
      </div>

      <div class="flex flex-col items-center py-4 hover:scale-[1.07] rounded-xl backdrop-blur-md border border-slate-500/25 transition-all duration-300">
        <span class="text-4xl sm:text-5xl font-semibold ">{hours}</span>
        <span class="mt-2 text-sm uppercase tracking-wide">Hours</span>
      </div>

      <div class="flex flex-col items-center py-4 hover:scale-[1.07] rounded-xl backdrop-blur-md border border-slate-500/25 transition-all duration-300">
        <span class="text-4xl sm:text-5xl font-semibold ">{minutes}</span>
        <span class="mt-2 text-sm uppercase tracking-wide">Minutes</span>
      </div>

      <div class="flex flex-col items-center py-4 hover:scale-[1.07] rounded-xl backdrop-blur-md border border-slate-500/25 transition-all duration-300">
        <span class="text-4xl sm:text-5xl font-semibold ">{seconds}</span>
        <span class="mt-2 text-sm uppercase tracking-wide">Seconds</span>
      </div>
    </div>
    {#if showButton}
      <ColorButton class="text-white dark:text-black mt-10 hover:opacity-75 transition-all duration-300" href='/round'>
        <span>Go Go Go!</span>
      </ColorButton>
    {/if}
  </div>
</section>