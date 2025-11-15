import { logProctoringViolation } from './quizApi';
import type { FaceDetectionResult as FaceDetectionResultData } from '../types/mediapipe';

let audioDetectionInterval: ReturnType<typeof setInterval> | null = null;
let tabSwitchListener: (() => void) | null = null;


interface FaceDetectionWrapper {
  setOptions(options: { model: 'short' | 'full'; minDetectionConfidence: number }): void;
  onResults(listener: (results: unknown) => void): void; // receive unknown and narrow below
  send(input: { image: HTMLVideoElement }): Promise<void>;
}

interface CameraWrapper {
  start(): void;
  stop?(): void;
}

export async function initializeProctoring(sessionId: string): Promise<void> {
  try {
    await initFaceDetection(sessionId);
    await initAudioDetection(sessionId);
    initTabSwitchDetection(sessionId);
  } catch (error) {
    console.error('Failed to initialize proctoring:', error);
    throw error;
  }
}

async function initFaceDetection(sessionId: string): Promise<void> {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    });

    const video = document.createElement('video');
    video.srcObject = stream;
    video.autoplay = true;
    video.muted = true;

    const { FaceDetection: FaceDetectionClass } = await import('@mediapipe/face_detection');
    const { Camera: CameraClass } = await import('@mediapipe/camera_utils');

    const faceDetection = new (FaceDetectionClass as unknown as new (cfg: { locateFile: (f: string) => string }) => FaceDetectionWrapper)({
      locateFile: (file: string) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`
    });

    faceDetection.setOptions({
      model: 'short',
      minDetectionConfidence: 0.5
    });

    let noFaceCount = 0;
    let multipleFaceCount = 0;

    faceDetection.onResults((results: unknown) => {
      const mpResults = results as FaceDetectionResultData;
      const faces = mpResults.detections?.length ?? 0;

      if (faces === 0) {
        noFaceCount++;
        if (noFaceCount > 5) {
          logProctoringViolation(sessionId, 'no_face', 'No face detected');
          noFaceCount = 0;
        }
      } else {
        noFaceCount = 0;
      }

      if (faces > 1) {
        multipleFaceCount++;
        if (multipleFaceCount > 3) {
          logProctoringViolation(sessionId, 'multiple_faces', `${faces} faces detected`);
          multipleFaceCount = 0;
        }
      } else {
        multipleFaceCount = 0;
      }
    });

    const camera = new (CameraClass as unknown as new (v: HTMLVideoElement, cfg: { onFrame: () => Promise<void>; width: number; height: number }) => CameraWrapper)(video, {
      onFrame: async () => {
        await faceDetection.send({ image: video });
      },
      width: 640,
      height: 480
    });

    camera.start();
  } catch (error) {
    console.error('Face detection initialization failed:', error);
    throw error;
  }
}

async function initAudioDetection(sessionId: string): Promise<void> {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    source.connect(analyser);
    analyser.fftSize = 256;
    const data = new Uint8Array(analyser.frequencyBinCount);

    audioDetectionInterval = setInterval(() => {
      analyser.getByteFrequencyData(data);
      const avg = data.reduce((s, v) => s + v, 0) / data.length;
      if (avg > 50) {
        logProctoringViolation(sessionId, 'audio_detected', 'Significant audio detected');
      }
    }, 2000);
  } catch (error) {
    console.error('Audio detection initialization failed:', error);
    throw error;
  }
}

function initTabSwitchDetection(sessionId: string): void {
  let tabSwitchCount = 0;

  const handler = () => {
    if (document.hidden) {
      tabSwitchCount++;
      if (tabSwitchCount > 2) {
        logProctoringViolation(sessionId, 'tab_switch', 'User switched tab');
        tabSwitchCount = 0;
      }
    } else {
      tabSwitchCount = 0;
    }
  };

  document.addEventListener('visibilitychange', handler);
  tabSwitchListener = handler;
}

export function cleanupProctoring(): void {
  if (audioDetectionInterval) {
    clearInterval(audioDetectionInterval);
    audioDetectionInterval = null;
  }

  if (tabSwitchListener) {
    document.removeEventListener('visibilitychange', tabSwitchListener);
    tabSwitchListener = null;
  }
}