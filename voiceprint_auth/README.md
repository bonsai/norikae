# Voiceprint Authentication System (声紋認証システム)

On-device speaker recognition using CH32V003 (UIAPduino Pro Micro)

## Project Overview

**Goal**: Authenticate users by voice pattern on edge device (no cloud API)

**Hardware**:
- MCU: CH32V003 (48MHz, 16KB Flash, 2KB RAM)
- Mic: MAX4466 analog microphone with pre-amp
- Output: Servo motor for physical lock + Serial to UiPath

## Technical Stack

### Approach 1: Traditional Signal Processing (Recommended for start)
- **Feature Extraction**: MFCC (13 coefficients, 8kHz, 20ms frames)
- **Classification**: Template matching with cosine similarity
- **Implementation**: Fixed-point arithmetic (Q15) for CH32V003

### Approach 2: TinyML
- **Framework**: BitNetMCU (1-bit quantized neural networks)
- **Training**: PyTorch on PC → C header export
- **Inference**: Pure C on device (no multiplication needed)

## Project Structure

```
voiceprint_auth/
├── firmware/           # CH32V003 C code (ch32v003fun)
├── python_training/    # Python scripts for model generation
├── pwa_webserial/      # Optional: Web-based UI with WASM
└── docs/              # Circuit diagrams, notes
```

## Development Flow

1. **PC Python**: Record voice → Extract MFCC → Generate template (.npy → .h)
2. **Firmware**: ADC sampling → MFCC (fixed-point) → Compare with template
3. **Output**: GPIO high (servo unlock) + Serial "UNLOCK_OK" to UiPath

## Key Constraints

| Resource | CH32V003 | Strategy |
|----------|----------|----------|
| Flash | 16KB | Store templates as const in Flash |
| RAM | 2KB | Ring buffer + streaming MFCC (no full buffer) |
| CPU | 48MHz, no FPU | Fixed-point Q15 arithmetic only |

## Getting Started

```bash
# Install Python dependencies
pip install librosa numpy scipy matplotlib

# Generate voice template from WAV
python python_training/generate_template.py my_voice.wav

# Flash firmware to CH32V003 (using WCH-LinkE)
```

## References
- Brian Smith's CH32V003 STT: https://github.com/smurf0969/ch32v003_stt
- ch32v003fun: https://github.com/cnlohr/ch32v003fun
- BitNetMCU: https://github.com/microsoft/BitNet
