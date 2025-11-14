<script lang="ts">
  import { onMount, createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let monaco: any;
  export let code: string = "";
  export let language: string = "plaintext";
  let editor: any;
  let editorEl: any;

  onMount(async () => {
    monaco = await import("monaco-editor");

    editor = monaco.editor.create(editorEl, {
      value: code,
      language,
      theme: "vs-dark",
      minimap: { enabled: false },
      fontSize: 15
    });

    editor.onDidChangeModelContent(() => {
      const value = editor.getValue();
	  console.debug("[Editor] dispatch update:code", value.slice(0, 200));
      dispatch("update:code", value);   
    });
  });

  $: if (editor && monaco) {
    monaco.editor.setModelLanguage(editor.getModel(), language);
  }

  $: if (editor && code !== editor.getValue()) {
	console.debug("[Editor] parent changed code — setting editor value");
    editor.setValue(code); 
  }
</script>

<div bind:this={editorEl} class="h-[600px]"></div>
