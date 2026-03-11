# DIY ECG Monitor (自作心電図計)

Real-time ECG monitoring with analog front-end + CH32V203/V307

## Project Overview

**Goal**: Build a safe, battery-powered ECG monitor with R-wave detection and TinyML anomaly classification

**Hardware**:
- MCU: CH32V203 (48MHz, 64KB Flash, 20KB RAM) or CH32V307 (64KB RAM)
- Analog Front-End: Instrumentation amp (AD620 or 3-op-amp discrete)
- Safety: Galvanic isolation, battery-only operation

## System Architecture

```
Electrodes → Instrumentation Amp → Filters → ADC → CH32V203 → Serial/BLE
                                          ↓
                                    Pan-Tompkins
                                    (R-wave detect)
                                          ↓
                                    TinyML (anomaly class)
```

## Analog Front-End Design

### 1. Instrumentation Amplifier
- **Option A**: AD620 IC (recommended for reliability)
- **Option B**: 3-op-amp discrete (LMV358 × 3)

Gain formula: `G = 1 + (49.4kΩ / Rg)` → Target G = 100~200

### 2. Filter Stages
| Filter | Cutoff | Purpose |
|--------|--------|---------|
| HPF | 0.5Hz | Remove baseline wander (breathing) |
| LPF | 150Hz | Remove EMG noise, prevent aliasing |
| Notch | 50/60Hz | Remove mains hum |

### 3. Safety Circuit
- **Protection**: 1MΩ resistors at electrodes
- **Isolation**: Optocoupler for serial communication
- **Power**: Battery only (no USB during operation)

## Digital Signal Processing

### Sampling Rate
- **Target**: 250Hz or 500Hz (adequate for ECG, low CPU load)
- **ADC**: CH32V203 internal 12-bit ADC

### R-Wave Detection: Pan-Tompkins Algorithm
1. Bandpass filter (5-15Hz)
2. Differentiation
3. Squaring
4. Moving integration
5. Adaptive thresholding

### TinyML Classification (Optional)
- **Input**: 1-second ECG window (250 samples)
- **Model**: 1-bit CNN or Random Forest (emlearn)
- **Output**: Normal / Arrhythmia / Noise

## Project Structure

```
ecg_monitor/
├── analog_circuit/     # KiCad schematics, BOM
├── firmware/           # CH32V203 C code
│   ├── adc_sampling.c
│   ├── pan_tompkins.c
│   └── tinyml_inference.c
├── python_analysis/    # PC-side analysis
│   ├── ecg_preprocess.py
│   ├── r_wave_detect.py
│   └── generate_ml_model.py
└── pwa_viewer/         # WebSerial real-time viewer
```

## Safety Warnings

⚠️ **DO NOT** connect to PC via USB while electrodes are attached to body
⚠️ **USE** battery power only during measurement
⚠️ **ADD** 1MΩ protection resistors at electrode inputs
⚠️ **TEST** with signal generator first before human use

## Getting Started

```bash
# Install Python dependencies
pip install numpy scipy matplotlib biosppy heartpy

# Simulate ECG waveform for testing
python python_analysis/synthetic_ecg.py

# Analyze recorded ECG data
python python_analysis/r_wave_detect.py sample_ecg.wav
```

## References
- Pan-Tompkins algorithm: https://github.com/berndporr/py-ecg-detectors
- AD8232 breakout (reference design): https://github.com/sparkfun/SparkFun_Bio_Sensor_Hardware_Library
- CH32V203 SDK: https://github.com/openwch/ch32v20x
- emlearn: https://github.com/emlearn/emlearn

## Next Steps

1. Build analog front-end on breadboard
2. Test with function generator (1mV sine wave)
3. Implement ADC sampling on CH32V203
4. Port Pan-Tompkins to C (fixed-point)
5. Add WebSerial viewer for real-time display
