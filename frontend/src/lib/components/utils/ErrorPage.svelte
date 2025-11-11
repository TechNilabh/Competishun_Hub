<script lang="ts">
  import Game1 from '$lib/components/magic/Games/SnakeGame.svelte';
  import { browser } from '$app/environment';
  import { goto } from '$app/navigation';
</script>

<div class="flex  flex-col my-12 gap-3 md:flex-row items-center justify-center min-h-screen  text-center md:text-left px-6">
  
  <!-- Left: Game -->
  <div class="w-full md:w-1/2 flex items-center justify-center md:translate-x-16">
    {#if browser}
      <Game1 />
    {/if}
  </div>

  <!-- Right: Error message -->
  <div class="w-full md:w-1/2 flex flex-col items-center md:items-start space-y-4">
    <h1 class="text-2xl sm:text-3xl lg:text-4xl text-center animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40">Oops!</h1>
    <p class="text-gray-400">We couldn't find the page you were looking for</p>
    <button 
      type="button"
      on:click={() => goto('/')}
      class="px-6 py-2 rounded-full bg-black text-white dark:bg-white dark:text-black hover:opacity-10 transition"
      aria-label="Go to home page"
    >
      Go home
    </button>
  </div>
</div>
