# PiicoDev® Magnetometer QMC6310 MicroPython Module

This is the firmware repo for the [Core Electronics PiicoDev® Magnetometer QMC6310](https://core-electronics.com.au/catalog/product/view/sku/CE07937)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guides](https://piico.dev/p15)

## Details
### `PiicoDev_QMC6310(bus=, freq=, sda=, scl=, addr=0x1C, odr=0, osr1=0, osr2=3, range=3000, sign_x=0, sign_y=1, sign_z=1, cal_filename='calibration.cal')`
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
range     | int  | 200, 800, 1200, 3000 microTesla | 200                    | Range. Larger ranges are less sensitive.
sign_x    | int  | 0, 1             | 0                                     | Sign to represent the polarity of the magnetic field. 0 Matches the silk screen
sign_y    | int  | 0, 1             | 1                                     | Sign to represent the polarity of the magnetic field. 1 Matches the silk screen
sign_z    | int  | 0, 1             | 1                                     | Sign to represent the polarity of the magnetic field. 1 Matches the silk screen
cal_filename | string |  | 'calibration.cal' | If more than one magnetometer (for example on seperate I2C buses or if an I2C mux is used), use a different filename for each. If set to `None` calibration is skipped.

### `PiicoDev_QMC6310.readMagnitude()`
Reads the magnetic field magnitude using the calibration generated during the calibration routine if available.  Magnitude range is configurable using PiicoDev_QMC6310.setRange().
Parameter   | Type  | Range                    | Description | Unit
----------- | ----- | ------------------------ | ----------- | ------
returned    | float | 0.0 to (200.0 to 3000.0) | Magnitude field strength | uT

### `PiicoDev_QMC6310.readHeading()`
Reads the magnetic field bearing from true north.  If no declination is provided the result is a bearing from magnetic north.  Uses the calibration generated during the calibration routine if available.
Parameter   | Type  | Range        | Description | Unit
----------- | ----- | ------------ | ----------- | ------
returned    | float | 0.0 to 360.0 | Bearing from true north or magnetic north if no declination is set | deg

### `PiicoDev_QMC6310.readPolar()`
Reads the raw magnetic field magnitude and angle (degrees) in the X and Y plane.  Magnitude range is configurable using PiicoDev_QMC6310.setRange().
Parameter   | Type  | Range                   | Description | Unit
----------- | ----- | ----------------------- | ----------- | ----
**Returns** | **Dictionary**
polar       | float | 0.0 to 360.0            | Raw bearing from magnetic north | deg
Gauss       | float | 0.0 to (2.0 to 30.0)    | Magnetic field strength | Gauss
uT          | float | 0.0 to (200.0 to 3000.0 | Magnitude field strength | uT

### `PiicoDev_QMC6310.read()`
Reads the X, Y and Z components of the magnetic field.
Parameter   | Type | Range           | Description
----------- | ---- | --------------- | -----------
**Returns** | **Dictionary**
x           | float  | 0.0 to (200.0 to 3000.0 | X magnetic field component
y           | float  | 0.0 to (200.0 to 3000.0 | Y magnetic field component
z           | float  | 0.0 to (200.0 to 3000.0 | Z magnetic field component

### `PiicoDev_QMC6310.calibrate()`
Routine to calibrate the magnetometer.  Rotate the magnetometer in the X and Y or X, Y, & Z directions until the routine is complete.

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
range     | int  | 200, 800, 1200, 3000 | Set the maximum range in microtesla.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
