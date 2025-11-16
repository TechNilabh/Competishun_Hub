<script lang="ts">
  import { examStore, questionStatuses } from '$lib/stores/exam';
  import { createEventDispatcher } from 'svelte';
  import { X, CheckCircle, Circle, Dot } from 'lucide-svelte';

  export let isOpen = false;
  
  const dispatch = createEventDispatcher();
  
  $: questions = $examStore.quizQuestions;
  $: statuses = $questionStatuses;
  $: currentIndex = $examStore.currentQuestionIndex;
  $: answers = $examStore.quizAnswers;
  
  function jumpToQuestion(index: number) {
    examStore.update(state => ({
      ...state,
      currentQuestionIndex: index
    }));
    dispatch('close');
  }
  
  function getQuestionStatus(questionId: string) {
    const answer = answers.get(questionId);
    return {
      attempted: answer && answer.selected_answer,
      color: answer && answer.selected_answer ? 'bg-gradient-to-br from-green-500 to-emerald-600' : 'bg-gradient-to-br from-gray-600 to-gray-700'
    };
  }
</script>

{#if isOpen}
  <div 
    class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
    on:click={() => dispatch('close')}
    on:keydown={(e) => e.key === 'Escape' && dispatch('close')}
  >
    <div 
      class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-2xl max-w-3xl w-full max-h-[85vh] overflow-hidden border-2 border-gray-700"
      on:click|stopPropagation
    >
      <div class="flex justify-between items-center p-6 border-b-2 border-gray-700 bg-gradient-to-r from-blue-900/50 to-purple-900/50">
        <div>
          <h2 class="text-2xl font-bold text-white flex items-center gap-2">
            <Dot size={32} class="text-blue-400 animate-pulse" />
            Question Navigator
          </h2>
          <p class="text-gray-400 text-sm mt-1">Jump to any question</p>
        </div>
        <button
          on:click={() => dispatch('close')}
          class="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-700 rounded-lg"
        >
          <X size={28} />
        </button>
      </div>
      
      <div class="p-6 border-b-2 border-gray-700 bg-gray-800/50">
        <div class="flex flex-wrap gap-6 justify-center text-sm">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg shadow-lg"></div>
            <div>
              <div class="font-semibold text-white">Attempted</div>
              <div class="text-xs text-gray-400">Answer saved</div>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-gray-600 to-gray-700 rounded-lg shadow-lg"></div>
            <div>
              <div class="font-semibold text-white">Unattempted</div>
              <div class="text-xs text-gray-400">Not answered</div>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg shadow-lg ring-4 ring-blue-400/50"></div>
            <div>
              <div class="font-semibold text-white">Current</div>
              <div class="text-xs text-gray-400">Active question</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="p-6 overflow-y-auto max-h-[50vh]">
        <div class="grid grid-cols-5 sm:grid-cols-8 gap-3">
          {#each questions as question, index}
            {@const status = getQuestionStatus(question.id)}
            {@const isCurrent = currentIndex === index}
            
            <button
              on:click={() => jumpToQuestion(index)}
              class="group relative aspect-square rounded-xl font-bold text-white transition-all duration-300 transform hover:scale-110 hover:shadow-2xl {status.color} {isCurrent ? 'ring-4 ring-blue-400 scale-110' : ''}"
            >
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-lg">{index + 1}</span>
              </div>
              
              {#if status.attempted}
                <div class="absolute -top-1 -right-1 bg-white rounded-full p-0.5">
                  <CheckCircle size={14} class="text-green-600" />
                </div>
              {/if}
              
              {#if isCurrent}
                <div class="absolute -bottom-1 left-1/2 transform -translate-x-1/2">
                  <div class="w-2 h-2 bg-blue-400 rounded-full animate-ping"></div>
                  <div class="w-2 h-2 bg-blue-400 rounded-full absolute top-0"></div>
                </div>
              {/if}
              
              <div class="absolute inset-0 bg-white/0 group-hover:bg-white/10 rounded-xl transition-all"></div>
            </button>
          {/each}
        </div>
      </div>
      
      <!-- Footer with Stats -->
      <div class="p-6 border-t-2 border-gray-700 bg-gray-800/50">
        <div class="flex justify-around text-center">
          <div>
            <div class="text-2xl font-bold text-green-400">{Array.from(answers.values()).filter(a => a.selected_answer).length}</div>
            <div class="text-xs text-gray-400">Attempted</div>
          </div>
          <div class="w-px bg-gray-700"></div>
          <div>
            <div class="text-2xl font-bold text-yellow-400">{questions.length - Array.from(answers.values()).filter(a => a.selected_answer).length}</div>
            <div class="text-xs text-gray-400">Remaining</div>
          </div>
          <div class="w-px bg-gray-700"></div>
          <div>
            <div class="text-2xl font-bold text-white">{questions.length}</div>
            <div class="text-xs text-gray-400">Total</div>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  @keyframes ping {
    75%, 100% {
      transform: scale(2);
      opacity: 0;
    }
  }
  
  .animate-ping {
    animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
  }
</style>