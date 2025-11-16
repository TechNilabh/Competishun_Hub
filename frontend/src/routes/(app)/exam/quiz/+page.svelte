<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { examStore } from '$lib/stores/exam';
  import { proctoringStore } from '$lib/stores/proctoring';
  import { initializeProctoring, cleanupProctoring } from '$lib/utils/proctoring';
  import ProctorCamera from '$lib/components/exam/ProctorCamera.svelte';
  import QuizInterface from '$lib/components/exam/QuizInterface.svelte';
  import ProgressBar from '$lib/components/exam/ProgressBar.svelte';
  import ViolationAlert from '$lib/components/exam/ViolationAlert.svelte';
  import { Clock, LogOut, Code } from 'lucide-svelte';
  
  let timeRemaining = 0;
  let timerInterval: any;
  let sessionId = '';
  let quizDuration = 0;
  let isSubmitting = false;
  
  $: session = $examStore.session;
  $: violations = $proctoringStore.violations;
  $: codingProblems = $examStore.codingProblems;
  $: hasCodingRound = codingProblems && codingProblems.length > 0;
  
  function formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  async function handleSubmit() {
    const message = hasCodingRound 
      ? 'Submit quiz and proceed to coding round?' 
      : 'Submit the entire exam? You cannot come back.';
      
    if (!confirm(message)) {
      return;
    }
    
    isSubmitting = true;
    
    try {
      if (hasCodingRound) {
        cleanupProctoring();
        examStore.update(state => ({
          ...state,
          isQuizPhase: false
        }));
        goto('/exam/coding');
      } else {
        await fetch(`http://localhost:8000/api/exam-sessions/${sessionId}/submit/`, {
          method: 'POST'
        });
        cleanupProctoring();
        alert('Exam submitted successfully!');
        goto('/exam');
      }
    } catch (error) {
      console.error('Failed to submit:', error);
      alert('Failed to submit. Please try again.');
      isSubmitting = false;
    }
  }
  
  onMount(async () => {
    if (!session) {
      goto('/exam');
      return;
    }
    
    sessionId = session.id;
    quizDuration = session.exam.quiz_duration_minutes * 60;
    timeRemaining = quizDuration;
    
    try {
      await initializeProctoring(sessionId);
    } catch (error) {
      console.error('Failed to initialize proctoring:', error);
    }
   
    timerInterval = setInterval(() => {
      timeRemaining--;
      
      examStore.update(state => ({
        ...state,
        timeRemaining
      }));
      
      // Auto-submit when time runs out
      if (timeRemaining <= 0) {
        handleSubmit();
      }
    }, 1000);
    
    const unsubscribe = proctoringStore.subscribe(state => {
      if (state.violations >= 3) {
        alert('You have been disqualified due to multiple violations.');
        handleSubmit();
      }
    });
    
    return () => {
      unsubscribe();
    };
  });
  
  onDestroy(() => {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
    cleanupProctoring();
  });
</script>

<svelte:head>
  <title>Quiz Round</title>
</svelte:head>

<div class="min-h-screen bg-gray-900 flex flex-col pt-16">
  <!-- Top Bar -->
  <div class="fixed top-0 left-0 right-0 bg-gray-800 border-b border-gray-700 px-6 py-3 z-30 mt-16">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-6">
        <h1 class="text-xl font-bold text-white">
          Quiz Round
        </h1>
        
        <div class="flex items-center gap-2 px-4 py-2 bg-gray-900 rounded-lg">
          <Clock size={20} class="text-blue-400" />
          <span class="text-lg font-mono font-bold {timeRemaining < 300 ? 'text-red-400 animate-pulse' : 'text-white'}">
            {formatTime(timeRemaining)}
          </span>
        </div>
      </div>
      
      <div class="flex gap-3">
        {#if hasCodingRound}
          <button
            on:click={handleSubmit}
            disabled={isSubmitting}
            class="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
          >
            <Code size={18} />
            <span>{isSubmitting ? 'Loading...' : 'Proceed to Coding'}</span>
          </button>
        {/if}
        
        <button
          on:click={handleSubmit}
          disabled={isSubmitting}
          class="flex items-center gap-2 px-6 py-2 bg-red-600 hover:bg-red-500 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
        >
          <LogOut size={18} />
          <span>{isSubmitting ? 'Submitting...' : 'Submit Quiz'}</span>
        </button>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="mt-3">
      <ProgressBar />
    </div>
  </div>
  
  <div class="flex-1 flex overflow-hidden mt-32">
    <!-- Main Quiz Area -->
    <div class="flex-1 overflow-hidden">
      <QuizInterface {sessionId} />
    </div>
  </div>
  
  <ProctorCamera {sessionId} />
  <ViolationAlert />
</div>

<style>
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  .animate-pulse {
    animation: pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
</style>