import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_ssd1306 import SSD1306_I2C

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.extensions.led import LED

import busio
import digitalio

# Initialize keyboard
keyboard = KMKKeyboard()

# Macros
macros = Macros()
keyboard.modules.append(macros)

# LED setup (example: LED on pin D13)
led = LED(led_pin=board.LED)  # Adjust to your actual LED pin if different
keyboard.extensions.append(led)

# Define key pins - pyramid layout:
#    [ D2 ]
# [ D3, D4, D1 ]
PINS = [board.D3, board.D4, board.D1, board.D2]  # Order matters: bottom-left to right, then top

keyboard.matrix = KeysScanner(pins=PINS, value_when_pressed=False)

# Setup I2C and OLED display (SSD1306)
i2c = busio.I2C(scl=board.SCL, sda=board.SDA)
display = SSD1306_I2C(128, 32, i2c)
display.fill(0)
display.show()

# Text label setup
text_area = label.Label(terminalio.FONT, text="Ready", x=0, y=12)
main_group = displayio.Group()
main_group.append(text_area)
display.show(main_group)

# Helper function to update OLED text
def update_display(text):
    text_area.text = text
    display.show(main_group)

# Define keymap
keyboard.keymap = [
    [
        KC.LEFT,   # D3 - Bottom Left
        KC.DOWN,   # D4 - Bottom Middle
        KC.RIGHT,  # D1 - Bottom Right
        KC.UP
    ]
]

# Hook to handle OLED and LED updates
def on_key_event(key, pressed, key_number):
    if pressed:
        update_display(f"Key {key_number} pressed")
        led.set_led(True)
    else:
        update_display("Ready")
        led.set_led(False)

keyboard.after_matrix_scan.append(on_key_event)

# Start
if __name__ == '__main__':
    keyboard.go()
