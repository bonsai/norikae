# Quick Start Guide

## Project 1: Voiceprint Authentication (声紋認証)

### What You'll Build
A voice-activated lock system using CH32V003 that:
- Records your voice via analog mic
- Extracts MFCC features on-device
- Compares against stored templates
- Unlocks a servo motor when authorized
- Sends "UNLOCK_OK" to UiPath via serial

### Hardware Needed
| Item | Model/Spec | Qty | Notes |
|------|------------|-----|-------|
| MCU Board | UIAPduino Pro Micro CH32V003 | 1 | 48MHz, 16KB Flash, 2KB RAM |
| Microphone | MAX4466 (with pre-amp) | 1 | Analog output |
| Servo | SG90 (9g micro servo) | 1 | For lock mechanism |
| Jumper wires | Female-to-Female | 10+ | For connections |
| USB-TTL | CH340/CP2102 | 1 | For programming |

### Wiring Diagram
```
CH32V003          MAX4466
  PA1 (ADC)   ───  OUT
  3.3V        ───  VCC
  GND         ───  GND

CH32V003          SG90 Servo
  PD4 (Timer2) ───  Orange (Signal)
  5V           ───  Red (Power)
  GND          ───  Brown (Ground)

CH32V003          USB-TTL
  PA2 (TX)     ───  RX
  PA3 (RX)     ───  TX
  GND          ───  GND
```

### Software Setup

#### Step 1: Install Python Dependencies
```bash
cd "G:\My Drive\voiceprint_auth"
pip install -r requirements.txt
```

#### Step 2: Record Training Data
Record your voice as WAV files (use Windows Voice Recorder or Audacity):
- Sample rate: 16kHz
- Bit depth: 16-bit
- Channels: Mono
- Duration: 3-5 seconds

Say something like "Open sesame" or your preferred trigger phrase.

#### Step 3: Generate Voice Template
```bash
# Train with your voice
python python_training/generate_template.py train \
  --input "my_voice.wav" \
  --name "tomohiro" \
  --output "./templates"

# Export to C header for firmware
python python_training/generate_template.py export \
  --input "./templates/*.npy" \
  --output "./firmware"
```

#### Step 4: Test Authentication Accuracy
```bash
# Create test samples (record 5 versions of your phrase)
python python_training/generate_template.py test \
  --input "test1.wav" \
  --template "./templates/tomohiro_template.npy" \
  --threshold 0.85
```

#### Step 5: Flash Firmware
1. Install WCH-LinkE driver: https://www.wch.cn/downloads/
2. Open `firmware/voiceprint_auth.c` in MounRiver Studio or VSCode
3. Replace `speaker_templates.h` values with your generated templates
4. Build and flash to CH32V003

#### Step 6: Test with UiPath
1. Open UiPath
2. Create new "Serial Monitor" workflow
3. Listen for "UNLOCK_OK" on COM port
4. Trigger your automation when received

### Tuning Tips
- **Threshold too low?** → False positives (others can unlock)
- **Threshold too high?** → False negatives (you can't unlock)
- **Adjust threshold**: Change `AUTH_THRESHOLD` in `speaker_templates.h`
- **Better accuracy**: Record more training samples (5-10 variations)

---

## Project 2: ECG Monitor (心電図計)

### What You'll Build
A battery-powered ECG monitor that:
- Reads heart signals via electrodes
- Detects R-waves (heartbeats) in real-time
- Calculates heart rate (BPM)
- Streams data to PC via WebSerial
- Can detect arrhythmia with TinyML

### ⚠️ Safety Warning
**This device connects to your body. Follow these rules:**
1. **Battery power ONLY** - Never connect to USB while electrodes attached
2. **Use galvanic isolation** - Optocouplers for all signal lines to PC
3. **1MΩ protection resistors** - At each electrode input
4. **Test with signal generator first** - Before human use

### Hardware Needed
| Item | Model/Spec | Qty | Notes |
|------|------------|-----|-------|
| MCU Board | CH32V203C8T6 (or V307) | 1 | 20KB+ RAM recommended |
| Instrumentation Amp | AD620 or INA128 | 1 | Or build 3-op-amp discrete |
| Op-Amp | LMV358 | 3 | For filters (if discrete) |
| Electrodes | Ag/AgCl disposable | 3 | Standard ECG electrodes |
| Battery | 3.7V Li-ion + LDO | 1 | 3.3V regulator required |
| Resistors | 1MΩ, 499Ω, 10kΩ, 1kΩ | Various | See circuit_design.md |
| Capacitors | 0.33uF, 1nF, 330nF | Various | See circuit_design.md |

### Wiring Diagram (AD620 Version)
```
Electrodes              AD620              CH32V203
  RA ──[1MΩ]──────────── Pin 2 (-IN)
  LA ──[1MΩ]──────────── Pin 3 (+IN)       PA1 (ADC)
  RL ─────────────────── Pin 5 (REF)       GND

                        Pin 6 (OUT) ───────┬─[1MΩ]─┬─ To ADC
                                           │      │
                                          [10kΩ]  ┌┴┐
                                           │      │ │ 0.33uF (HPF)
                                          GND     └┬┘
                                                   │
                                                  GND

Power:
  V+ (Pin 7) ── 5V (battery)
  V- (Pin 4) ── GND (single supply)
  Pin 4 ──[10uF]── GND (decoupling)
```

### Software Setup

#### Step 1: Install Python Dependencies
```bash
cd "G:\My Drive\ecg_monitor"
pip install -r requirements.txt
```

#### Step 2: Generate Synthetic ECG for Testing
```bash
# Generate normal ECG (60 BPM)
python python_analysis/synthetic_ecg.py \
  --type normal \
  --hr 60 \
  --duration 10 \
  --output "test_normal.wav"

# Generate arrhythmia (for ML training)
python python_analysis/synthetic_ecg.py \
  --type afib \
  --duration 10 \
  --output "test_afib.wav"
```

#### Step 3: Test R-Wave Detection
```bash
python python_analysis/r_wave_detect.py test_normal.wav
```

This will:
- Detect R-peaks using Pan-Tompkins algorithm
- Calculate heart rate
- Generate analysis plot (`test_normal_analysis.png`)

#### Step 4: Build Analog Circuit
Follow `docs/circuit_design.md` to build the front-end on breadboard.

#### Step 5: Test with Function Generator
Before human use:
1. Set function generator to: 1mV sine, 10Hz
2. Connect to circuit input
3. Verify ~100mV output on oscilloscope
4. Check frequency response (0.5Hz - 150Hz flat)

#### Step 6: Flash Firmware
1. Modify `firmware/ecg_monitor.c` for your hardware
2. Build with MounRiver Studio (CH32V203 SDK)
3. Flash via SWD programmer

#### Step 7: View Real-Time ECG
```bash
# Optional: Run WebSerial viewer
python pwa_viewer/app.py
# Open browser: http://localhost:5000
```

### Expected Results
- **Resting HR**: 60-100 BPM (normal adult)
- **R-R interval**: ~1 second (60 BPM) to ~0.6s (100 BPM)
- **Signal amplitude**: 0.5-2mV at electrodes, ~100-200mV after amp

### Troubleshooting
| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| No signal | Electrode contact | Re-attach, use fresh electrodes |
| 50/60Hz noise | Mains hum | Check RLD connection, add notch filter |
| Baseline drift | Movement/breathing | Improve HPF (lower cutoff) |
| Saturated output | Gain too high | Increase Rg (reduce gain) |

---

## Next Steps

### Voiceprint Project
- [ ] Add more speaker templates (family members)
- [ ] Implement VAD (Voice Activity Detection)
- [ ] Try BitNetMCU for neural network approach
- [ ] Add to UiPath workflow for auto-login

### ECG Project
- [ ] Build PCB version (KiCad design)
- [ ] Add TinyML arrhythmia detection (emlearn)
- [ ] Create PWA viewer with WebSerial
- [ ] Log data to cloud for long-term analysis

## Community & Support
- CH32V003fun: https://github.com/cnlohr/ch32v003fun
- BitNetMCU: https://github.com/microsoft/BitNet
- emlearn: https://github.com/emlearn/emlearn
