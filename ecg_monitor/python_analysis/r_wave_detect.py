"""
R-Wave Detection using Pan-Tompkins Algorithm
Detect heartbeats from ECG signal
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks
from scipy.io import wavfile
import argparse


def bandpass_filter(signal: np.ndarray, sample_rate: int, lowcut: float = 5.0, highcut: float = 15.0, order: int = 2) -> np.ndarray:
    """Apply bandpass filter for QRS enhancement"""
    nyquist = sample_rate / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)


def differentiate(signal: np.ndarray, sample_rate: int) -> np.ndarray:
    """Approximate derivative (slope enhancement)"""
    # dy/dx ≈ (x[n] - x[n-1]) * fs
    return np.diff(signal) * sample_rate


def square_signal(signal: np.ndarray) -> np.ndarray:
    """Square the signal (make all positive, emphasize peaks)"""
    return signal ** 2


def moving_integration(signal: np.ndarray, window_size: int) -> np.ndarray:
    """Moving window integration"""
    integrated = np.zeros(len(signal))
    for i in range(len(signal)):
        start = max(0, i - window_size + 1)
        integrated[i] = np.mean(signal[start:i+1])
    return integrated


def pan_tompkins_detection(ecg: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Full Pan-Tompkins algorithm for R-wave detection
    
    Returns:
        (processed_signal, r_peak_indices)
    """
    # Step 1: Bandpass filter (5-15 Hz for QRS)
    filtered = bandpass_filter(ecg, sample_rate)
    
    # Step 2: Differentiation
    diffed = differentiate(filtered, sample_rate)
    
    # Step 3: Squaring
    squared = square_signal(diffed)
    
    # Step 4: Moving integration (150ms window)
    window_samples = int(0.15 * sample_rate)
    integrated = moving_integration(squared, window_samples)
    
    # Step 5: Peak detection with adaptive threshold
    # Normalize
    integrated_norm = (integrated - np.mean(integrated)) / np.std(integrated)
    
    # Find peaks
    peaks, properties = find_peaks(
        integrated_norm,
        height=1.5,  # Threshold (adjust based on signal quality)
        distance=int(0.3 * sample_rate),  # Minimum 300ms between beats
        prominence=0.5
    )
    
    return integrated, peaks


def calculate_heart_rate(r_peaks: np.ndarray, sample_rate: int) -> float:
    """Calculate heart rate from R-R intervals"""
    if len(r_peaks) < 2:
        return 0.0
    
    # R-R intervals in seconds
    rr_intervals = np.diff(r_peaks) / sample_rate
    
    # Average heart rate (60 / average RR interval)
    avg_rr = np.mean(rr_intervals)
    heart_rate = 60.0 / avg_rr
    
    return heart_rate


def analyze_ecg_file(wav_path: str, show_plot: bool = True):
    """Load WAV file and perform R-wave detection"""
    # Load WAV
    sample_rate, data = wavfile.read(wav_path)
    
    # Convert to float if int16
    if data.dtype == np.int16:
        ecg = data.astype(np.float64) / 32767.0
    else:
        ecg = data
    
    print(f"Loaded: {wav_path}")
    print(f"Sample rate: {sample_rate} Hz, Duration: {len(ecg)/sample_rate:.1f} s")
    
    # Pan-Tompkins processing
    integrated, r_peaks = pan_tompkins_detection(ecg, sample_rate)
    
    # Calculate heart rate
    heart_rate = calculate_heart_rate(r_peaks, sample_rate)
    print(f"Detected {len(r_peaks)} beats")
    print(f"Estimated heart rate: {heart_rate:.1f} BPM")
    
    # Plot results
    if show_plot:
        fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)
        
        t = np.arange(len(ecg)) / sample_rate
        
        axes[0].plot(t, ecg, linewidth=0.5)
        axes[0].set_title("Raw ECG")
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True, alpha=0.3)
        
        axes[1].plot(t, bandpass_filter(ecg, sample_rate), linewidth=0.5)
        axes[1].set_title("Bandpass Filtered (5-15 Hz)")
        axes[1].set_ylabel("Amplitude")
        axes[1].grid(True, alpha=0.3)
        
        axes[2].plot(t, integrated, linewidth=0.5)
        axes[2].plot(t[r_peaks], integrated[r_peaks], 'ro', markersize=8, label='R-peaks')
        axes[2].set_title("Integrated Signal with Detected R-Peaks")
        axes[2].set_ylabel("Amplitude")
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # R-R intervals
        if len(r_peaks) > 1:
            rr_intervals = np.diff(r_peaks) / sample_rate
            rr_times = t[r_peaks[1:]]
            axes[3].plot(rr_times, rr_intervals * 1000, 'o-', linewidth=1)  # Convert to ms
            axes[3].axhline(y=1000, color='r', linestyle='--', alpha=0.5, label='60 BPM')
            axes[3].axhline(y=600, color='g', linestyle='--', alpha=0.5, label='100 BPM')
            axes[3].set_title("R-R Intervals (Heart Rate Variability)")
            axes[3].set_ylabel("Interval (ms)")
            axes[3].set_xlabel("Time (s)")
            axes[3].legend()
            axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        output_plot = wav_path.replace(".wav", "_analysis.png")
        plt.savefig(output_plot, dpi=150)
        print(f"✓ Saved analysis plot: {output_plot}")
    
    return r_peaks, heart_rate


def main():
    parser = argparse.ArgumentParser(description="R-Wave Detection (Pan-Tompkins)")
    parser.add_argument("input", help="Input WAV file")
    parser.add_argument("--no-plot", action="store_true")
    args = parser.parse_args()
    
    analyze_ecg_file(args.input, show_plot=not args.no_plot)


if __name__ == "__main__":
    main()
