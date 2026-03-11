/**
 * Speech-to-Text (STT) Module
 * Recognizes spoken digits (0-9) using voice feature matching
 */

import { getPyodide } from "./pyodide_setup.js";

let digitTemplates = {};

/**
 * Load digit templates from JSON file
 * @param {string} path - Path to digits.json
 */
export async function loadDigitTemplates(path = "./digits.json") {
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

/**
 * Set digit templates directly (for admin registration)
 * @param {Object} templates - Digit templates object
 */
export function setDigitTemplates(templates) {
  digitTemplates = templates;
}

/**
 * Recognize spoken digit from audio
 * @param {Float32Array} audioData - Audio samples
 * @param {number} threshold - Similarity threshold (default: 0.8)
 * @returns {Promise<{digit: string|null, confidence: number, allScores: Object}>} Recognition result
 */
export async function recognizeDigit(audioData, threshold = 0.8) {
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

/**
 * Register a digit template (for admin use)
 * @param {string} digit - Digit character ("0"-"9")
 * @param {Float32Array} audioData - Audio samples
 * @returns {Promise<Array>} Feature vector for the digit
 */
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

/**
 * Register digit with multiple samples (average for better accuracy)
 * @param {string} digit - Digit character ("0"-"9")
 * @param {Float32Array[]} audioSamples - Array of audio samples (3 recordings)
 * @returns {Promise<Array>} Averaged feature vector
 */
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

/**
 * Export current digit templates as JSON
 * @returns {string} JSON string of digit templates
 */
function exportTemplates() {
  return JSON.stringify(digitTemplates, null, 2);
}
