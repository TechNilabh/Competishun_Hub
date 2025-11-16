<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { Clock, FileText, Code } from "lucide-svelte";

  let exams: any[] = [];
  let loading = true;
  let error = "";

  onMount(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/exams/");
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      exams = data.results || data;
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Available Exams</title>
</svelte:head>

<div class="min-h-screen py-16 px-4 bg-[var(--bg)]">
  <div class="mx-auto max-w-7xl">

    <!-- Header -->
    <div class="text-center mb-14">
      <h1 class="text-5xl font-extrabold text-[var(--text-primary)] mb-3 tracking-tight">
        Available Exams
      </h1>
      <p class="text-lg text-[var(--text-secondary)]">
        Choose an exam to begin your assessment journey
      </p>
    </div>

    <!-- LOADING -->
    {#if loading}
      <div class="flex flex-col items-center justify-center py-20">
        <div class="h-12 w-12 rounded-full border-4 border-indigo-500 border-t-transparent animate-spin mb-4"></div>
        <p class="text-[var(--text-secondary)] text-lg">Loading exams...</p>
      </div>

    <!-- ERROR -->
    {:else if error}
      <div class="max-w-md mx-auto bg-red-700/20 border border-red-700 rounded-xl p-6 shadow-lg">
        <h3 class="text-red-400 font-semibold text-xl mb-2">Error Loading Exams</h3>
        <p class="text-red-300 text-sm mb-4">{error}</p>
        <button
          on:click={() => window.location.reload()}
          class="px-5 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg"
        >
          Retry
        </button>
      </div>

    <!-- NO EXAMS -->
    {:else if exams.length === 0}
      <div class="text-center py-20 opacity-80">
        <svg class="mx-auto h-24 w-24 text-gray-600 mb-6" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586l6 6V19a2 2 0 01-2 2z"/>
        </svg>

        <h3 class="text-2xl text-[var(--text-primary)] font-semibold mb-2">No Exams Available</h3>
        <p class="text-[var(--text-secondary)] mb-6 text-lg">
          No exams are available at the moment. Please check back soon.
        </p>

        <button
          on:click={() => window.location.reload()}
          class="px-6 py-3 bg-indigo-500 hover:bg-indigo-600 text-white rounded-lg font-medium"
        >
          Refresh Page
        </button>
      </div>

    <!-- EXAMS LIST -->
    {:else}
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">

        {#each exams as exam}
          <div class="rounded-2xl bg-[var(--card-bg)] border border-[var(--border)] p-6 
                      hover:border-indigo-500 hover:shadow-[0_0_20px_rgba(99,102,241,0.25)]
                      transition-all duration-300 group">

            <!-- Exam Title -->
            <h3 class="text-2xl font-bold text-[var(--text-primary)] mb-3 group-hover:text-indigo-400 transition-colors">
              {exam.title}
            </h3>

            <p class="text-[var(--text-secondary)] mb-6 line-clamp-3 text-sm leading-relaxed">
              {exam.description}
            </p>

            <!-- Exam meta info -->
            <div class="space-y-3 mb-6">
              <div class="flex items-center gap-3 text-[var(--text-secondary)]">
                <Clock size={18} class="text-indigo-400"/>
                <span class="text-sm">Duration: {exam.duration_minutes} min</span>
              </div>

              <div class="flex items-center gap-3 text-[var(--text-secondary)]">
                <FileText size={18} class="text-green-400"/>
                <span class="text-sm">Quiz: {exam.quiz_duration_minutes} min</span>
              </div>

              <div class="flex items-center gap-3 text-[var(--text-secondary)]">
                <Code size={18} class="text-purple-400"/>
                <span class="text-sm">Coding: {exam.duration_minutes - exam.quiz_duration_minutes} min</span>
              </div>
            </div>

            <!-- Start Button -->
            <button
              on:click={() => goto(`/exam/start?exam_id=${exam.id}`)}
              class="w-full px-6 py-3 bg-indigo-500 hover:bg-indigo-600
                     text-white font-semibold rounded-lg transition-all shadow group-hover:scale-[1.03]"
            >
              Start Exam
            </button>
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
