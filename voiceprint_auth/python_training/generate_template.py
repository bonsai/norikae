"""
Voiceprint Template Generator
Extracts MFCC features from WAV files and exports C header for CH32V003
"""

import librosa
import numpy as np
import argparse
from pathlib import Path


def extract_voice_print(wav_path: str, sr: int = 16000, n_mfcc: int = 13) -> np.ndarray:
    """
    Extract MFCC feature vector from WAV file
    
    Args:
        wav_path: Path to input WAV file
        sr: Target sample rate (16kHz recommended for edge devices)
        n_mfcc: Number of MFCC coefficients (13 is standard)
    
    Returns:
        Mean MFCC vector (shape: [n_mfcc])
    """
    # Load and resample to target rate
    y, _ = librosa.load(wav_path, sr=sr, mono=True)
    
    # Extract MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    # Average over time to get single feature vector
    voice_print = np.mean(mfcc.T, axis=0)
    
    return voice_print


def calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Calculate cosine similarity between two voice prints"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def save_template(voice_print: np.ndarray, name: str, output_dir: str = ".") -> Path:
    """Save voice print as .npy file"""
    output_path = Path(output_dir) / f"{name}_template.npy"
    np.save(output_path, voice_print)
    print(f"✓ Saved template: {output_path}")
    return output_path


def export_c_header(templates: dict, output_path: str = "speaker_templates.h"):
    """
    Export voice templates as C header file for CH32V003 firmware
    
    Args:
        templates: Dict of {name: voice_print_array}
        output_path: Output .h file path
    """
    n_mfcc = len(list(templates.values())[0])
    n_speakers = len(templates)
    
    with open(output_path, 'w') as f:
        f.write("// Auto-generated voice templates for CH32V003\n")
        f.write(f"#define NUM_SPEAKERS {n_speakers}\n")
        f.write(f"#define MFCC_DIM {n_mfcc}\n\n")
        
        f.write("const float speaker_templates[NUM_SPEAKERS][MFCC_DIM] = {\n")
        for name, vec in templates.items():
            f.write(f"  // {name}\n")
            f.write("  {" + ", ".join(f"{v:.6f}" for v in vec) + "},\n")
        f.write("};\n\n")
        
        f.write("const char* speaker_names[NUM_SPEAKERS] = {\n")
        for name in templates.keys():
            f.write(f'  "{name}",\n')
        f.write("};\n")
    
    print(f"✓ Exported C header: {output_path}")


def authenticate_test(test_wav: str, template_path: str, threshold: float = 0.85) -> bool:
    """
    Test authentication against a stored template
    
    Returns:
        True if similarity >= threshold
    """
    template = np.load(template_path)
    current = extract_voice_print(test_wav)
    similarity = calculate_similarity(template, current)
    
    print(f"Similarity: {similarity:.4f} (threshold: {threshold})")
    return similarity >= threshold


def main():
    parser = argparse.ArgumentParser(description="Voiceprint Template Generator")
    parser.add_argument("mode", choices=["train", "test", "export"], help="Operation mode")
    parser.add_argument("--input", "-i", required=True, help="Input WAV file(s)")
    parser.add_argument("--name", "-n", help="Speaker name (for train mode)")
    parser.add_argument("--template", "-t", help="Template file (for test mode)")
    parser.add_argument("--threshold", default=0.85, type=float, help="Authentication threshold")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    if args.mode == "train":
        # Generate template from training WAV
        if not args.name:
            print("Error: --name required for train mode")
            return
        
        voice_print = extract_voice_print(args.input)
        print(f"Extracted MFCC features: {len(voice_print)} dimensions")
        print(f"Feature vector: {voice_print}")
        
        save_template(voice_print, args.name, args.output)
        
    elif args.mode == "test":
        # Test authentication
        if not args.template:
            print("Error: --template required for test mode")
            return
        
        result = authenticate_test(args.input, args.template, args.threshold)
        print(f"✓ AUTHORIZED" if result else "✗ REJECTED")
        
    elif args.mode == "export":
        # Export multiple templates to C header
        import glob
        templates = {}
        for npy_file in glob.glob(args.input):
            name = Path(npy_file).stem.replace("_template", "")
            templates[name] = np.load(npy_file)
        
        export_c_header(templates, Path(args.output) / "speaker_templates.h")


if __name__ == "__main__":
    main()
