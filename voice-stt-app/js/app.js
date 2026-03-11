/**
 * Unified Voice Digit STT Application Module
 * Merged from: pyodide_setup.js, audio.js, stt.js
 */

// --- Global States ---
let pyodide = null;
let audioContext = null;
let digitTemplates = {};

// --- Pyodide Setup (from pyodide_setup.js) ---
async function initPyodide() {
  if (pyodide) return pyodide;

  console.log("Loading Pyodide...");
  pyodide = await loadPyodide();
  await pyodide.loadPackage("numpy");

  // Define Python functions for feature extraction and comparison
  await pyodide.runPythonAsync(`
import numpy as np

def get_features(audio_data):
    """Extract 16-dimensional feature vector from audio using FFT"""
    y = np.array(audio_data.to_py())
    
    # Normalize amplitude
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y))
    
    # FFT and split into 16 bands
    fft = np.abs(np.fft.rfft(y))
    features = np.mean(np.array_split(fft, 16), axis=1)
    return features.tolist()

def get_features_temporal(audio_data):
    """Extract features with temporal segmentation (3 segments)"""
    y = np.array(audio_data.to_py())
    if np.max(np.abs(y)) > 0:
        y = y / np.max(np.abs(y))
    
    # Split audio into 3 temporal segments
    segment_size = len(y) // 3
    segments = [y[:segment_size], y[segment_size:segment_size*2], y[segment_size*2:]]
    
    # Extract FFT features from each segment
    all_features = []
    for seg in segments:
        if len(seg) > 0:
            fft = np.abs(np.fft.rfft(seg))
            seg_features = np.mean(np.array_split(fft, 8), axis=1)
            all_features.extend(seg_features.tolist())
    
    return all_features  # 24-dimensional vector

def compare(vec_a, vec_b):
    """Calculate cosine similarity between two vectors"""
    a, b = np.array(vec_a), np.array(vec_b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def update_profile(current_vec, new_vec, learning_rate=0.1):
    """Blend new data into existing profile (for continuous learning)"""
    c = np.array(current_vec)
    n = np.array(new_vec)
    updated = (c * (1.0 - learning_rate)) + (n * learning_rate)
    return updated.tolist()
`);

  console.log("✅ Pyodide initialized");
  return pyodide;
}

function getPyodide() {
  return pyodide;
}

// --- Audio Recording (from audio.js) ---
function initAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return audioContext;
}

async function recordAudio(duration = 2500) {
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

function calculateRMS(samples) {
  let sum = 0;
  for (let i = 0; i < samples.length; i++) {
    sum += samples[i] * samples[i];
  }
  return Math.sqrt(sum / samples.length);
}

function hasVoiceActivity(samples, threshold = 0.02) {
  return calculateRMS(samples) > threshold;
}

// --- STT Logic (from stt.js) ---
async function loadDigitTemplates(path = "./digits.json") {
  try {
    const response = await fetch(path);
    digitTemplates = await response.json();
    console.log("✅ Loaded digit templates:", Object.keys(digitTemplates).length, "digits");
    return digitTemplates;
  } catch (error) {
    console.error("Failed to load digit templates:", error);
    digitTemplates = {};
    return {};
  }
}

function setDigitTemplates(templates) {
  digitTemplates = templates;
}

async function recognizeDigit(audioData, threshold = 0.8) {
  const pyodide = getPyodide();
  if (!pyodide) {
    throw new Error("Pyodide not initialized");
  }

  const getFeatures = pyodide.globals.get("get_features");
  const compare = pyodide.globals.get("compare");

  // Extract features from input audio
  const inputVec = getFeatures(audioData);

  // Compare with all digit templates
  let bestDigit = null;
  let maxSimilarity = 0;
  const allScores = {};

  for (const [digit, template] of Object.entries(digitTemplates)) {
    if (!template || template.length === 0) continue;

    const similarity = compare(template, inputVec);
    allScores[digit] = similarity;

    if (similarity > maxSimilarity) {
      maxSimilarity = similarity;
      bestDigit = digit;
    }
  }

  // Return result only if confidence exceeds threshold
  if (maxSimilarity < threshold) {
    return { digit: null, confidence: maxSimilarity, allScores };
  }

  return { digit: bestDigit, confidence: maxSimilarity, allScores };
}

async function registerDigit(digit, audioData) {
  const pyodide = getPyodide();
  if (!pyodide) {
    throw new Error("Pyodide not initialized");
  }

  const getFeatures = pyodide.globals.get("get_features");
  const featureVec = getFeatures(audioData);
  
  digitTemplates[digit] = featureVec;
  return featureVec;
}

async function registerDigitAveraged(digit, audioSamples) {
  const pyodide = getPyodide();
  if (!pyodide) {
    throw new Error("Pyodide not initialized");
  }

  const getFeatures = pyodide.globals.get("get_features");
  const featureVectors = audioSamples.map((sample) => getFeatures(sample));
  
  // Calculate average vector using Python/NumPy
  const avgVec = pyodide.globals.get("update_profile")(featureVectors[0], featureVectors[1], 0.5);
  const finalVec = pyodide.globals.get("update_profile")(avgVec, featureVectors[2], 0.5);
  
  digitTemplates[digit] = finalVec;
  return finalVec;
}

function exportTemplates() {
  return JSON.stringify(digitTemplates, null, 2);
}

// --- Exports ---
export { 
  initPyodide, 
  getPyodide, 
  recordAudio, 
  hasVoiceActivity,
  loadDigitTemplates, 
  setDigitTemplates, 
  recognizeDigit,
  registerDigit,
  registerDigitAveraged,
  exportTemplates
};
