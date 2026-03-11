# Quick Start Guide

See the main quickstart at: `G:\My Drive\voiceprint_auth\QUICKSTART.md`

## ECG Monitor Specific Steps

### Step 1: Install Dependencies
```bash
cd "G:\My Drive\ecg_monitor"
pip install -r requirements.txt
```

### Step 2: Test R-Wave Detection with Synthetic Data
```bash
# Generate test ECG
python python_analysis/synthetic_ecg.py --type normal --hr 60 -o test.wav

# Analyze it
python python_analysis/r_wave_detect.py test.wav
```

### Step 3: Build Analog Front-End
See `docs/circuit_design.md` for complete schematic and BOM.

### Step 4: Safety Check ⚠️
- [ ] Battery power only (no USB during measurement)
- [ ] 1MΩ protection resistors at electrodes
- [ ] Galvanic isolation for serial output
- [ ] Test with function generator first

### Step 5: Flash Firmware
Build `firmware/ecg_monitor.c` with MounRiver Studio for CH32V203.

### Step 6: View Output
Open serial terminal @ 115200bps to see:
```
ECG Monitor Ready
SAFETY: Ensure battery operation only!
HR: 62.3 BPM, Peaks: 8
```
