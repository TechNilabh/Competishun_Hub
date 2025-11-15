<script lang="ts">
  import { examStore, currentQuestion, questionStatuses } from '$lib/stores/exam';
  import { submitQuizAnswer } from '$lib/utils/quizApi';
  import { ChevronLeft, ChevronRight, Grid3x3 } from 'lucide-svelte';
  import QuestionGrid from './QuestionGrid.svelte';
  
  export let sessionId: string;
  
  let selectedAnswer = '';
  let showGrid = false;
  let isSubmitting = false;
  
  $: question = $currentQuestion;
  $: currentIndex = $examStore.currentQuestionIndex;
  $: totalQuestions = $examStore.quizQuestions.length;
  $: canGoPrevious = currentIndex > 0;
  $: canGoNext = currentIndex < totalQuestions - 1;
  
  $: if (question) {
    const savedAnswer = $examStore.quizAnswers.get(question.id);
    selectedAnswer = savedAnswer?.selected_answer || '';
  }
  
  async function handleAnswerSelect(answer: string) {
    if (isSubmitting || !question) return;
    
    selectedAnswer = answer;
    isSubmitting = true;
    
    try {
      const result = await submitQuizAnswer(sessionId, question.id, answer);
      
      examStore.update(state => {
        const newAnswers = new Map(state.quizAnswers);
        newAnswers.set(question.id, result);
        return { ...state, quizAnswers: newAnswers };
      });
    } catch (error) {
      console.error('Failed to submit answer:', error);
    } finally {
      isSubmitting = false;
    }
  }
  
  function navigateQuestion(direction: number) {
    examStore.update(state => ({
      ...state,
      currentQuestionIndex: Math.max(0, Math.min(totalQuestions - 1, currentIndex + direction))
    }));
  }
  
  function clearAnswer() {
    selectedAnswer = '';
  }
</script>

<div class="quiz-interface h-full flex flex-col bg-gray-900">
  {#if question}
    <!-- Question Content -->
    <div class="flex-1 overflow-y-auto p-6">
      <div class="max-w-4xl mx-auto">
        <!-- Question Header -->
        <div class="mb-6 flex justify-between items-center">
          <div>
            <span class="text-sm font-semibold text-blue-400">
              Question {currentIndex + 1} of {totalQuestions}
            </span>
            <span class="ml-4 text-sm text-gray-400">
              Marks: {question.marks}
            </span>
            {#if question.difficulty}
              <span class="ml-4 px-2 py-1 text-xs rounded-full {
                question.difficulty === 'easy' ? 'bg-green-500' :
                question.difficulty === 'medium' ? 'bg-yellow-500' :
                'bg-red-500'
              } text-white">
                {question.difficulty}
              </span>
            {/if}
          </div>
          
         <button
  on:click={() => showGrid = true}
  class="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-lg transition-colors"
>
  <Grid3x3 size={18} />
  <span>Question Grid</span>
</button>
        </div>
        
        <div class="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <h2 class="text-xl text-white leading-relaxed">
            {@html question.question_text}
          </h2>
        </div>
        
        <div class="space-y-3">
          {#each [
            { key: 'A', value: question.option_a },
            { key: 'B', value: question.option_b },
            { key: 'C', value: question.option_c },
            { key: 'D', value: question.option_d }
          ] as option}
            {#if option.value}
              <button
                on:click={() => handleAnswerSelect(option.key)}
                disabled={isSubmitting}
                class="w-full text-left p-4 rounded-lg border-2 transition-all duration-200 {
                  selectedAnswer === option.key
                    ? 'bg-blue-600 border-blue-400 text-white shadow-lg shadow-blue-500/50'
                    : 'bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600 hover:bg-gray-750'
                } disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <div class="flex items-start gap-3">
                  <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold {
                    selectedAnswer === option.key ? 'bg-white text-blue-600' : 'bg-gray-700 text-white'
                  }">
                    {option.key}
                  </div>
                  <div class="flex-1 pt-1">
                    {@html option.value}
                  </div>
                </div>
              </button>
            {/if}
          {/each}
        </div>
        
        {#if selectedAnswer}
          <button
            on:click={clearAnswer}
            class="mt-4 px-4 py-2 text-sm text-red-400 hover:text-red-300 transition-colors"
          >
            Clear Answer
          </button>
        {/if}
      </div>
    </div>
    
    <div class="border-t border-gray-700 p-4 bg-gray-800">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <button
          on:click={() => navigateQuestion(-1)}
          disabled={!canGoPrevious}
          class="flex items-center gap-2 px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ChevronLeft size={20} />
          <span>Previous</span>
        </button>
        
        <div class="text-center">
          <div class="text-sm text-gray-400">
            {#if selectedAnswer}
              <span class="text-green-400">✓ Answer saved</span>
            {:else}
              <span>No answer selected</span>
            {/if}
          </div>
        </div>
        
        <button
          on:click={() => navigateQuestion(1)}
          disabled={!canGoNext}
          class="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span>Next</span>
          <ChevronRight size={20} />
        </button>
      </div>
    </div>
  {:else}
    <div class="flex items-center justify-center h-full">
      <p class="text-gray-400">No question available</p>
    </div>
  {/if}
</div>

<QuestionGrid
  bind:isOpen={showGrid}
  on:close={() => showGrid = false}
/>