<script lang="ts">
  import { proctoringStore } from '$lib/stores/proctoring';
  import { AlertTriangle } from 'lucide-svelte';
  import { fly } from 'svelte/transition';
  
  $: violations = $proctoringStore.violations;
  $: lastViolationType = $proctoringStore.lastViolationType;
  $: showWarning = violations > 0;
  $: faceDetected = $proctoringStore.faceDetected;
  $: multipleFaces = $proctoringStore.multipleFaces;
  
  function getViolationMessage(type: string | null): string {
    const messages: Record<string, string> = {
      'no_face': 'No face detected! Please stay in frame.',
      'multiple_faces': 'Multiple faces detected! Ensure you are alone.',
      'looking_away': 'Please look at the screen.',
      'tab_switch': 'Tab switching detected! Stay on this page.',
      'audio_detected': 'External audio detected!',
    };
    return type ? messages[type] || 'Violation detected!' : '';
  }
</script>

{#if showWarning && lastViolationType}
  <div
    class="fixed top-24 right-4 z-50 max-w-sm"
    transition:fly={{ x: 300, duration: 300 }}
  >
    <div class="bg-red-500 text-white px-4 py-3 rounded-lg shadow-2xl border-2 border-red-700 animate-shake">
      <div class="flex items-start gap-3">
        <AlertTriangle size={24} class="flex-shrink-0 mt-0.5 animate-pulse" />
        <div class="flex-1">
          <h3 class="font-bold text-lg">⚠️ Warning {violations}/3</h3>
          <p class="text-sm mt-1">{getViolationMessage(lastViolationType)}</p>
          {#if violations >= 3}
            <p class="text-xs mt-2 font-semibold bg-red-700 px-2 py-1 rounded animate-pulse">
              🚨 Maximum violations reached! Exam will be auto-submitted.
            </p>
          {/if}
        </div>
      </div>
    </div>
  </div>
{/if}

{#if violations >= 2}
  <div class="fixed inset-0 pointer-events-none z-40">
    <div class="absolute inset-0 border-4 border-red-500 animate-flash-border"></div>
  </div>
{/if}

<div class="fixed bottom-4 right-4 z-50 space-y-2">
  {#if !faceDetected}
    <div class="bg-yellow-500 text-black px-3 py-2 rounded-lg shadow-lg text-sm font-semibold animate-bounce flex items-center gap-2">
      <span class="w-2 h-2 bg-black rounded-full animate-pulse"></span>
      Face Not Detected
    </div>
  {/if}
  
  {#if multipleFaces}
    <div class="bg-red-500 text-white px-3 py-2 rounded-lg shadow-lg text-sm font-semibold animate-bounce flex items-center gap-2">
      <span class="w-2 h-2 bg-white rounded-full animate-pulse"></span>
      Multiple People Detected
    </div>
  {/if}
</div>

<style>
  @keyframes shake {
    0%, 100% {
      transform: translateX(0);
    }
    10%, 30%, 50%, 70%, 90% {
      transform: translateX(-5px);
    }
    20%, 40%, 60%, 80% {
      transform: translateX(5px);
    }
  }
  
  @keyframes flash-border {
    0%, 100% {
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  @keyframes bounce {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-10px);
    }
  }
  
  .animate-shake {
    animation: shake 0.5s;
  }
  
  .animate-flash-border {
    animation: flash-border 1s infinite;
  }
  
  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
  
  .animate-bounce {
    animation: bounce 1s infinite;
  }
</style>