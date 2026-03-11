/*
 * ECG Monitor Firmware for CH32V203
 * 
 * Features:
 * - ADC sampling from instrumentation amp (PA1)
 * - Pan-Tompkins R-wave detection
 * - Heart rate calculation
 * - Serial/WebSerial output
 * - Optional: TinyML anomaly detection
 *
 * Hardware:
 * - ECG Front-End: AD620/INA128 → PA1 (ADC1_CH1)
 * - UART: PA2(TX), PA3(RX) @ 115200
 * - Safety: Battery only, galvanic isolation
 *
 * ⚠️ SAFETY WARNING: Do not connect to PC while electrodes attached!
 */

#include "ch32v20x.h"
#include <stdio.h>
#include <string.h>

// ============= Configuration =============
#define ECG_SAMPLE_RATE     500         // 500Hz sampling (ECG standard)
#define BUFFER_SIZE         250         // 1 second buffer
#define NUM_TAPS            31          // Filter taps for Pan-Tompkins

// ============= Global Buffers =============
int16_t ecg_buffer[BUFFER_SIZE];
volatile uint16_t ecg_index = 0;
volatile uint8_t buffer_ready = 0;

// Pan-Tompkins intermediate signals
int16_t filtered[BUFFER_SIZE];
int16_t integrated[BUFFER_SIZE];
uint16_t r_peaks[BUFFER_SIZE];
uint8_t num_peaks = 0;

// ============= Function Prototypes =============
void SystemInit(void);
void ADC_Init(void);
void Timer_Init(void);
void UART_Init(void);

void Process_ECG_Buffer(void);
void Pan_Tompkins_Filter(int16_t* input, int16_t* output, int len);
uint8_t Detect_R_Peaks(int16_t* signal, uint16_t* peaks, int len);
float Calculate_Heart_Rate(uint16_t* peaks, uint8_t count, int sample_rate);

void Send_ECG_Data(void);
void Send_Heart_Rate(float bpm);

// ============= Main =============
int main(void)
{
    SystemInit();
    
    UART_Init();      // For PC/WebSerial communication
    ADC_Init();       // For ECG input
    Timer_Init();     // For 500Hz sampling
    
    printf("ECG Monitor Ready\n");
    printf("SAFETY: Ensure battery operation only!\n");
    
    while(1)
    {
        if(buffer_ready)
        {
            buffer_ready = 0;
            
            // Process 1-second buffer
            Process_ECG_Buffer();
            
            // Send raw data (for PC visualization)
            Send_ECG_Data();
            
            // Send heart rate
            if(num_peaks > 1)
            {
                float bpm = Calculate_Heart_Rate(r_peaks, num_peaks, ECG_SAMPLE_RATE);
                Send_Heart_Rate(bpm);
                printf("HR: %.1f BPM, Peaks: %d\n", bpm, num_peaks);
            }
        }
    }
}

// ============= ADC Interrupt =============
void ADC1_2_IRQHandler(void) __attribute__((interrupt));
void ADC1_2_IRQHandler(void)
{
    if(ADC1->STATR & ADC_STATR_EOC)
    {
        ecg_buffer[ecg_index++] = (int16_t)(ADC1->RDATAR & 0xFFF);  // 12-bit ADC
        
        if(ecg_index >= BUFFER_SIZE)
        {
            ecg_index = 0;
            buffer_ready = 1;
        }
        
        ADC1->STATR = ~ADC_STATR_EOC;
    }
}

// ============= Signal Processing =============
void Process_ECG_Buffer(void)
{
    // Pan-Tompkins processing
    Pan_Tompkins_Filter(ecg_buffer, filtered, BUFFER_SIZE);
    
    // R-peak detection
    num_peaks = Detect_R_Peaks(filtered, r_peaks, BUFFER_SIZE);
}

// Simplified Pan-Tompkins bandpass filter
void Pan_Tompkins_Filter(int16_t* input, int16_t* output, int len)
{
    // Lowpass: y[n] = 2y[n-1] - y[n-2] + x[n] - 2x[n-6] + x[n-12]
    // Highpass: y[n] = y[n-1] - x[n] + x[n-32]
    // Combined bandpass effect (5-15Hz)
    
    int16_t lp[BUFFER_SIZE], hp[BUFFER_SIZE];
    
    // Lowpass filter (cutoff ~11Hz)
    lp[0] = input[0];
    lp[1] = input[1];
    for(int i = 2; i < len; i++)
    {
        lp[i] = 2*lp[i-1] - lp[i-2] + input[i] - 2*input[i-6] + input[i-12];
    }
    
    // Highpass filter (cutoff ~5Hz)
    hp[0] = lp[0];
    for(int i = 1; i < len; i++)
    {
        int prev = (i >= 32) ? lp[i-32] : 0;
        hp[i] = hp[i-1] - lp[i] + prev;
    }
    
    // Square and integrate
    for(int i = 0; i < len; i++)
    {
        int16_t squared = (hp[i] * hp[i]) >> 8;  // Scale down
        
        // Moving integration (150ms window = 75 samples @ 500Hz)
        int sum = 0;
        int count = 0;
        for(int j = 0; j <= 75 && i-j >= 0; j++)
        {
            sum += squared;
            count++;
        }
        output[i] = sum / count;
    }
}

// Simple peak detection with adaptive threshold
uint8_t Detect_R_Peaks(int16_t* signal, uint16_t* peaks, int len)
{
    uint8_t count = 0;
    
    // Calculate signal statistics for adaptive threshold
    int32_t mean = 0;
    for(int i = 0; i < len; i++)
    {
        mean += signal[i];
    }
    mean /= len;
    
    int32_t variance = 0;
    for(int i = 0; i < len; i++)
    {
        int32_t diff = signal[i] - mean;
        variance += diff * diff;
    }
    int16_t std_dev = sqrt(variance / len);
    
    // Threshold: mean + 1.5 * std_dev
    int16_t threshold = mean + (3 * std_dev) / 2;
    
    // Find peaks
    int min_distance = ECG_SAMPLE_RATE * 0.3;  // 300ms refractory period
    
    for(int i = 1; i < len - 1; i++)
    {
        if(signal[i] > threshold && 
           signal[i] > signal[i-1] && 
           signal[i] > signal[i+1])
        {
            // Check minimum distance from last peak
            if(count == 0 || (i - peaks[count-1]) >= min_distance)
            {
                peaks[count++] = i;
            }
        }
    }
    
    return count;
}

float Calculate_Heart_Rate(uint16_t* peaks, uint8_t count, int sample_rate)
{
    if(count < 2) return 0;
    
    // Average R-R interval
    int32_t total_rr = 0;
    for(int i = 1; i < count; i++)
    {
        total_rr += (peaks[i] - peaks[i-1]);
    }
    
    float avg_rr = (float)total_rr / (count - 1);
    float bpm = (60.0 * sample_rate) / avg_rr;
    
    return bpm;
}

// ============= Output Functions =============
void Send_ECG_Data(void)
{
    // Send raw ECG data as binary packet
    // Format: SYNC(0xAA, 0x55) + length + data[250] + checksum
    printf("DATA_START\n");
    
    for(int i = 0; i < BUFFER_SIZE; i++)
    {
        printf("%d,", ecg_buffer[i]);
    }
    
    printf("DATA_END\n");
}

void Send_Heart_Rate(float bpm)
{
    printf("HR:%.1f\n", bpm);
}

// ============= Peripheral Init =============
void UART_Init(void)
{
    // PA2 = TX, PA3 = RX
    GPIOA->CFGLR &= ~(0xF << 8);
    GPIOA->CFGLR |= (GPIO_Speed_50MHz | GPIO_AF_PP) << 8;
    
    GPIOA->CFGLR &= ~(0xF << 12);
    GPIOA->CFGLR |= GPIO_IPU << 12;
    
    RCC->APB2PCENR |= RCC_APB2Periph_USART1 | RCC_APB2Periph_GPIOA;
    
    USART1->BRR = 26;  // 72MHz / 115200 (CH32V203 @ 72MHz)
    USART1->CTLR1 = USART_CTLR1_TE | USART_CTLR1_RE | USART_CTLR1_UE;
}

void ADC_Init(void)
{
    // PA1 = ADC1_IN1
    GPIOA->CFGLR &= ~(0xF << 4);
    GPIOA->CFGLR |= GPIO_Mode_AIN << 4;
    
    RCC->APB2PCENR |= RCC_APB2Periph_ADC1 | RCC_APB2Periph_GPIOA;
    
    ADC1->CTLR2 = ADC_CTLR2_ADON | ADC_CTLR2_CONT;
    ADC1->RSQR3 = ADC_Channel_1;
    
    ADC1->CTLR1 |= ADC_CTLR1_EOCIE;
    NVIC_EnableIRQ(ADC1_2_IRQn);
}

void Timer_Init(void)
{
    // Timer2 for ADC trigger @ 500Hz
    RCC->APB1PCENR |= RCC_APB1Periph_TIM2;
    
    Timer2->PSC = 72 - 1;  // 72MHz / 72 = 1MHz
    Timer2->ATRLR = 2000 - 1;  // 1MHz / 2000 = 500Hz
    Timer2->SWEVGR = 1;
    Timer2->CTLR1 = 1;
    
    Timer2->CTLR2 = TIM_TRGOSource_Update;
    ADC1->CTLR2 |= ADC_CTLR2_EXTSEL | ADC_CTLR2_EXTTRIG;
}

// ============= Printf Support =============
int _write(int fd, char *ptr, int len)
{
    for(int i = 0; i < len; i++)
    {
        while(!(USART1->STATR & USART_STATR_TC));
        USART1->DATAR = *ptr++;
    }
    return len;
}
