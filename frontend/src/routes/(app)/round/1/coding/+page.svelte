<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { examStore } from '$lib/stores/exam';
  import { submitCodingSubmission, submitExam, getCodingSubmissions } from '$lib/utils/quizApi';
  import { executeCode } from '$lib/utils/piston';
  import ProctorCamera from '$lib/components/exam/ProctorCamera.svelte';
  import CodeEditor from '$lib/components/exam/CodeEditor.svelte';
  import TestCasePanel from '$lib/components/exam/TestCasePanel.svelte';
  import ViolationAlert from '$lib/components/exam/ViolationAlert.svelte';
  import { Clock, Send, ChevronLeft, ChevronRight } from 'lucide-svelte';
  import type { CodingProblem, CodingSubmission } from '$lib/types/exam';
  
  let timeRemaining = 0;
  let timerInterval: any;
  let sessionId = '';
  let currentProblemIndex = 0;
  let code = '';
  let language = 'python';
  let output = '';
  let error = '';
  let isRunning = false;
  let isSubmitting = false;
  let executionTime = 0;
  let memoryUsed = 0;
  let submissions: CodingSubmission[] = [];
  
  $: session = $examStore.session;
  $: problems = $examStore.codingProblems;
  $: currentProblem = problems[currentProblemIndex];
  $: canGoPrevious = currentProblemIndex > 0;
  $: canGoNext = currentProblemIndex < problems.length - 1;
  
  function formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  
  async function handleRunCode(codeToRun: string) {
    isRunning = true;
    output = '';
    error = '';
    
    try {
      const result = await executeCode(language, codeToRun, currentProblem.sample_input);
      
      if (result.code === 0) {
        output = result.stdout || result.output;
        executionTime = result.cpu_time || 0;
        memoryUsed = Math.floor((result.memory || 0) / 1024);
      } else {
        error = result.stderr || 'Runtime error occurred';
      }
    } catch (err: any) {
      error = err.message || 'Failed to execute code';
    } finally {
      isRunning = false;
    }
  }
  
  async function handleSubmitCode() {
    if (!code.trim()) {
      alert('Please write some code before submitting');
      return;
    }
    
    if (!confirm('Submit this solution? This will be evaluated against all test cases.')) {
      return;
    }
    
    isSubmitting = true;
    
    try {
      const submission = await submitCodingSubmission({
        session: sessionId,
        problem: currentProblem.id,
        language,
        code
      });
      
      submissions = [submission, ...submissions];
      
      alert(`Submission complete!\nStatus: ${submission.status}\nScore: ${submission.score}/${currentProblem.max_marks}\nTest Cases Passed: ${submission.test_cases_passed}/${submission.total_test_cases}`);
      
      await loadSubmissions();
    } catch (err: any) {
      alert('Failed to submit code: ' + (err.message || 'Unknown error'));
    } finally {
      isSubmitting = false;
    }
  }
  
  async function loadSubmissions() {
    if (!currentProblem) return;
    
    try {
      submissions = await getCodingSubmissions(sessionId, currentProblem.id);
    } catch (error) {
      console.error('Failed to load submissions:', error);
    }
  }
  
  function navigateProblem(direction: number) {
    currentProblemIndex = Math.max(0, Math.min(problems.length - 1, currentProblemIndex + direction));
    code = '';
    output = '';
    error = '';
    loadSubmissions();
  }
  
  async function handleFinalSubmit() {
    if (!confirm('Are you sure you want to submit the entire exam? You cannot come back.')) {
      return;
    }
    
    try {
      await submitExam(sessionId);
      alert('Exam submitted successfully!');
      goto('/exam');
    } catch (error) {
      console.error('Failed to submit exam:', error);
      alert('Failed to submit exam. Please try again.');
    }
  }
  
  onMount(async () => {
    if (!session) {
      goto('/exam');
      return;
    }
    
    sessionId = session.id;
    
    const totalDuration = session.exam.duration_minutes * 60;
    const quizDuration = session.exam.quiz_duration_minutes * 60;
    timeRemaining = totalDuration - quizDuration;
    
    examStore.update(state => ({
      ...state,
      isQuizPhase: false
    }));
    
    await loadSubmissions();
    
    timerInterval = setInterval(() => {
      timeRemaining--;
      
      if (timeRemaining <= 0) {
        handleFinalSubmit();
      }
    }, 1000);
  });
  
  onDestroy(() => {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
  });
</script>

<svelte:head>
  <title>Coding Round</title>
</svelte:head>

<div class="min-h-screen bg-gray-900 flex flex-col">
  <!-- Top Bar -->
  <div class="bg-gray-800 border-b border-gray-700 px-6 py-3 sticky top-0 z-30">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-6">
        <h1 class="text-xl font-bold text-white">
          Coding Round
        </h1>
        
        <div class="flex items-center gap-2 px-4 py-2 bg-gray-900 rounded-lg">
          <Clock size={20} class="text-purple-400" />
          <span class="text-lg font-mono font-bold {timeRemaining < 300 ? 'text-red-400' : 'text-white'}">
            {formatTime(timeRemaining)}
          </span>
        </div>
        
        <div class="text-sm text-gray-400">
          Problem {currentProblemIndex + 1} of {problems.length}
        </div>
      </div>
      
      <button
        on:click={handleFinalSubmit}
        class="flex items-center gap-2 px-6 py-2 bg-green-600 hover:bg-green-500 text-white font-semibold rounded-lg transition-colors"
      >
        <Send size={18} />
        <span>Submit Exam</span>
      </button>
    </div>
  </div>
  
  {#if currentProblem}
    <div class="flex-1 flex overflow-hidden">
      <!-- Problem Description -->
      <div class="w-1/3 border-r border-gray-700 overflow-y-auto bg-gray-850">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-white">
              {currentProblem.title}
            </h2>
            <span class="px-3 py-1 text-xs rounded-full {
              currentProblem.difficulty === 'easy' ? 'bg-green-500' :
              currentProblem.difficulty === 'medium' ? 'bg-yellow-500' :
              'bg-red-500'
            } text-white font-semibold">
              {currentProblem.difficulty}
            </span>
          </div>
          
          <div class="space-y-6 text-gray-300">
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Description</h3>
              <p class="whitespace-pre-wrap">{currentProblem.description}</p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Input Format</h3>
              <p class="whitespace-pre-wrap">{currentProblem.input_format}</p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Output Format</h3>
              <p class="whitespace-pre-wrap">{currentProblem.output_format}</p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Constraints</h3>
              <p class="whitespace-pre-wrap">{currentProblem.constraints}</p>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Sample Input</h3>
              <pre class="p-3 bg-gray-900 rounded font-mono text-sm">{currentProblem.sample_input}</pre>
            </div>
            
            <div>
              <h3 class="text-lg font-semibold text-white mb-2">Sample Output</h3>
              <pre class="p-3 bg-gray-900 rounded font-mono text-sm">{currentProblem.sample_output}</pre>
            </div>
            
            <div class="bg-blue-900/30 border border-blue-700 rounded-lg p-4">
              <h3 class="text-lg font-semibold text-blue-400 mb-2">Max Score</h3>
              <p class="text-2xl font-bold text-white">{currentProblem.max_marks} points</p>
            </div>
            
            {#if submissions.length > 0}
              <div>
                <h3 class="text-lg font-semibold text-white mb-3">Your Submissions</h3>
                <div class="space-y-2">
                  {#each submissions.slice(0, 5) as submission}
                    <div class="p-3 bg-gray-900 rounded-lg border border-gray-700">
                      <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-semibold {
                          submission.status === 'accepted' ? 'text-green-400' :
                          submission.status === 'wrong_answer' ? 'text-yellow-400' :
                          'text-red-400'
                        }">
                          {submission.status.replace('_', ' ').toUpperCase()}
                        </span>
                        <span class="text-sm text-gray-400">{submission.language}</span>
                      </div>
                      <div class="text-xs text-gray-400">
                        Score: {submission.score}/{currentProblem.max_marks} |
                        Tests: {submission.test_cases_passed}/{submission.total_test_cases}
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
        </div>
      </div>
      
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Code Editor -->
        <div class="flex-1 overflow-hidden border-b border-gray-700">
          <CodeEditor
            bind:language
            bind:code
            onRun={handleRunCode}
            readOnly={isSubmitting}
          />
        </div>
        
        <div class="h-80 overflow-hidden">
          <TestCasePanel
            testCases={currentProblem.test_cases}
            {output}
            {error}
            {isRunning}
            {executionTime}
            {memoryUsed}
          />
        </div>
        
        <div class="p-4 bg-gray-800 border-t border-gray-700">
          <button
            on:click={handleSubmitCode}
            disabled={isSubmitting || !code.trim()}
            class="w-full px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-semibold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? 'Submitting...' : 'Submit Solution'}
          </button>
        </div>
      </div>
    </div>
    
    <div class="bg-gray-800 border-t border-gray-700 p-4">
      <div class="flex justify-between items-center max-w-4xl mx-auto">
        <button
          on:click={() => navigateProblem(-1)}
          disabled={!canGoPrevious}
          class="flex items-center gap-2 px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft size={20} />
          <span>Previous Problem</span>
        </button>
        
        <div class="flex gap-2">
          {#each problems as problem, index}
            <button
              on:click={() => {
                currentProblemIndex = index;
                code = '';
                output = '';
                error = '';
                loadSubmissions();
              }}
              class="w-10 h-10 rounded-lg font-semibold transition-all {
                currentProblemIndex === index
                  ? 'bg-blue-600 text-white ring-2 ring-blue-400'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }"
            >
              {index + 1}
            </button>
          {/each}
        </div>
        
        <button
          on:click={() => navigateProblem(1)}
          disabled={!canGoNext}
          class="flex items-center gap-2 px-6 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>Next Problem</span>
          <ChevronRight size={20} />
        </button>
      </div>
    </div>
  {/if}
  
  <ProctorCamera {sessionId} />
  <ViolationAlert />
</div>