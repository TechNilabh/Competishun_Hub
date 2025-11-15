export interface FaceLandmark {
  x: number
  y: number
  z?: number
}

export interface RelativeBoundingBox {
  xMin: number
  yMin: number
  width: number
  height: number
}

export interface LocationData {
  relativeBoundingBox: RelativeBoundingBox
  relativeLandmarks: FaceLandmark[]
}

export interface Detection {
  boundingBox: {
    xCenter: number
    yCenter: number
    width: number
    height: number
  }
  locationData: LocationData
  score: number[]
}

export interface FaceDetectionResult {
  detections: Detection[]
  image?: HTMLCanvasElement | HTMLVideoElement
}

declare module "@mediapipe/face_detection" {
  export class FaceDetection {
    constructor(options: { locateFile: (file: string) => string })
    setOptions(options: { model: string; minDetectionConfidence: number }): void
    onResults(callback: (results: FaceDetectionResult) => void): void
    send(input: { image: HTMLVideoElement }): Promise<void>
  }
}

declare module "@mediapipe/camera_utils" {
  export class Camera {
    constructor(
      video: HTMLVideoElement,
      options: {
        onFrame: () => Promise<void>
        width: number
        height: number
      }
    )
    start(): void
    stop(): void
  }
}
