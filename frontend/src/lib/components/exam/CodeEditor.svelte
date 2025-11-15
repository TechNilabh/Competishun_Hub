<script lang="ts">
  import { onMount } from 'svelte';
  import { Play, RotateCcw } from 'lucide-svelte';
  
  export let language: string = 'python';
  export let code: string = '';
  export let onRun: (code: string) => void;
  export let readOnly: boolean = false;
  
  let textareaElement: HTMLTextAreaElement;
  
  const languageTemplates: Record<string, string> = {
    python: '# Write your Python code here\n\ndef main():\n    pass\n\nif __name__ == "__main__":\n    main()',
    c: '#include <stdio.h>\n\nint main() {\n    // Write your C code here\n    \n    return 0;\n}',
    cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your C++ code here\n    \n    return 0;\n}',
    java: 'public class Main {\n    public static void main(String[] args) {\n        // Write your Java code here\n        \n    }\n}',
    javascript: '// Write your JavaScript code here\n\nfunction main() {\n    \n}\n\nmain();',
  };
  
  function resetCode() {
    code = languageTemplates[language] || '';
  }
  
  function handleKeyDown(e: KeyboardEvent) {
    
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = textareaElement.selectionStart;
      const end = textareaElement.selectionEnd;
      code = code.substring(0, start) + '    ' + code.substring(end);
      
      
      setTimeout(() => {
        textareaElement.selectionStart = textareaElement.selectionEnd = start + 4;
      }, 0);
    }
  }
  
  onMount(() => {
    if (!code) {
      resetCode();
    }
  });
</script>

<div class="code-editor h-full flex flex-col bg-gray-900 border border-gray-700 rounded-lg overflow-hidden">
  <!-- Editor Header -->
  <div class="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
    <div class="flex items-center gap-4">
      <span class="text-sm font-semibold text-gray-300">Code Editor</span>
      <select
        bind:value={language}
        disabled={readOnly}
        class="px-3 py-1 bg-gray-700 text-white text-sm rounded border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="python">Python</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
        <option value="java">Java</option>
        <option value="javascript">JavaScript</option>
      </select>
    </div>
    
    <div class="flex items-center gap-2">
      <button
        on:click={resetCode}
        disabled={readOnly}
        class="flex items-center gap-2 px-3 py-1 text-sm bg-gray-700 hover:bg-gray-600 text-white rounded transition-colors disabled:opacity-50"
        title="Reset to template"
      >
        <RotateCcw size={14} />
        <span>Reset</span>
      </button>
      
      <button
        on:click={() => onRun(code)}
        disabled={readOnly}
        class="flex items-center gap-2 px-4 py-1 text-sm bg-green-600 hover:bg-green-500 text-white rounded transition-colors disabled:opacity-50"
      >
        <Play size={14} />
        <span>Run Code</span>
      </button>
    </div>
  </div>
  
  <div class="flex-1 relative">
    <textarea
      bind:this={textareaElement}
      bind:value={code}
      on:keydown={handleKeyDown}
      {readOnly}
      class="w-full h-full p-4 bg-gray-900 text-gray-100 font-mono text-sm resize-none focus:outline-none"
      style="tab-size: 4;"
      spellcheck="false"
      placeholder="Write your code here..."
    />
    
  </div>
</div>

<style>
  textarea {
    line-height: 1.6;
  }
  
  textarea::placeholder {
    color: #6b7280;
  }
</style>