<script lang="ts">
  import { studentProblems, professionalProblems } from '$lib/data/problems';
  import { slide, fade } from 'svelte/transition';

  let track = 'student';
  let openId: number | null = null;

  const list = () => (track === 'student' ? studentProblems : professionalProblems);

  const toggle = (id: number) => {
    openId = openId === id ? null : id;
  };
</script>


<section id="round" class="relative mx-auto mt-32 max-w-7xl px-6 md:px-8">
    <div class="max-w-6xl mx-auto px-4 py-12 flex flex-col justify-center items-center">

        <!-- Heading -->
        <h1 class="text-2xl sm:text-3xl lg:text-4xl text-center animate-fade-in text-balance lg:text-right bg-gradient-to-br from-black from-30% to-black/40 bg-clip-text font-bold leading-none tracking-tighter text-transparent opacity-0 [--animation-delay:200ms] dark:from-white dark:to-white/40 p-10">
        Problem statement
        </h1>


        <!-- Problem list -->
        <div class="flex flex-col gap-6">
        {#each list() as p}
            <div class="rounded-xl bg-white dark:bg-neutral-900 border border-black/10 dark:border-white/10 p-4 md:p-6 transition-all duration-300">

            <div class="flex flex-col md:flex-row gap-4 transition:slide">
                <!-- Image -->
                <img
                src={p.image}
                alt=""
                class="w-full md:w-40 h-32 object-cover rounded-lg"
                />

                <!-- Content -->
                <div class="flex-1">
                <h2 class="text-xl font-semibold mb-1">{p.title}</h2>

                <p class="text-sm opacity-80 mb-2">
                    {p.short}
                </p>

                <!-- View more / View less -->
                {#if openId === p.id}
                <div
                    in:slide={{ duration: 250 }}
                    out:slide={{ duration: 200 }}
                    class="text-sm whitespace-pre-line opacity-90 mb-3"
                >
                    {p.long}
                </div>

                <button
                    class="text-[--color] text-sm font-medium"
                    on:click={() => toggle(p.id)}
                >
                    View less
                </button>
                {:else}
                <button
                    class="text-[--color] text-sm font-medium"
                    on:click={() => toggle(p.id)}
                >
                    View more
                </button>
                {/if}

                </div>
            </div>
            </div>
        {/each}
        </div>
    </div>
</section>
