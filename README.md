<!-- TODO How to use this template
Follow these commented instructions to build the repo.
Delete the instructions as you go, to keep for a cleaner final file.
 -->

<!-- TODO Initialise the repo with the following two files:
 The MicroPython Module for this device with name: "PiicoDev_[DEVICE MFN].py". Eg for temperature sensor TMP117: PiicoDev_TMP117.py
 A (tested) main.py file
-->


<!-- TODO update title to be descriptive. Eg.
PiicoDev® [Description] [Part#] MicroPython Module
PiicoDev® Precision Temperature Sensor TMP117 MicroPython Module -->
# PiicoDev® Template MicroPython Module

<!-- TODO update link URL with CE SKU -->
<!-- TODO update link title -->
This is the firmware repo for the [Core Electronics PiicoDev® XXXXXX](https://core-electronics.com.au/catalog/product/view/sku/XXXXXX)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

<!-- TODO update tutorial link with the device tinyurl eg. piico.dev/p1
See the [Quickstart Guide](https://piico.dev/pX)
 -->

<!-- TODO verify the tested-devices list -->
This module has been tested on:
 - Micro:bit v2
 - Raspberry Pi Pico
 - Raspberry Pi SBC

## Details
### `PiicoDev_QMC6310(bus=, freq=, sda=, scl=, addr=0x1C, odr=0, osr1=0, osr2=3, range=3)`
Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
bus       | int  | 0, 1             | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq      | int  | 100-1000000      | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda       | Pin  | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl       | Pin  | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only
addr      | int  | 0x1C             | 0x1C                                  | This address cannot be changed
odr       | int  | 0 - 3            | 0                                     | 0: 10Hz, 1: 50Hz, 2: 100Hz, 3: 200Hz
osr1      | int  | 0 - 3            | 0                                     | 0: 4, 2: 4, 3: 2, 4: 1
osr2      | int  | 0 - 3            | 3                                     | 0: 1, 1: 2, 2: 4, 4: 8
range     | int  | 0 - 3            | 3                                     | 0: 30Gauss, 1: 12Gauss, 2: 8Gauss, 3: 2Gauss

### `PiicoDev_QMC6310.readTruePolar(declination)`
Reads the magnetic field angle in the X and Y plane using calibration offsets and given declination.
Parameter   | Type  | Range       | Description | Unit |
----------- | ----- | ----------- | --------------------
declination | float | 0.0 - 360.0 | Magnetic declination | deg
**Returns** | (**Dictionary**)
polar_true  | float | 0.0 to 360.0            | Bearing from true north | deg

### `PiicoDev_QMC6310.readPolarCal()`
Reads the magnetic field magnitude and angle (degrees) in the X and Y plane using calibration offsets.
Parameter   | Type  | Range                   | Description | Unit |
----------- | ----- | ----------------------- | ----------- | ---- |
**Returns** | (**Dictionary**)
polar_cal   | float | 0.0 to 360.0            | Calibrated bearing from magnetic north| deg
Gauss_cal   | float | 0.0 to (2.0 to 30.0)    | Magnetic field strength. Range is configurable using PiicoDev_QMC6310.setRange() | Gauss
uT_cal      | float | 0.0 to (200.0 to 3000.0 | Magnitude field strength | uT

### `PiicoDev_QMC6310.readPolar()`
Reads the raw magnetic field magnitude and angle (degrees) in the X and Y plane.
Parameter   | Type  | Range                   | Description | Unit |
----------- | ----- | ----------------------- | ----------- | ---- |
**Returns** | (**Dictionary**)
polar       | float | 0.0 to 360.0            | Raw bearing from magnetic north | deg
Gauss       | float | 0.0 to (2.0 to 30.0)    | Magnetic field strength. Range is configurable using PiicoDev_QMC6310.setRange() | Gauss
uT          | float | 0.0 to (200.0 to 3000.0 | Magnitude field strength | uT

### `PiicoDev_QMC6310.read()`
Reads the X, Y and Z components of the magnetic field.
Parameter   | Type | Range           | Description
----------- | ---- | --------------- | -----------
**Returns** | **Dictionary**
x           | int  | -32768 to 32767 | X magnetic field component
y           | int  | -32768 to 32767 | Y magnetic field component
z           | int  | -32768 to 32767 | Z magnetic field component
x_cal       | int  | -32768 to 32767 | X magnetic field component using calibration offsets
y_cal       | int  | -32768 to 32767 | Y magnetic field component using calibration offsets
z_cal       | int  | -32768 to 32767 | Z magnetic field component using calibration offsets

### `PiicoDev_QMC6310.calibrate()`
Routine to calibrate the magnetometer.

### `PiicoDev_QMC6310.setOutputDataRate(odr)`
Sets the Output Data Rate.
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
odr       | int  | 0 to 3 | 0: 10Hz, 1: 50Hz, 2: 100Hz, 3: 200Hz

### `PiicoDev_QMC6310.setOverSamplingRatio(osr1)`
Sets the Over Sampling Ratio.
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
osr1      | int  | 0 to 3 | 0: 4, 2: 4, 3: 2, 4: 1

### `PiicoDev_QMC6310.setOverSamplingRate(osr2)`
Sets the Over Sampling Rate.
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
osr2      | int  | 0 to 3 | 0: 1, 1: 2, 2: 4, 4: 8

### `PiicoDev_QMC6310.setRange(range)`
Sets the Range.
Parameter | Type | Range  | Description
--------- | ---- | ------ | -----------
range     | int  | 0 to 3 | 0: 30Gauss, 1: 12Gauss, 2: 8Gauss, 3: 2Gauss

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
