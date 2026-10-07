🏆 Presentation Quick Reference
Project Title: SAFECHARGE: Dual-Stage Hardware Battery Safety Controller & FPGA Telemetry Engine
Team Members: Prisha & Team (B.Tech ECE, 3rd Year)
Hardware Architecture: ESP32 Sensing Front-End ➔ UART Link ➔ PYNQ-Z2 FPGA Safety Core ➔ Relay Cutoff + Live Jupyter Telemetry Dashboard
Every year, thousands of mobile devices catch fire or suffer permanent damage due to cheap uncertified chargers, voltage surges, and battery thermal runaway—from high-profile recalls like the Samsung Galaxy Note 7 to everyday phone burn incidents during unattended overnight charging.

The core problem is that conventional battery management relies on software OS routines. If an OS freezes, delays, or suffers a kernel panic, battery monitoring halts while charging power remains connected!

To solve this, we created SAFECHARGE—a low-cost, dual-stage hardware-level safety controller. It continuously samples Voltage, Current, and Temperature at high resolution, streams telemetry to a PYNQ-Z2 FPGA hardware state machine, and physically trips a relay cutoff in under 100 milliseconds before thermal runaway can even start. Let us show you our live working demonstration!"
Stage 1 (ESP32 Sensing & Local Display):

Uses ADC1 channels to sample physical transducers (
𝑉
,
𝐼
,
𝑇
V,I,T) and 3 fault-simulation potentiometers.
Drives a local 16×2 I2C character LCD for local status backup.
Transmits real-unit telemetry text frames (V=mV, I=mA, T=centi-C, F, S) every 500 ms over UART.

Stage 2 (PYNQ-Z2 FPGA Hardware Safety Core):

Processes data in Verilog fabric clocked at 125 MHz.
Evaluates parameters concurrently in hardware comparators every clock cycle (zero OS latency).
Exposes values to the PYNQ Linux Processing System (PS) via 32-bit dual-channel AXI GPIO registers.
Displays real-time dark-mode graphs, bar indicators, and event logs on a live Jupyter Notebook dashboard!
Part 3: Live Demonstration Script (Step-by-Step for the Table)
Step 1: Show Normal Monitoring State
What to say: "Currently, the system is in MONITOR (SAFE) state. All parameters are within normal limits (
𝑉
<
5.0
V
V<5.0V, 
𝐼
<
6.5
A
I<6.5A, 
𝑇
<
32
∘
C
T<32
∘
C)."
What to point at:
Show the Green LED illuminated on the board.
Point out the Relay closed supplying power to the load.
Show the 16×2 LCD reading STATE: SAFE.
Point to your laptop screen showing Green progress bars and live telemetry lines on the PYNQ Jupyter Dashboard.
Step 2: Demonstrate Temperature Warning Threshold
Action: Turn POT 3 (Temperature Knob) slowly clockwise.
What to say: "Now, as temperature rises above 
32.0
∘
C
32.0
∘
C, watch the system transition to WARNING state."
What to point at:
Yellow LED lights up.
PYNQ Dashboard bar turns YELLOW, and the event log records State: WARNING.
Step 3: Demonstrate Critical Over-Voltage / Over-Temperature Hard Cutoff
Action: Turn the knob further past the 
40.0
∘
C
40.0
∘
C fault limit (or turn Voltage knob past 
5.5
V
5.5V).
What to say: "The moment temperature crosses 
40.0
∘
C
40.0
∘
C, the FPGA hardware FSM trips an instantaneous Hard Cutoff!"
What to point at:
Relay clicks OFF instantly (<100ms), physically disconnecting load power.
Red LED illuminates and Buzzer sounds the audible alarm.
Dashboard displays RED bars, latches FAULT state, and logs the exact event State: FAULT.
Step 4: Demonstrate Fault Latch & Reset Protocol
Action: Turn the knob back down to a normal value.
What to say: "Notice that even though I turned the temperature knob back down, the system remains latched in FAULT state for safety—it will never automatically re-energize a dangerous battery. It requires an explicit human reset."
Action: Press the physical RESET Push Button.
What to say: "Pressing the RESET button verifies parameters are safe and restores the system to MONITOR (SAFE) charging mode!"
Hardware-Level Determinism:

Unlike microcontrollers that process instructions sequentially in software loops, the PYNQ FPGA evaluates voltage, current, temperature, and spike flags concurrently every single clock cycle (125 MHz).

1-Second Hardware Watchdog Timer:

If the UART wire is disconnected or the ESP32 freezes, the FPGA hardware watchdog timer expires in 1.0 second, automatically de-energizing the relay to fail-safe OPEN state.

5% Hysteresis Anti-Chatter Protection:

State transitions incorporate a 5% deadband below thresholds to eliminate mechanical relay chatter when sensor signals hover near decision boundaries.

Boot-Strapping Isolation & Star Grounding:

220
Ω
220Ω resistors isolate GPIO2 and GPIO15 to prevent silicon boot-strap lockup.
All grounds (ESP32, ACS712, Relay, LCD, PYNQ) join at a unified single-point Star Ground to eliminate ADC offset drift and UART corruption.


We have done this project for our hackathon that was held in SJC Institute of technology on October 8 2026.
Presented by Students of BMSIT&M.
