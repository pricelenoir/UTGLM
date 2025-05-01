# Golf Launch Monitor

This directory contains all necessary files to operate the **Golf Launch Monitor**, designed to determine the flight trajectory of a golf shot.

## Overview

The **Golf Launch Monitor** utilizes a **Raspberry Pi 5** connected to the **Texas Instruments IWR6843ISK radar module** via a USB to micro-USB cable. The radar module is configured for our specific application and outputs serialized sensor data to the Raspberry Pi via COM port. The Raspberry Pi handles all data input and processing and outputs individual shot metrics via WebSockets to an demo web application for further analysis.


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
3. **Ping Raspberry Pi**: Power the board on and check for a connection via the command line.
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
pi@raspberrypi:~ $ cd UTGLM/glm

pi@raspberrypi:~/UTGLM/glm $ sh setup.sh
```

### 2. IWR6843ISK Set-up
1. **Download Necessary Software**:
   - **Uniflash**: [Download here](https://www.ti.com/tool/UNIFLASH).
   - **FTDI Drivers**: [Download here](https://ftdichip.com/drivers/) for USB-to-UART bridge.
     - Install these drivers and update the COM drivers in the **Device Manager** by navigating to `C:/Program Files/` after installation.
2. **Flash executable onto IWR6843ISK**:
   - Our project uses the default binary provided in the Texas Instrument demo to handle data acquisition.
   - Follow this tutorial to flash the demo executable `docs\xwr68xx_mmw_demo.bin` onto the radar module using Uniflash:
   [`Hardware Setup for IWR6843ISK`](https://www.youtube.com/watch?v=YsIiPGR9k4c).
3. **Connect IWR6843ISK to Raspberry Pi**
   - Ensure that data is being transferred via the COM port by using a tool like `minicom`.


## Using the Launch Monitor

### Configuration
The Texas Instruments **IWR6843ISK** radar module uses its own configuration API for tuning chirp parameters. You can find more information about these parameters in the following files:

- [`docs/programming_chirp_parameters.pdf`](docs/programming_chirp_parameters.pdf) – detailed explanation of each chirp parameter
- [`docs/documentation.cfg`](docs/documentation.cfg) – an annotated example configuration file

To apply a new configuration to the radar, edit the `IWR6843ISK.cfg` file and run the following script:

```bash
pi@raspberrypi:~/UTGLM/glm $ python config.py
```

### Running the Launch Monitor
Once the device is configured, you can start the radar processing server by running:

```bash
pi@raspberrypi:~/UTGLM/glm $ python main.py
```

This script will:
- Host a lightweight WebSocket server to stream shot metrics.
- Connect to the IWR6843ISK.
- Process radar data in real time.
- Generate an estimated 2D launch trajectory.

The data will be streamed and visualized to a Next.js web application found in the [`demo-app/`](../demo-app/) directory.