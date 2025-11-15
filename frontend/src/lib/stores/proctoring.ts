import { writable } from 'svelte/store';

interface ProctoringState {
  isCameraActive: boolean;
  isMicActive: boolean;
  isScreenSharing: boolean;
  violations: number;
  lastViolationType: string | null;
  faceDetected: boolean;
  multipleFaces: boolean;
  audioDetected: boolean;
  tabSwitchCount: number;
}

const initialState: ProctoringState = {
  isCameraActive: false,
  isMicActive: false,
  isScreenSharing: false,
  violations: 0,
  lastViolationType: null,
  faceDetected: true,
  multipleFaces: false,
  audioDetected: false,
  tabSwitchCount: 0,
};

export const proctoringStore = writable<ProctoringState>(initialState);

export function incrementViolation(type: string) {
  proctoringStore.update((state) => ({
    ...state,
    violations: state.violations + 1,
    lastViolationType: type,
  }));
}

export function updateFaceDetection(detected: boolean, multiple: boolean = false) {
  proctoringStore.update((state) => ({
    ...state,
    faceDetected: detected,
    multipleFaces: multiple,
  }));
}

export function updateAudioDetection(detected: boolean) {
  proctoringStore.update((state) => ({
    ...state,
    audioDetected: detected,
  }));
}

export function incrementTabSwitch() {
  proctoringStore.update((state) => ({
    ...state,
    tabSwitchCount: state.tabSwitchCount + 1,
  }));
}