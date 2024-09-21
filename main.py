# SPDX-License-Identifier: MIT

import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import neopixel
import digitalio
from adafruit_debouncer import Debouncer
from analogio import AnalogOut
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility

# Set up the on-off toggle
NeoToggle = False  # Off
NeoToggleRev = False  # Forward/Reverse

# Set up digital pins for switches
pin5 = digitalio.DigitalInOut(board.D5)
pin5.direction = digitalio.Direction.INPUT
pin5.pull = digitalio.Pull.UP
switch5 = Debouncer(pin5)

pin6 = digitalio.DigitalInOut(board.D6)
pin6.direction = digitalio.Direction.INPUT
pin6.pull = digitalio.Pull.UP
switch6 = Debouncer(pin6)

# Initialize I2C for sensors
i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)

# Set up AnalogOut on A0 for acceleration and A1 for direction
analog_out_accel = AnalogOut(board.A0)
analog_out_dir = AnalogOut(board.A1)

# Function to calculate voltage based on lux sensor
def calc_voltage(lux):
    if not NeoToggleRev:
        # Reverse mode: 50 lux = 0V, 1000 lux = 1.774V (stop)
        voltage = (lux - 50) / (1000 - 50) * 1.774
        return max(0, min(1.774, voltage))  # Clamp between 0 and 1.774V
    else:
        # Forward mode: 50 lux = 3.3V (fastest), 1000 lux = 1.774V (stop)
        voltage = 3.3 - ((lux - 50) / (1000 - 50) * (3.3 - 1.774))
        return max(1.774, min(3.3, voltage))  # Clamp between 1.774 and 3.3V

# Function to set the analog output based on voltage
def set_analog_output(analog_out, voltage):
    dac_value = int((voltage / 3.3) * 65535)
    analog_out.value = dac_value  # Set the analog output to the calculated value

# Handle toggle switch for on/off and forward/reverse
def on_off(wait):
    global NeoToggle
    global NeoToggleRev

    switch5.update()
    if switch5.fell:
        NeoToggle = not NeoToggle

    switch6.update()
    if switch6.fell:
        NeoToggleRev = not NeoToggleRev

    if NeoToggleRev:
        print("Mode: Reverse")
    else:
        print("Mode: Forward")

    print(f"Toggle: {NeoToggle}, Reverse: {NeoToggleRev}")
    time.sleep(wait)

# Control vehicle movement based on x-axis acceleration (for turning)
def control_vehicle_direction(x_accel):
    print(x_accel)
    if x_accel < -3:
        print("Turning right...")
        # Max voltage for turning right
        set_analog_output(analog_out_dir, 3.3)

    elif x_accel > 3:
        print("Turning left...")
        # Min voltage for turning left
        set_analog_output(analog_out_dir, 0.00001)

    else:
        print("Neutral...")
        # Neutral voltage
        set_analog_output(analog_out_dir, 1.774)

# Main loop
while True:
    on_off(0.01)

    # Check color sensor readiness
    while not apds.color_data_ready:
        on_off(0.1)

    if NeoToggle:
        time.sleep(0.01)
        # Accelerometer readings for vehicle control
        acceleration = accel_gyro.acceleration
        x_accel, y_accel, z_accel = acceleration
        control_vehicle_direction(x_accel)

        # Color sensor for lux-based voltage control
        r, g, b, c = apds.color_data
        lux = colorutility.calculate_lux(r, g, b)

        # Set analog output based on lux
        voltage = calc_voltage(lux)
        set_analog_output(analog_out_accel, voltage)

        # Print the values for debugging
    #    print(f"Lux: {lux:.2f}, Voltage (Accel): {voltage:.3f} V")
      #  print(f"Acceleration (x, y, z): {x_accel:.2f}, {y_accel:.2f}, {z_accel:.2f}")

    on_off(0.01)
    time.sleep(0.01)


