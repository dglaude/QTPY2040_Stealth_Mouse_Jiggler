import supervisor
supervisor.set_next_code_file(None, reload_on_error=True)
import microcontroller

# Default value if no "myconfig.py" are present
RAINBOW = True           # Display a rainbow when active
RAINBOW_DELAY = 50       # Mouse movement occurs every 256*RAINBOW_DELAY ticks, that mean every rainbow rotation reach red.
AUTO_START = True        # Do you want jiggling to start automatically.
WARN_NO_USB = True       # Do you want high speed blinking RED/BLUE when USB is not connected.

try:
    from myconfig import *
except ImportError:
    pass

import board
import usb_hid
import neopixel
import digitalio
from rainbowio import colorwheel
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard

# Start of code from: https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html
_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff
# End of code from: https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html

btn = digitalio.DigitalInOut(board.BUTTON)
btn.direction = digitalio.Direction.INPUT
btn.pull = digitalio.Pull.UP

last = supervisor.ticks_ms()
color_time = last

### Warning blink RED and BLUE
num_pixels = 1
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.1, auto_write=False)
rc_index = 0

blink = True
if WARN_NO_USB:
    while not supervisor.runtime.usb_connected:
        last = supervisor.ticks_ms()
        if ticks_diff (last, color_time) > RAINBOW_DELAY:
            color_time = last
            if blink:
                pixels[0] = colorwheel(0)
                pixels.show()
            else:
                pixels[0] = colorwheel(127)
                pixels.show()
            blink = not blink
    pixels[0] = (0,0,0)
    pixels.show()

infinity_direction = [(0,2),(2,2),(2,0),(2,-3),(2,-3),(2,0),(2,2),(0,2),(-2,2),(-2,0),(-3,-3),(-3,-3),(-2,0),(-2,2)]
octogonal_direction = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]
iterator = iter(octogonal_direction)
distance=2

active = False
jiggle = AUTO_START

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

raise_flag = False
new_caps = kbd.led_on(Keyboard.LED_CAPS_LOCK)

while True:
    last = supervisor.ticks_ms()

    if not btn.value:
        microcontroller.nvm[0] = int(not microcontroller.nvm[0])
        while not btn.value:
            pass
        microcontroller.reset()

    old_caps = new_caps
    new_caps = kbd.led_on(Keyboard.LED_CAPS_LOCK)

    if new_caps and not old_caps:
        raise_time = last
        raise_flag = True

    if raise_flag:
        since_when = ticks_diff (last, raise_time)
        if ticks_diff (last, raise_time) > 1000:
            raise_flag = False
        else:
            if not new_caps:
                jiggle = not jiggle
                color_time = last
                if not jiggle:
                    pixels[0] = (0,0,0)
                    pixels.show()
                raise_flag = False

    if jiggle:
        if ticks_diff (last, color_time) > RAINBOW_DELAY:
            color_time = last
            rc_index = (rc_index + 1) & 255
            pixels[0] = colorwheel(rc_index)
            if RAINBOW:
                pixels.show()
            if rc_index == 0:
                try:
                    element = next(iterator)
                except StopIteration:
                    iterator = iter(octogonal_direction)
                    element = next(iterator)
                mouse.move(x=distance*element[0], y=distance*element[1])
