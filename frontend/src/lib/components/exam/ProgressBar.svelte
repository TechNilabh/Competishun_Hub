<script lang="ts">
  import { examProgress } from '$lib/stores/exam';
  import { CheckCircle, Circle, Clock } from 'lucide-svelte';
  
  $: progress = $examProgress;
  $: percentageColor = progress.percentage < 30 ? 'from-red-500 to-orange-500' :
                       progress.percentage < 70 ? 'from-yellow-500 to-orange-500' :
                       'from-green-500 to-emerald-500';
</script>

<div class="space-y-3">
  <!-- Progress Bar -->
  <div class="relative">
    <div class="w-full bg-gray-800/50 rounded-full h-4 overflow-hidden shadow-inner border border-gray-700">
      <div 
        class="h-full bg-gradient-to-r {percentageColor} transition-all duration-500 ease-out relative overflow-hidden"
        style="width: {progress.percentage}%"
      >
        <!-- Animated shimmer effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent shimmer"></div>
        
        {#if progress.percentage > 15}
          <div class="absolute inset-0 flex items-center justify-end pr-3">
            <span class="text-xs font-bold text-white drop-shadow-lg">
              {Math.round(progress.percentage)}%
            </span>
          </div>
        {/if}
      </div>
    </div>
    
    {#if progress.percentage <= 15 && progress.percentage > 0}
      <div class="absolute -top-8 left-0 bg-gradient-to-r {percentageColor} px-3 py-1 rounded-full">
        <span class="text-xs font-bold text-white">
          {Math.round(progress.percentage)}%
        </span>
      </div>
    {/if}
  </div>
  
  <div class="flex items-center justify-between text-sm">
    <div class="flex items-center gap-6">
      <!-- Attempted -->
      <div class="flex items-center gap-2">
        <CheckCircle size={18} class="text-green-400" />
        <span class="text-gray-300">
          <span class="font-bold text-green-400">{progress.attempted}</span>
          <span class="text-gray-500 mx-1">/</span>
          <span class="text-gray-400">{progress.total}</span>
        </span>
        <span class="text-gray-500">Attempted</span>
      </div>
      
      <div class="flex items-center gap-2">
        <Circle size={18} class="text-yellow-400" />
        <span class="text-gray-300">
          <span class="font-bold text-yellow-400">{progress.unattempted}</span>
          <span class="text-gray-500">Remaining</span>
        </span>
      </div>
    </div>
    
    {#if progress.percentage === 100}
      <div class="flex items-center gap-2 text-green-400 animate-bounce">
        <CheckCircle size={18} />
        <span class="font-bold">All Complete!</span>
      </div>
    {/if}
  </div>
</div>

<style>
  @keyframes shimmer {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(100%);
    }
  }
  
  .shimmer {
    animation: shimmer 2s infinite;
  }
  
  @keyframes bounce {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-10px);
    }
  }
  
  .animate-bounce {
    animation: bounce 1s infinite;
  }
</style>