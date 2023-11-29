from gpio_lcd import GpioLcd
from rotary_encoder import RotaryEncoder
from machine import Pin
from time import sleep
from lcd_menu import LCDMenu

rot_pb = Pin(14, Pin.IN, Pin.PULL_UP)
rot = RotaryEncoder()
#from rotary_encoder import rotary_encoder_tester
lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)
lcd.blink_cursor_on()
menu = LCDMenu(lcd, rot, rot_pb)

def cb_menu_1():
    print("menu 1")

menu.add_menu_item("Menu 1", cb_menu_1)
menu.add_menu_item("Menu 2")
menu.add_menu_item("Menu 3")
menu.add_menu_item("Menu 4")

menu.display_menu()
menu.run()