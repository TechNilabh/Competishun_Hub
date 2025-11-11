<script lang="ts">
  import { cn } from "$lib/utils";
  import { AnimatePresence, Motion } from "svelte-motion";

  let className: any = "";
  export { className as class };

  export let words = "Fade In";
  export let delay = 0.05;
  export let variants = {
    hidden: { opacity: 0 },
    visible: (i: any) => ({
      y: 0,
      opacity: 1,
      transition: { delay: i * delay },
    }),
  };
  let wordsspilit = words.split(" ");
</script>

<Motion {variants} initial="hidden" animate="visible" let:motion>
  <h1
    class={cn(
      "font-display text-justify text-sm font-medium tracking-[-0.02em] text-gray-600 drop-shadow-sm dark:text-gray-400 md:text-base lg:text-xl",
      className
    )}
    use:motion
  >
    {#each wordsspilit as word, i}
      <Motion {variants} custom={i} let:motion>
        <span use:motion> {word}</span>
      </Motion>
    {/each}
  </h1>
</Motion>
