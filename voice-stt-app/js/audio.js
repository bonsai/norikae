/**
 * Audio Recording Module
 * Handles microphone access and audio capture using Web Audio API
 */

let audioContext = null;

/**
 * Initialize AudioContext (must be called after user interaction)
 */
function initAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

/**
 * Record audio from microphone
 * @param {number} duration - Recording duration in milliseconds (default: 2500)
 * @returns {Promise<Float32Array>} Audio samples as Float32Array
 */
export async function recordAudio(duration = 2500) {
  initAudioContext();

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: false,
        noiseSuppression: false,
        sampleRate: 44100
      }
    });

    const source = audioContext.createMediaStreamSource(stream);
    const processor = audioContext.createScriptProcessor(4096, 1, 1);
    let samples = [];

    return new Promise((resolve) => {
      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        samples.push(...inputData);
      };

      source.connect(processor);
      processor.connect(audioContext.destination);

      setTimeout(() => {
        stream.getTracks().forEach((track) => track.stop());
        processor.disconnect();
        resolve(new Float32Array(samples));
      }, duration);
    });
  } catch (error) {
    console.error("Audio recording error:", error);
    throw new Error("Failed to access microphone. Please allow microphone permissions.");
  }
}

/**
 * Calculate RMS (Root Mean Square) of audio samples
 * @param {Float32Array} samples - Audio samples
 * @returns {number} RMS value
 */
function calculateRMS(samples) {
  let sum = 0;
  for (let i = 0; i < samples.length; i++) {
    sum += samples[i] * samples[i];
  }
  return Math.sqrt(sum / samples.length);
}

/**
 * Detect if audio contains voice activity
 * @param {Float32Array} samples - Audio samples
 * @param {number} threshold - RMS threshold for voice detection
 * @returns {boolean} True if voice activity detected
 */
function hasVoiceActivity(samples, threshold = 0.02) {
  return calculateRMS(samples) > threshold;
}
