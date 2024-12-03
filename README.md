# University of Tennessee, Knoxville — Golf Launch Monitor

## Senior Design Project (ME450/460) 2024-2025

### Faculty Advisor:
- Dr. William Miller

### Team Members:
- Caden Branch
- Jake Wurms
- Noah Walker
- Price LeNoir
- Tyler Reed


## Project Overview

We are designing a Doppler radar-based golf launch monitor to be used in tandem with a weight distribution board equipped with load cells. This system is designed to determine a user's center of mass throughout their golf swing and provide real-time feedback to improve swing mechanics.

This repository contains the source code for the embedded devices that interact with:
- **Load cells**: Measure weight distribution and center of mass shifts.
- **Radar evaluation module**: Used to measure club head speed, ball speed, launch angle, and launch direction.
- **Raspberry Pi**: Manages the overall program, processes sensor data, and handles communication via Bluetooth.
- **iOS Mobile Application**: A companion app, deployable through TestFlight, to display data and insights from the system for user interaction and analysis.
