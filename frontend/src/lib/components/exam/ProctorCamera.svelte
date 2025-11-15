<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { proctoringStore } from '$lib/stores/proctoring';
  import { Camera, Mic, MicOff, CameraOff, AlertTriangle } from 'lucide-svelte';

  export let sessionId: string;
  
  let videoElement: HTMLVideoElement;
  let stream: MediaStream | null = null;
  let isCameraActive = false;
  let isMicActive = false;
  
  $: violations = $proctoringStore.violations;
  $: faceDetected = $proctoringStore.faceDetected;

  onMount(async () => {
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 320, height: 240 },
        audio: true
      });
      
      if (videoElement) {
        videoElement.srcObject = stream;
      }
      
      isCameraActive = true;
      isMicActive = true;
      
      proctoringStore.update(state => ({
        ...state,
        isCameraActive: true,
        isMicActive: true
      }));
    } catch (error) {
      console.error('Failed to access camera/microphone:', error);
    }
  });

  onDestroy(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
  });
</script>

<div class="proctor-camera fixed top-4 right-4 z-50">
  <div class="relative bg-gray-900 rounded-lg overflow-hidden shadow-2xl border-2 border-gray-700">
    <!-- Video Preview -->
    <video
      bind:this={videoElement}
      autoplay
      muted
      class="w-48 h-36 object-cover"
    />
    
    <div class="absolute top-2 left-2 flex gap-2">
      {#if isCameraActive}
        <div class="flex items-center gap-1 bg-green-500 px-2 py-1 rounded-full text-xs text-white animate-pulse">
          <Camera size={12} />
          <span>REC</span>
        </div>
      {:else}
        <div class="flex items-center gap-1 bg-red-500 px-2 py-1 rounded-full text-xs text-white">
          <CameraOff size={12} />
        </div>
      {/if}
      
      {#if isMicActive}
        <div class="flex items-center gap-1 bg-green-500 px-2 py-1 rounded-full text-xs text-white animate-pulse">
          <Mic size={12} />
        </div>
      {:else}
        <div class="flex items-center gap-1 bg-red-500 px-2 py-1 rounded-full text-xs text-white">
          <MicOff size={12} />
        </div>
      {/if}
    </div>
    
    {#if violations > 0}
      <div class="absolute top-2 right-2 flex items-center gap-1 bg-red-500 px-2 py-1 rounded-full text-xs text-white font-bold">
        <AlertTriangle size={12} />
        <span>{violations}/3</span>
      </div>
    {/if}
    
    {#if !faceDetected}
      <div class="absolute bottom-2 left-2 right-2 bg-yellow-500 px-2 py-1 rounded text-xs text-center font-semibold">
        ⚠️ Face not detected
      </div>
    {/if}
  </div>
</div>

<style>
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.7;
    }
  }
  
  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
</style>