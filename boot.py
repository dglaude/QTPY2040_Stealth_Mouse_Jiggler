import storage
import microcontroller
import usb_cdc, usb_hid, usb_midi

if microcontroller.nvm[0] == 0:
    storage.disable_usb_drive()
    usb_cdc.disable()
    usb_midi.disable()
    usb_hid.enable((usb_hid.Device.MOUSE,usb_hid.Device.KEYBOARD))       # Enable just MOUSE and KEYBOARD.
else:
    storage.enable_usb_drive() # probably redundant
