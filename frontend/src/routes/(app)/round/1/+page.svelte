<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { Clock, FileText, Code } from 'lucide-svelte';
  
  let exams: any[] = [];
  let loading = true;
  let error = '';
  
  onMount(async () => {
    try {
      console.log('Fetching exams from API...');
      const response = await fetch('http://localhost:8000/api/exams/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Django REST framework returns paginated data with 'results' key
      exams = data.results || data;
      
      console.log('Exams loaded:', exams);
    } catch (err: any) {
      console.error('Failed to fetch exams:', err);
      error = err.message;
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Available Exams</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 py-12 px-4">
  <div class="container mx-auto max-w-7xl">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-5xl font-bold text-white mb-4">
        Available Exams
      </h1>
      <p class="text-xl text-gray-400">
        Choose an exam to start your assessment
      </p>
    </div>
    
    {#if loading}
      <div class="flex flex-col items-center justify-center py-20">
        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500 mb-4"></div>
        <p class="text-gray-400">Loading exams...</p>
      </div>
    
    {:else if error}
      <div class="max-w-md mx-auto bg-red-900/20 border border-red-700 rounded-lg p-6">
        <h3 class="text-red-400 font-semibold mb-2">Error Loading Exams</h3>
        <p class="text-red-300 text-sm mb-4">{error}</p>
        <button
          on:click={() => window.location.reload()}
          class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded transition-colors"
        >
          Retry
        </button>
      </div>
    
    {:else if exams.length === 0}
      <div class="text-center py-20">
        <div class="mb-6">
          <svg class="mx-auto h-24 w-24 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-white mb-2">No Exams Available</h3>
        <p class="text-gray-400 mb-6">There are currently no exams available. Please check back later.</p>
        <button
          on:click={() => window.location.reload()}
          class="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors"
        >
          Refresh
        </button>
      </div>
    
    {:else}
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {#each exams as exam}
          <div class="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 hover:border-blue-500 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/20">
            <div class="p-6">
              <h3 class="text-2xl font-bold text-white mb-3">
                {exam.title}
              </h3>
              
              <p class="text-gray-400 mb-6 line-clamp-3">
                {exam.description}
              </p>
              
              <div class="space-y-3 mb-6">
                <div class="flex items-center gap-3 text-gray-300">
                  <Clock size={18} class="text-blue-400 flex-shrink-0" />
                  <span class="text-sm">Duration: {exam.duration_minutes} minutes</span>
                </div>
                
                <div class="flex items-center gap-3 text-gray-300">
                  <FileText size={18} class="text-green-400 flex-shrink-0" />
                  <span class="text-sm">Quiz: {exam.quiz_duration_minutes} minutes</span>
                </div>
                
                <div class="flex items-center gap-3 text-gray-300">
                  <Code size={18} class="text-purple-400 flex-shrink-0" />
                  <span class="text-sm">Coding: {exam.duration_minutes - exam.quiz_duration_minutes} minutes</span>
                </div>
              </div>
              
              <button
                on:click={() => goto(`/exam/start?exam_id=${exam.id}`)}
                class="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105"
              >
                Start Exam
              </button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>