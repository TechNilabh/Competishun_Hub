<script lang="ts">
  export let min: number = 0;
  export let max: number = 100;
  export let step: number = 1;
  export let value: number = (min + max) / 2;
  export let disabled: boolean = false;
  export let showTooltip: boolean = true;
  export let showLabels: boolean = true;
  export let showTicks: boolean = false;
  export let className: string = '';

  // Reactive updates
  $: percentage = ((value - min) / (max - min)) * 100;
  $: formattedValue = Number.isInteger(value) ? value.toString() : value.toFixed(2);

  function handleInput(e: Event) {
    const target = e.target as HTMLInputElement;
    value = parseFloat(target.value);
  }
</script>

<div
  class={`relative w-full ${className}`}
  class:opacity-50={disabled}
  class:pointer-events-none={disabled}
>
  {#if showLabels}
    <div class="flex justify-between mb-1">
      <span class="text-xs text-gray-500">{min}</span>
      <span class="text-xs text-gray-500">{max}</span>
    </div>
  {/if}

  <div class="relative">
    <input
      type="range"
      min={min}
      max={max}
      step={step}
      bind:value
      on:input={handleInput}
      class={`
        w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer
        dark:bg-gray-700
        [&::-webkit-slider-thumb]:appearance-none
        [&::-webkit-slider-thumb]:h-4
        [&::-webkit-slider-thumb]:w-4
        [&::-webkit-slider-thumb]:rounded-full
        [&::-webkit-slider-thumb]:bg-primary-500
        [&::-webkit-slider-thumb]:hover:bg-primary-600
        [&::-webkit-slider-thumb]:active:bg-primary-700
        [&::-webkit-slider-thumb]:dark:bg-primary-400
        [&::-webkit-slider-thumb]:dark:hover:bg-primary-300
        [&::-moz-range-thumb]:h-4
        [&::-moz-range-thumb]:w-4
        [&::-moz-range-thumb]:rounded-full
        [&::-moz-range-thumb]:bg-primary-500
        [&::-moz-range-thumb]:border-none
      `}
    />

    {#if showTooltip}
      <div
        class="absolute top-[-2.5rem] transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded px-2 py-1"
        style={`left: ${percentage}%`}
      >
        {formattedValue}
        <div class="absolute bottom-[-0.25rem] left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-800"></div>
      </div>
    {/if}

    {#if showTicks}
      <div class="flex justify-between w-full px-2 mt-1">
        {#each Array(Math.floor((max - min) / step)).fill(0) as _, i}
          <div class="w-px h-2 bg-gray-300"></div>
        {/each}
      </div>
    {/if}
  </div>
</div>