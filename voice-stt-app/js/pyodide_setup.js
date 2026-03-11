/**
 * Pyodide Setup Module
 * Initializes Python WASM runtime and defines feature extraction logic
 */

let pyodide = null;

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

export function getPyodide() {
  return pyodide;
}
