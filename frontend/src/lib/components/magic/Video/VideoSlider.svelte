<script lang="ts">
  import { onMount } from 'svelte';
  import VideoPlayer from './VideoPlayer.svelte';

  export let videos: { src: string; title?: string }[] = [];
  let currentIndex = 0;
  let touchStartX = 0;
  let touchEndX = 0;
  let container: HTMLDivElement;

  const nextVideo = () => {
    currentIndex = (currentIndex + 1) % videos.length;
  };

  const prevVideo = () => {
    currentIndex = (currentIndex - 1 + videos.length) % videos.length;
  };

  const handleTouchStart = (e: TouchEvent) => {
    touchStartX = e.changedTouches[0].screenX;
  };

  const handleTouchEnd = (e: TouchEvent) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  };

  const handleSwipe = () => {
    const threshold = 50; 
    const difference = touchStartX - touchEndX;

    if (difference > threshold) {
      nextVideo();
    } else if (difference < -threshold) {
      prevVideo();
    }
  };

  $: {
    if (container) {
      const videoWidth = container.clientWidth;
      container.scrollTo({
        left: currentIndex * videoWidth,
        behavior: 'smooth'
      });
    }
  }
</script>

<div class="relative w-full max-w-4xl mt-5 mx-auto overflow-hidden rounded-lg shadow-lg">
  <div
    bind:this={container}
    class="flex w-full snap-x snap-mandatory overflow-x-auto scrollbar-hide"
    on:touchstart={handleTouchStart}
    on:touchend={handleTouchEnd}
    style="scroll-snap-type: x mandatory;"
  >
    {#each videos as video, i}
      <div class="flex-shrink-0 w-full snap-start">
        <VideoPlayer src={video.src} active={i === currentIndex} />
        {#if video.title}
          <div class="text-black dark:text-white">
            <h3 class="text-lg font-semibold">{video.title}</h3>
          </div>
        {/if}
      </div>
    {/each}
  </div>

  <!-- Navigation arrows -->
  {#if videos.length > 1}
    <button
      on:click={prevVideo}
      class="absolute left-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 focus:outline-none"
      aria-label="Previous video"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>
    <button
      on:click={nextVideo}
      class="absolute right-4 top-1/2 -translate-y-1/2 bg-black/50 hover:bg-black/70 text-white rounded-full p-2 focus:outline-none"
      aria-label="Next video"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>
  {/if}

  
</div>

<style>
  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
</style>