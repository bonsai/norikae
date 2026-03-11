"""
Batch Voiceprint Accuracy Test
Test authentication accuracy with multiple samples per speaker
"""

import numpy as np
import glob
from pathlib import Path
from generate_template import extract_voice_print, calculate_similarity


def run_accuracy_test(template_dir: str, test_dir: str, threshold: float = 0.85):
    """
    Run batch accuracy test
    
    Args:
        template_dir: Directory containing *_template.npy files
        test_dir: Directory containing test WAV files (speakername_001.wav, etc.)
        threshold: Authentication threshold
    """
    # Load all templates
    templates = {}
    for npy_file in glob.glob(f"{template_dir}/*_template.npy"):
        name = Path(npy_file).stem.replace("_template", "")
        templates[name] = np.load(npy_file)
    
    print(f"Loaded {len(templates)} speaker templates: {list(templates.keys())}\n")
    
    # Test each WAV file
    results = {"correct": 0, "total": 0, "by_speaker": {}}
    
    for wav_file in glob.glob(f"{test_dir}/*.wav"):
        filename = Path(wav_file).stem
        # Expected format: speakername_001.wav
        parts = filename.rsplit("_", 1)
        if len(parts) != 2:
            print(f"⚠ Skipping {filename} (expected format: name_001.wav)")
            continue
        
        expected_speaker = parts[0]
        current_features = extract_voice_print(wav_file)
        
        # Find best match
        best_match = None
        best_similarity = -1
        for name, template in templates.items():
            sim = calculate_similarity(current_features, template)
            if sim > best_similarity:
                best_similarity = sim
                best_match = name
        
        # Check if correct
        is_authenticated = best_similarity >= threshold
        is_correct = (best_match == expected_speaker)
        
        results["total"] += 1
        if is_correct:
            results["correct"] += 1
        
        if expected_speaker not in results["by_speaker"]:
            results["by_speaker"][expected_speaker] = {"correct": 0, "total": 0}
        results["by_speaker"][expected_speaker]["total"] += 1
        if is_correct:
            results["by_speaker"][expected_speaker]["correct"] += 1
        
        status = "✓" if is_correct else "✗"
        auth_status = "AUTH" if is_authenticated else "REJ"
        print(f"{status} {filename}: predicted={best_match} ({best_similarity:.3f}) [{auth_status}]")
    
    # Summary
    print("\n" + "="*50)
    print(f"Overall Accuracy: {results['correct']}/{results['total']} = {results['correct']/results['total']*100:.1f}%")
    print("\nPer-speaker accuracy:")
    for speaker, stats in results["by_speaker"].items():
        acc = stats["correct"] / stats["total"] * 100 if stats["total"] > 0 else 0
        print(f"  {speaker}: {stats['correct']}/{stats['total']} = {acc:.1f}%")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--templates", default="./templates", help="Template directory")
    parser.add_argument("--test", default="./test_samples", help="Test WAV directory")
    parser.add_argument("--threshold", default=0.85, type=float)
    args = parser.parse_args()
    
    run_accuracy_test(args.templates, args.test, args.threshold)
