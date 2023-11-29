import machine
import utime
import uasyncio as asyncio

class LCDMenu:
    def __init__(self, lcd, encoder, button):
        self.lcd = lcd
        self.encoder = encoder
        self.button = button
        self.menu_items = []  # A list to store menu items
        self.current_menu = 0  # Index of the current menu
        self.selected_item = 0  # Index of the selected item in the current menu

        self.encoder_last_state = None  # Store the last state of the encoder
        self.encoder_button_pressed = False  # Flag to track button press

        self.initialize_lcd()
        self.initialize_encoder()
        self.initialize_button()

    def button_callback(self, pin):
        # Callback function for button press
        if self.encoder_button_pressed == False:
            print("pressed button")
            self.encoder_button_pressed = True

    def initialize_lcd(self):
        # Initialize and clear the LCD display
        #self.lcd.init()
        self.lcd.clear()
        self.lcd.move_to(0, 0)

    def initialize_encoder(self):
        # Initialize the rotary encoder
        self.encoder_last_state = self.encoder.re_full_step()

    def initialize_button(self):
        # Initialize the button
        self.button.irq(handler=self.button_callback, trigger=machine.Pin.IRQ_FALLING)

    def add_menu_item(self, text, callback=None):
        # Add a menu item to the current menu
        self.menu_items.append({"text": text, "callback": callback})

    def display_menu(self):
        # Display the current menu
        self.lcd.clear()
        
        for selected in range(len(self.menu_items)):
            self.lcd.move_to(1, selected)
            self.lcd.putstr(self.menu_items[selected]["text"])
        self.lcd.move_to(0, self.selected_item)
        self.lcd.blink_cursor_on()
            
    def navigate_menu(self):
        while True:
            # Read the current state of the encoder
            encoder_state = self.encoder.re_full_step()
            #print(encoder_state)
            # Check for clockwise rotation
            if encoder_state == 1:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                print("Selected item: ", self.selected_item)
                self.display_menu()
            # Check for counterclockwise rotation
            elif encoder_state == -1:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                print("Selected item: ", self.selected_item)
            # Update the LCD display
                self.display_menu()

            # Update the last state of the encoder
            self.encoder_last_state = encoder_state

            # Check if the button is pressed
            if self.encoder_button_pressed:
                callback = self.menu_items[self.selected_item]["callback"]
                if callback:
                    callback()

            if self.encoder_button_pressed == True:
                await asyncio.sleep_ms(200)  # Adjust the delay as needed
                # Reset the button state
                self.encoder_button_pressed = False
            
            

    def run(self):
        # Start the navigation loop
        loop = asyncio.get_event_loop()
        loop.create_task(self.navigate_menu())
        loop.run_forever()
