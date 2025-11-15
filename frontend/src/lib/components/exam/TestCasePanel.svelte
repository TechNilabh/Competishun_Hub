<script lang="ts">
  import { Check, X, Loader } from 'lucide-svelte';
  import type { TestCase } from '$lib/types/exam';
  
  export let testCases: TestCase[] = [];
  export let output: string = '';
  export let error: string = '';
  export let isRunning: boolean = false;
  export let executionTime: number = 0;
  export let memoryUsed: number = 0;
  
  let activeTab: 'input' | 'output' | 'testcases' = 'output';
  
  $: sampleTestCases = testCases.filter(tc => tc.is_sample);
</script>

<div class="test-case-panel h-full flex flex-col bg-gray-900 border border-gray-700 rounded-lg overflow-hidden">
  <!-- Tabs -->
  <div class="flex border-b border-gray-700 bg-gray-800">
    <button
      on:click={() => activeTab = 'output'}
      class="px-4 py-2 text-sm font-medium transition-colors {
        activeTab === 'output'
          ? 'bg-gray-900 text-white border-b-2 border-blue-500'
          : 'text-gray-400 hover:text-white'
      }"
    >
      Output
    </button>
    <button
      on:click={() => activeTab = 'testcases'}
      class="px-4 py-2 text-sm font-medium transition-colors {
        activeTab === 'testcases'
          ? 'bg-gray-900 text-white border-b-2 border-blue-500'
          : 'text-gray-400 hover:text-white'
      }"
    >
      Test Cases ({sampleTestCases.length})
    </button>
  </div>
  
  <div class="flex-1 overflow-y-auto p-4">
    {#if isRunning}
      <div class="flex items-center justify-center h-full">
        <div class="text-center">
          <Loader class="animate-spin mx-auto mb-2 text-blue-500" size={32} />
          <p class="text-gray-400">Running code...</p>
        </div>
      </div>
    {:else if activeTab === 'output'}
      {#if error}
        <div class="bg-red-900/30 border border-red-700 rounded p-4">
          <div class="flex items-center gap-2 mb-2">
            <X class="text-red-500" size={20} />
            <h3 class="font-semibold text-red-400">Error</h3>
          </div>
          <pre class="text-sm text-red-300 font-mono whitespace-pre-wrap">{error}</pre>
        </div>
      {:else if output}
        <div class="bg-gray-800 rounded p-4">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <Check class="text-green-500" size={20} />
              <h3 class="font-semibold text-green-400">Output</h3>
            </div>
            {#if executionTime > 0}
              <div class="text-xs text-gray-400">
                {executionTime}ms | {memoryUsed}KB
              </div>
            {/if}
          </div>
          <pre class="text-sm text-gray-300 font-mono whitespace-pre-wrap">{output}</pre>
        </div>
      {:else}
        <div class="flex items-center justify-center h-full text-gray-500">
          <p>Run your code to see output</p>
        </div>
      {/if}
    {:else if activeTab === 'testcases'}
      {#if sampleTestCases.length > 0}
        <div class="space-y-4">
          {#each sampleTestCases as testCase, index}
            <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
              <h4 class="font-semibold text-white mb-3">
                Sample Test Case {index + 1}
              </h4>
              
              <div class="space-y-3">
                <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase">Input</label>
                  <pre class="mt-1 p-2 bg-gray-900 rounded text-sm text-gray-300 font-mono whitespace-pre-wrap">{testCase.input_data}</pre>
                </div>
                
                <div>
                  <label class="text-xs font-semibold text-gray-400 uppercase">Expected Output</label>
                  <pre class="mt-1 p-2 bg-gray-900 rounded text-sm text-gray-300 font-mono whitespace-pre-wrap">{testCase.expected_output}</pre>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {:else}
        <div class="flex items-center justify-center h-full text-gray-500">
          <p>No sample test cases available</p>
        </div>
      {/if}
    {/if}
  </div>
</div>

<style>
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>