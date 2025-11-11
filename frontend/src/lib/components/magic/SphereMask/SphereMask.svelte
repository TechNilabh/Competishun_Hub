<script lang="ts">
  import { cn } from '$lib/utils';
  export let reverse: boolean = false;
</script>

<div
  class={cn(
    // color logic
    '[--color:var(--color-three)] dark:[--color:var(--color-one)]',

    'pointer-events-none relative mx-auto h-[50rem] overflow-hidden',

    // soft radial mask for smoother fade
    '[mask-image:radial-gradient(ellipse_at_center_center,#000,transparent_55%)]',

    reverse
      ? 'my-[-22rem] rotate-180 md:mt-[-30rem]'
      : 'my-[-18.8rem]',

    // glow bloom layer
    'before:absolute before:inset-0 before:size-full before:opacity-45',
    'before:[background-image:radial-gradient(circle_at_bottom_center,var(--color),transparent_75%)]',

    // bottom halo trim
    'after:absolute after:-left-1/2 after:top-1/2 after:aspect-[1/0.7] after:w-[200%]',
    'after:rounded-[50%] after:border-t after:border-[hsl(var(--border))] after:bg-background'
  )}
></div>
