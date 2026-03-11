"""
Synthetic ECG Waveform Generator
Generates realistic ECG signals for testing and ML training
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
import argparse


def generate_ecg_waveform(
    duration_sec: float = 10,
    heart_rate_bpm: float = 60,
    sample_rate: int = 500,
    noise_level: float = 0.0
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic ECG waveform with P-QRS-T complex
    
    Args:
        duration_sec: Duration in seconds
        heart_rate_bpm: Heart rate in beats per minute
        sample_rate: Sampling rate in Hz
        noise_level: Standard deviation of Gaussian noise
    
    Returns:
        (time_array, ecg_signal)
    """
    # Time array
    t = np.linspace(0, duration_sec, int(duration_sec * sample_rate))
    
    # Heart rate to beat period
    beat_period = 60.0 / heart_rate_bpm
    
    # Initialize signal
    ecg = np.zeros_like(t)
    
    # Generate each beat
    for i in range(int(duration_sec / beat_period)):
        beat_center = i * beat_period
        
        # P wave (atrial depolarization)
        p_wave = 0.15 * np.exp(-((t - (beat_center - 0.2)) ** 2) / 0.002)
        
        # QRS complex (ventricular depolarization)
        q_wave = -0.15 * np.exp(-((t - (beat_center - 0.05)) ** 2) / 0.001)
        r_wave = 1.0 * np.exp(-((t - beat_center) ** 2) / 0.0005)
        s_wave = -0.25 * np.exp(-((t - (beat_center + 0.05)) ** 2) / 0.001)
        qrs = q_wave + r_wave + s_wave
        
        # T wave (ventricular repolarization)
        t_wave = 0.25 * np.exp(-((t - (beat_center + 0.25)) ** 2) / 0.005)
        
        # Add to signal
        ecg += p_wave + qrs + t_wave
    
    # Add noise
    if noise_level > 0:
        ecg += np.random.normal(0, noise_level, len(ecg))
    
    # Add baseline wander (simulating breathing)
    baseline = 0.1 * np.sin(2 * np.pi * 0.3 * t)
    ecg += baseline
    
    return t, ecg


def generate_arrhythmia_ecg(
    duration_sec: float = 10,
    sample_rate: int = 500,
    arrhythmia_type: str = "afib"
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generate ECG with arrhythmia for anomaly detection training
    
    Args:
        arrhythmia_type: "afib" (atrial fibrillation), "pvc" (premature ventricular contraction)
    """
    t = np.linspace(0, duration_sec, int(duration_sec * sample_rate))
    ecg = np.zeros_like(t)
    
    if arrhythmia_type == "afib":
        # Irregular R-R intervals, no P waves
        beat_times = np.cumsum(np.random.uniform(0.5, 1.0, int(duration_sec * 1.5)))
        for beat_center in beat_times[beat_times < duration_sec]:
            # No P wave (characteristic of AFib)
            r_wave = 1.0 * np.exp(-((t - beat_center) ** 2) / 0.0005)
            t_wave = 0.25 * np.exp(-((t - (beat_center + 0.25)) ** 2) / 0.005)
            ecg += r_wave + t_wave
    
    elif arrhythmia_type == "pvc":
        # Normal beats with occasional PVC
        beat_times = np.arange(0, duration_sec, 60/60)  # 60 BPM
        for i, beat_center in enumerate(beat_times):
            if i % 5 == 3:  # Every 4th beat is PVC
                # Wide QRS, no P wave
                qrs = 1.2 * np.exp(-((t - beat_center) ** 2) / 0.002)
            else:
                # Normal beat
                p_wave = 0.15 * np.exp(-((t - (beat_center - 0.2)) ** 2) / 0.002)
                r_wave = 1.0 * np.exp(-((t - beat_center) ** 2) / 0.0005)
                t_wave = 0.25 * np.exp(-((t - (beat_center + 0.25)) ** 2) / 0.005)
                qrs = p_wave + r_wave + t_wave
            ecg += qrs
    
    # Add noise
    ecg += np.random.normal(0, 0.05, len(ecg))
    
    return t, ecg


def save_as_wav(ecg_signal: np.ndarray, sample_rate: int, output_path: str):
    """Save ECG signal as 16-bit WAV file"""
    from scipy.io import wavfile
    
    # Normalize to 16-bit range
    ecg_normalized = ecg_signal / np.max(np.abs(ecg_signal))
    ecg_int16 = (ecg_normalized * 32767).astype(np.int16)
    
    wavfile.write(output_path, sample_rate, ecg_int16)
    print(f"✓ Saved WAV: {output_path}")


def plot_ecg(t: np.ndarray, ecg: np.ndarray, title: str = "ECG Waveform"):
    """Plot ECG waveform"""
    plt.figure(figsize=(12, 4))
    plt.plot(t, ecg, linewidth=0.5)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (mV)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, min(5, t[-1]))  # Show first 5 seconds
    plt.tight_layout()
    plt.savefig(title.replace(" ", "_").lower() + ".png", dpi=150)
    print(f"✓ Saved plot: {title.replace(' ', '_').lower()}.png")


def main():
    parser = argparse.ArgumentParser(description="Synthetic ECG Generator")
    parser.add_argument("--type", choices=["normal", "afib", "pvc"], default="normal")
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--hr", type=float, default=60.0, help="Heart rate (BPM)")
    parser.add_argument("--noise", type=float, default=0.0)
    parser.add_argument("--sr", type=int, default=500, help="Sample rate (Hz)")
    parser.add_argument("--output", "-o", default="synthetic_ecg.wav")
    
    args = parser.parse_args()
    
    if args.type == "normal":
        t, ecg = generate_ecg_waveform(
            duration_sec=args.duration,
            heart_rate_bpm=args.hr,
            sample_rate=args.sr,
            noise_level=args.noise
        )
        title = f"Normal ECG (HR={args.hr} BPM)"
    else:
        t, ecg = generate_arrhythmia_ecg(
            duration_sec=args.duration,
            sample_rate=args.sr,
            arrhythmia_type=args.type
        )
        title = f"Arrhythmia ECG ({args.type.upper()})"
    
    save_as_wav(ecg, args.sr, args.output)
    plot_ecg(t, ecg, title)


if __name__ == "__main__":
    main()
