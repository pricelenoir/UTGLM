# Golf Launch Monitor

This directory contains all necessary files to operate the **Golf Launch Monitor**, designed to track and measure the flight trajectory of a golf shot.

## Overview

The **Golf Launch Monitor** utilizes a **Raspberry Pi 4** connected to the **Texas Instruments IWR6843ISK radar module** via a USB to micro-USB cable. The radar module is configured for our specific application and outputs serialized sensor data to the Raspberry Pi via COM port. The Raspberry Pi handles all data input and processing and outputs individual shot metrics via Bluetooth to an iOS application for further analysis and display.


## Setup Instructions

### 1. Raspberry Pi Set-up
#### 1.1 Install OS
1. **Raspberry Pi Imager**: Download and install [Raspberry Pi Imager](https://www.raspberrypi.org/software/).
2. **Flash Operating System**: 
   - Insert microSD card into reader and open Imager.
   - Select correct device model.
   - Select Raspberry Pi OS LITE (64-bit).
   - Select microSD card reader as storage.
   - Edit custom OS settings:
      - **Hostname**: Use default hostname (raspberrypi.local).
      - **Login**: Set username and password for remote login.
      - **Network**: Select Configure wireless LAN.
      - **Enable SSH**: In the services tab, enable SSH with password authentication.
      - **Save and apply custom OS settings**
3. **Ping Raspberry Pi**: Power the board on and check for a connection.
```bash
ping raspberrypi.local
```
4. **SSH into Raspberry Pi**: Use SSH to access the Raspberry Pi for remote development.
```bash
ssh-keygen -R raspberrypi.local
ssh pi@raspberrypi.local
```
5. **Install Git**: Update and install git to pull UTGLM repo.
```bash
pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get install -y git
```
6. **Pull Git repository**: Clone UTGLM code base.
```bash
pi@raspberrypi:~ $ git clone https://github.com/pricelenoir/UTGLM.git
```
7. **Run setup script**:
```bash
cd UTGLM/glm
sh setup.sh
```

### 2. IWR6843ISK Set-up
#### 2.1 On Windows Machine
1. **Download Necessary Software**:
   - **mmWave SDK**: [Download here](https://www.ti.com/tool/MMWAVE-SDK).
   - **mmWave Studio**: Request access as a student through [TI’s website](https://www.ti.com/tool/MMWAVE-STUDIO).
   - **Code Composer Studio**: [Download here](https://www.ti.com/tool/CCSTUDIO).
   - **Uniflash**: [Download here](https://www.ti.com/tool/UNIFLASH).
   - **FTDI Drivers**: [Download here](https://ftdichip.com/drivers/) for USB-to-UART bridge.
     - Install these drivers and update the COM drivers in the **Device Manager** by navigating to `C:/Program Files/` after installation.
2. **Install TI Cloud Agent**:
   - **TICloud Agent Bridge Chrome Extension** and **TI Cloud Agent**: Used for web-based demo visualizer and real-time monitoring.
3. **Check out additional resources**
   - Add other stuff here (i.e. demo visualizer, mmwave training, etc.)

   
#### 2.2 Radar Module Setup
1. **Connect the IWR6843ISK Radar Module**:
   - Use the USB to micro-USB cable to connect the radar module to your PC.
   - Verify the connection and ensure it is properly recognized on your Windows machine.

2. **Configure Radar Module**:
   - Using **mmWave Studio** or **Code Composer Studio**, configure the IWR6843ISK for your specific golf tracking application.
   - Load the firmware and necessary parameters into the radar module to begin capturing data.
