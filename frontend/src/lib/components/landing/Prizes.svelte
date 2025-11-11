<script lang="ts">
  import prize_momentos from '$lib/imgs/star23.svg';
  import prize_certificates from '$lib/imgs/prism.svg';
  import prize_goodies from '$lib/imgs/cyl.svg';

  let title = "Prizes";

  const prizeList = [
    {
      name: "Certificates",
      desc: "Official certificates for all participants and winners, recognizing your achievement.",
      image: prize_certificates
    },
    {
      name: "Momentos",
      desc: "Exclusive momentos for winners to commemorate your accomplishment.",
      image: prize_momentos
    },
    {
      name: "Goodies",
      desc: "Premium goodies and merch for finalists and top performers.",
      image: prize_goodies
    }
  ];
</script>

<section id="prizes" class="relative mx-auto mt-32 max-w-7xl px-6 md:px-8 text-center flex flex-col items-center">
  
  <!-- Title -->
  <div class="-translate-y-4 text-2xl sm:text-3xl lg:text-4xl font-bold bg-gradient-to-br from-black from-30% to-black/40 dark:from-white dark:to-white/40 bg-clip-text text-transparent tracking-tight animate-fade-in opacity-0 [--animation-delay:200ms]">
    {title}
  </div>

  <!-- Grid -->
  <div class="mt-12 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 w-full">

    {#each prizeList as prize}
      <div 
        class="p-4 rounded-2xl backdrop-blur-xl border border-black/10 dark:border-white/10 shadow-xl transition-transform duration-300 ease-out cursor-pointer"
        
      >
        <img 
        src={prize.image} alt={prize.name} class="w-28 h-28 mx-auto mb-4 transition duration-200" />

        <div class="text-xl font-semibold mb-2">{prize.name}</div>

        <div class="text-sm text-gray-700 dark:text-gray-300 px-2">
          {prize.desc}
        </div>
      </div>
    {/each}

  </div>

</section>
