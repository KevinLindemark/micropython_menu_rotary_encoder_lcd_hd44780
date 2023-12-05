from gpio_lcd import GpioLcd
from rotary_encoder import RotaryEncoder
from machine import Pin
from time import sleep
from lcd_menu import LCDMenu
from lmt84 import LMT84

lmt84 = LMT84()

rot_pb = Pin(14, Pin.IN, Pin.PULL_UP)
rot = RotaryEncoder()

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)

lcd.blink_cursor_on()

menu = LCDMenu(lcd, rot, rot_pb)

led1 = Pin(26, Pin.OUT)

# https://maxpromer.github.io/LCD-Character-Creator/ 
lcd_custom_char_degrees = bytearray([0x0E, 0x0A,
                                     0x0E, 0x00,
                                     0x00, 0x00,
                                     0x00, 0x00])

def lcd_temperature_celsius():
    lcd.move_to(1, menu.selected) # moves to selected line
    lcd.putstr("                  ") # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.celsius_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("C")

def lcd_temperature_fahrenheit():
    lcd.move_to(1, menu.selected) # moves to selected line
    lcd.putstr("                  ") # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.fahrenheit_temperature():.1f} ")
    lcd.custom_char(2, lcd_custom_char_degrees)
    lcd.putchar(chr(2))
    lcd.putstr("F")

def lcd_temperature_kelvin():
    lcd.move_to(1, menu.selected) # moves to selected line
    lcd.putstr("                  ") # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"Temp is {lmt84.kelvin_temperature():.1f}K")

def lcd_toggle_led1():
    """Toggle led1"""
    lcd.move_to(1, menu.selected) # moves to selected line
    lcd.putstr("                  ") # delete selected line text by adding whitespaces
    lcd.move_to(1, menu.selected)
    lcd.putstr(f"LED1 is toggled!")
    led1.value(not led1.value())

def test1():
    print("test1")
    
menu.add_menu_item("Temp celsius", lcd_temperature_celsius)
menu.add_menu_item("Temp fahrenheit", lcd_temperature_fahrenheit)
menu.add_menu_item("Temp kelvin", lcd_temperature_kelvin)
menu.add_menu_item("Toggle LED1", lcd_toggle_led1)
menu.add_menu_item("Test1", test1)
menu.add_menu_item("Test2")

menu.display_menu()
menu.run()