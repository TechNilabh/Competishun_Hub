<script lang="ts">
  import prize_momentos from '$lib/imgs/star23.svg';
  import prize_certificates from '$lib/imgs/prism.svg';
  import prize_goodies from '$lib/imgs/cyl.svg';

  const title = "Prizes";

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

<section 
  id="prizes"
  class="relative mx-auto mt-32 max-w-7xl px-6 md:px-8 text-center flex flex-col items-center animate-fadeIn"
>

  <!-- Title -->
  <h2 class="text-2xl sm:text-3xl lg:text-4xl text-center animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40">
    {title}
  </h2>

  <!-- Prize Grid -->
  <div class="mt-14 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 w-full">

    {#each prizeList as prize, i}
      <div
        class="p-8 rounded-2xl border border-[var(--border)]
               bg-[var(--card-bg)] shadow-lg shadow-black/20
               hover:border-indigo-500 hover:shadow-indigo-500/20
               hover:-translate-y-2 hover:scale-[1.02]
               transition-all duration-300 ease-out cursor-pointer select-none"
      >
        <img
          src={prize.image}
          alt={prize.name}
          class="w-24 h-24 mx-auto mb-5 transition-transform duration-300 group-hover:scale-110"
        />

        <h3 class="text-xl font-bold text-[var(--text-primary)] mb-3">
          {prize.name}
        </h3>

        <p class="text-sm text-[var(--text-secondary)] max-w-xs mx-auto leading-relaxed">
          {prize.desc}
        </p>
      </div>
    {/each}

  </div>

</section>

<style>
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .animate-fadeIn {
    animation: fadeIn 0.4s ease-out;
  }
</style>
