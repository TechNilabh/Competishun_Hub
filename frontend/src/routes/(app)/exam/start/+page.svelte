<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { Camera, Mic, AlertTriangle, CheckCircle } from 'lucide-svelte';
  import { examStore } from '$lib/stores/exam';
  
  let examId = '';
  let cameraPermission = false;
  let micPermission = false;
  let loading = false;
  let error = '';
  let stream: MediaStream | null = null;
  let videoElement: HTMLVideoElement;
  let permissionError = '';
  let showVideo = false;
  
  onMount(() => {
    examId = $page.url.searchParams.get('exam_id') || '';
    if (!examId) {
      error = 'No exam ID provided';
      setTimeout(() => goto('/exam'), 2000);
    }
  });
  
  async function requestPermissions() {
    permissionError = '';
    error = '';
    
    try {
      console.log('Requesting permissions...');
      
      stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: true
      });
      
      console.log('Permissions granted, stream:', stream);
      
      // Wait for video element to be ready
      await new Promise(resolve => setTimeout(resolve, 100));
      
      if (videoElement && stream) {
        videoElement.srcObject = stream;
        await videoElement.play();
        showVideo = true;
        console.log('Video playing');
      }
      
      cameraPermission = true;
      micPermission = true;
      
    } catch (err: any) {
      console.error('Permission error:', err);
      permissionError = `Failed to access camera/microphone: ${err.message}`;
      cameraPermission = false;
      micPermission = false;
    }
  }
  
  async function startExam() {
    if (!cameraPermission || !micPermission) {
      error = 'Please grant camera and microphone permissions';
      return;
    }
    
    loading = true;
    error = '';
    
    try {
      console.log('Step 1: Creating exam session...');
      
      const sessionResponse = await fetch('http://localhost:8000/api/exam-sessions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          exam: examId,
          is_camera_enabled: cameraPermission,
          is_mic_enabled: micPermission,
          is_screen_shared: false
        }),
      });
      
      if (!sessionResponse.ok) {
        const errorText = await sessionResponse.text();
        console.error('Session creation failed:', errorText);
        throw new Error('Failed to create exam session');
      }
      
      const session = await sessionResponse.json();
      console.log('Step 2: Session created:', session);
      
      // Fetch questions
      console.log('Step 3: Fetching questions...');
      const questionsResponse = await fetch(`http://localhost:8000/api/exams/${examId}/questions/`);
      
      if (!questionsResponse.ok) {
        throw new Error('Failed to fetch questions');
      }
      
      const questions = await questionsResponse.json();
      console.log('Step 4: Questions loaded:', questions);
      
      // Initialize exam store
      examStore.set({
        session,
        quizQuestions: questions.quiz_questions || [],
        codingProblems: questions.coding_problems || [],
        quizAnswers: new Map(),
        currentQuestionIndex: 0,
        timeRemaining: session.exam.duration_minutes * 60,
        isQuizPhase: true
      });
      
      // Start session
      console.log('Step 5: Starting session...');
      const startResponse = await fetch(`http://localhost:8000/api/exam-sessions/${session.id}/start/`, {
        method: 'POST',
      });
      
      if (!startResponse.ok) {
        throw new Error('Failed to start exam session');
      }
      
      console.log('Step 6: Navigating to quiz...');
      await goto('/exam/quiz');
      
    } catch (err: any) {
      console.error('Start exam error:', err);
      error = err.message || 'Failed to start exam';
    } finally {
      loading = false;
    }
  }
  
  onDestroy(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
  });
</script>

<svelte:head>
  <title>Start Exam - Permission Setup</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center p-4">
  <div class="max-w-4xl w-full">
    <div class="bg-gray-800 rounded-2xl shadow-2xl overflow-hidden border border-gray-700">
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-purple-600 p-6">
        <h1 class="text-3xl font-bold text-white text-center">
          Exam Setup & Permissions
        </h1>
        <p class="text-center text-blue-100 mt-2">
          Please grant the required permissions to continue
        </p>
      </div>
      
      <div class="p-8">
        <!-- Camera Preview -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-white mb-3">Camera Preview</h3>
          <div class="relative bg-gray-900 rounded-lg overflow-hidden aspect-video max-w-md mx-auto border-2 border-gray-700">
            {#if showVideo}
              <video
                bind:this={videoElement}
                autoplay
                playsinline
                muted
                class="w-full h-full object-cover"
              />
            {:else}
              <div class="w-full h-full flex items-center justify-center text-gray-500">
                <div class="text-center">
                  <Camera size={48} class="mx-auto mb-2" />
                  <p>Camera preview will appear here</p>
                </div>
              </div>
            {/if}
          </div>
        </div>
        
        <!-- Permissions List -->
        <div class="space-y-4 mb-8">
          <div class="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
            <div class="flex items-center gap-3">
              <Camera size={24} class="text-blue-400" />
              <div>
                <h3 class="font-semibold text-white">Camera Access</h3>
                <p class="text-sm text-gray-400">Required for proctoring</p>
              </div>
            </div>
            {#if cameraPermission}
              <CheckCircle class="text-green-500" size={24} />
            {:else}
              <AlertTriangle class="text-yellow-500" size={24} />
            {/if}
          </div>
          
          <div class="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
            <div class="flex items-center gap-3">
              <Mic size={24} class="text-green-400" />
              <div>
                <h3 class="font-semibold text-white">Microphone Access</h3>
                <p class="text-sm text-gray-400">Required for audio monitoring</p>
              </div>
            </div>
            {#if micPermission}
              <CheckCircle class="text-green-500" size={24} />
            {:else}
              <AlertTriangle class="text-yellow-500" size={24} />
            {/if}
          </div>
        </div>
        
        <!-- Instructions -->
        <div class="bg-yellow-900/30 border border-yellow-700 rounded-lg p-4 mb-6">
          <h3 class="font-semibold text-yellow-400 mb-2 flex items-center gap-2">
            <AlertTriangle size={20} />
            Important Instructions
          </h3>
          <ul class="text-sm text-yellow-200 space-y-2">
            <li>• Ensure you are in a well-lit room</li>
            <li>• Stay alone during the exam</li>
            <li>• Keep your face visible at all times</li>
            <li>• Do not switch tabs or minimize the window</li>
            <li>• Violations will be logged (3 violations = auto-submit)</li>
          </ul>
        </div>
        
        <!-- Permission Error -->
        {#if permissionError}
          <div class="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-6">
            <p class="text-red-400 text-sm">{permissionError}</p>
          </div>
        {/if}
        
        <!-- Error Message -->
        {#if error}
          <div class="bg-red-900/30 border border-red-700 rounded-lg p-4 mb-6">
            <p class="text-red-400 text-sm">{error}</p>
          </div>
        {/if}
        
        <!-- Action Buttons -->
        <div class="flex gap-4">
          {#if !cameraPermission || !micPermission}
            <button
              on:click={requestPermissions}
              disabled={loading}
              class="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Grant Permissions
            </button>
          {:else}
            <button
              on:click={startExam}
              disabled={loading}
              class="flex-1 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-semibold rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
            >
              {loading ? 'Starting Exam...' : 'Start Exam Now'}
            </button>
          {/if}
          
          <button
            on:click={() => goto('/exam')}
            disabled={loading}
            class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</div>