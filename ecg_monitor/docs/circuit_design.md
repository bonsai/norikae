# ECG Analog Front-End Circuit Design

## Overview

This document describes the analog front-end circuit for the DIY ECG monitor.
The circuit amplifies the微弱 heart signal (~1mV) to a level suitable for ADC conversion.

## Safety First ⚠️

**CRITICAL**: This device connects to the human body. Follow these rules:

1. **Battery Power Only**: Never connect to USB/PC while electrodes are attached
2. **Galvanic Isolation**: Use optocouplers for all signal lines to PC
3. **Protection Resistors**: 1MΩ minimum at each electrode input
4. **Test First**: Verify with function generator before human use

## Circuit Blocks

### 1. Instrumentation Amplifier (Initial Stage)

**Option A: AD620 (Recommended)**

```
        Electrode RA ──┬──[1MΩ]──┬── Pin 2 (-IN)
                       │         │
                      [10kΩ]    ┌┴┐ AD620
                       │        │ │
        Electrode LA ──┴──[1MΩ]─┤ ├─ Pin 6 (OUT) ──→ To Filter
                                 │ │
        Rg ──[499Ω]──────────────┤ ├─ Pin 3 (+IN)
                                 └┬┘
                                  │
        Electrode RL ─────────────┴── Pin 5 (REF)
```

**Gain Calculation**:
```
G = 1 + (49.4kΩ / Rg)

For G = 100:
Rg = 49.4kΩ / 99 ≈ 500Ω (use 499Ω standard value)
```

**Option B: 3-Op-Amp Discrete (LMV358 × 3)**

```
Stage 1: Buffer Amplifiers (×2)
  - Non-inverting configuration
  - Gain = 1 (unity buffer)
  - High input impedance

Stage 2: Difference Amplifier
  - Subtracts the two buffered signals
  - Gain = Rf/Rin (typically 10-50)
```

### 2. Filter Stages

#### High-Pass Filter (0.5Hz cutoff)
Removes baseline wander from breathing/movement

```
        Input ──||────┬──── Output
              0.33uF  │
                     ┌┴┐
                     │ │ 1MΩ (to Vref)
                     └┬┘
                      │
                     GND
```

**Cutoff Frequency**:
```
fc = 1 / (2π × R × C)
   = 1 / (2π × 1MΩ × 0.33uF)
   ≈ 0.48 Hz
```

#### Low-Pass Filter (150Hz cutoff)
Removes EMG noise and prevents aliasing

```
        Input ──┬──[1kΩ]──┬──── Output
                │         │
               ┌┴┐       ┌┴┐
               │ │ 1nF   │ │ 1nF (to GND)
               └┬┘       └┬┘
                │         │
               GND       GND
```

**Cutoff Frequency**:
```
fc = 1 / (2π × R × C)
   = 1 / (2π × 1kΩ × 1nF)
   ≈ 159 Hz
```

#### Notch Filter (50/60Hz)
Removes mains hum (optional, can be done digitally)

**Twin-T Notch Filter**:
```
                    [R]
        Input ──[R]──┬──[R]── Output
                     │
                    ┌┴┐
                    │ │ 2C
                    └┬┘
                     │
        Input ──||───┴───||── Output
                2C        C
```

**Component Values for 50Hz**:
- R = 10kΩ
- C = 330nF
- 2C = 680nF (parallel 330nF + 330nF)

### 3. Right Leg Drive (RLD)

Active noise cancellation for common-mode interference

```
        RLD Electrode ──[1MΩ]──┬── Output of Inverting Amp
                               │
        Inverting Amp Input ───┴── From RA/LA average
```

### 4. Protection Circuit

```
        Electrode ──[1MΩ]──┬──[10kΩ]──┬── To Amp Input
                           │          │
                          ┌┴┐        ┌┴┐
                          │ │        │ │ Zener (3.3V)
                          │ │ 100nF  └┬┘
                          └┬┘        │
                           │        GND
                          GND
```

## Complete Signal Chain

```
Electrodes (RA, LA, RL)
    ↓
Protection (1MΩ + ESD diodes)
    ↓
Instrumentation Amp (G = 100)
    ↓
High-Pass Filter (0.5Hz)
    ↓
Low-Pass Filter (150Hz)
    ↓
Notch Filter (50/60Hz, optional)
    ↓
Right Leg Drive (feedback)
    ↓
CH32V203 ADC (PA1)
```

## Component List

| Component | Value | Quantity | Purpose |
|-----------|-------|----------|---------|
| AD620 | - | 1 | Instrumentation amp |
| LMV358 | - | 3 | Alternative (3-op-amp) |
| Resistor | 1MΩ | 3 | Input protection |
| Resistor | 499Ω | 1 | Gain setting (AD620) |
| Resistor | 10kΩ | 4 | Filter |
| Resistor | 1kΩ | 2 | LPF |
| Capacitor | 0.33uF | 1 | HPF |
| Capacitor | 1nF | 2 | LPF |
| Capacitor | 330nF | 3 | Notch |
| Capacitor | 100nF | 2 | Decoupling |
| Zener | 3.3V | 2 | Overvoltage protection |

## PCB Layout Tips

1. **Keep analog traces short** - Minimize noise pickup
2. **Ground plane** - Use solid ground plane under analog section
3. **Separate analog/digital** - Keep MCU digital signals away from analog front-end
4. **Power decoupling** - 100nF capacitor close to each IC power pin
5. **Electrode placement** - Standard Lead I configuration:
   - RA (Right Arm): Right wrist/upper arm
   - LA (Left Arm): Left wrist/upper arm
   - RL (Right Leg): Right ankle/lower leg (reference)

## Testing Procedure

1. **Power Check**: Verify ±5V (or single 3.3V) supply
2. **Offset Check**: Output should be ~VCC/2 (1.65V for 3.3V system)
3. **Gain Check**: Inject 1mV sine wave @ 10Hz, verify ~100mV output
4. **Frequency Response**: Sweep 0.1Hz - 500Hz, verify flat response
5. **Noise Check**: Short inputs, verify output noise < 10mVpp

## References

- AD620 Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/ad620.pdf
- AAMI EC11 (ECG Standard): https://www.aami.org/
- "Bioelectric Amplifiers" - Texas Instruments Application Note
