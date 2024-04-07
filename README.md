# QTPY2040_Stealth_Mouse_Jiggler
Circuit Python Mouse Jiggle that does not present CIRCUITPY drive or Serial CDC over USB (REPL).

This is an evolultion of the "Mouse_Jiggler_Trinket_M0" found here: https://github.com/dglaude/Mouse_Jiggler_Trinket_M0
It was made possible thanks to an hint by @p3lim in https://github.com/adafruit/circuitpython/issues/9136#

A mouse jiggler is a device that generate tiny mouse mouvement on your computer to avoid it from going into sleep mode.

This version is particular in that it tries to be not visible as anything else than a composite USB device with mouse and keyboard. So the typical CIRCUITPY driver and USB Serial CDC (REPL) interface are disabled (but can be restored for changing the code).

## Feature

* Blink RED/BLUE if there is no USB connection (like when turning off your computer)
* Display a rainbow when the device is actively jiggling the mouse
* Activity can be toggled by double clicking the CAPS LOCK (off->on followed by on->off) by default the rainbow indicate if active (and turn off if desactivated)
* Start in stealth mode. The default mode is stored in microcontroler.nvm[0] and can be switch for next boot by a press on the boot button (that also restart the board when you release)

## Installation

Minimum installation only require the file `code.py`, `boot.py` and a few libraries:
* `adafruit_hid` (folder)
* `neopixel` (mpy file)
* `adafruit_pixelbuf` (mpy file)

Optional is the file `myconfig.py` to change the default behavior.

If you want to customize the behaviour, you can add the file  `muconfig.py` and edit some lines and choose the value you want to use in place of the default.

## Design decision

Design goal:
1) Enable/Disable from keyboard
2) Works on Windows/Linux/Mac
3) Does not modify the computer behavior
4) Visual indication that it is activated or not
5) Stealth mode (no mass storage, no cdc)
6) Stealth mode can be modified with build in hardware (no jumper/soldering)
7) Recover from USB late connection and disconnection (power up, sleep, wake-up, ...)
8) User configurable (all option regrouped in a single file)

## Hardware requirement

* Require the presence of an RGB LED such as NeoPixel (but could work with a DotStar), the code use `board.NEOPIXEL`.
* Require the presence of a button to switch out of stealth mode, the code use `board.BUTTON` (notice that on the QT PY 2040, the boot button can be used as a user button, this is not true for the XIAO RP 2040)
* Require the availability of `microcontroler.nvm[0]` to store the stealt mode status for next reboot.
