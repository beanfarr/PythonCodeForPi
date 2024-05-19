import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for Set 2
TRIG = 18
ECHO = 23
RED_LED = 17
YELLOW_LED =27
GREEN_LED = 22
PHOTO_RES = 26

# GPIO pin setup
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(PHOTO_RES, GPIO.IN)

# Initial LED state
GPIO.output(GREEN_LED, GPIO.HIGH)
GPIO.output(YELLOW_LED, GPIO.LOW)
GPIO.output(RED_LED, GPIO.LOW)

# Distance function
def distance():
    GPIO.output(TRIG, False)
    time.sleep(0.1)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start, pulse_end = 0, 0

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    timeout = time.time() + 1
    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    if time.time() >= timeout:
        return 99999

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150
    distance_cm = round(distance_cm, 2)

    return distance_cm

# Photoresistor function
def read_photoresistor():
    GPIO.setup(PHOTO_RES, GPIO.OUT)
    GPIO.output(PHOTO_RES, GPIO.LOW)
    time.sleep(0.1)
    
    GPIO.setup(PHOTO_RES, GPIO.IN)
    start_time = time.time()
    while GPIO.input(PHOTO_RES) == GPIO.LOW:
        pass
    end_time = time.time()
    resistance = end_time - start_time
    
    m = 1000
    b = 10
    lux = m * resistance + b
    return lux

def get_led_status():
    try:
        dist = distance()
        lux = read_photoresistor()

        # Debug prints (can be commented out)
        print(f"Set 2 - Distance: {dist} cm")
        print(f"Set 2 - Lux: {lux:.2f}")

        if dist < 20 and lux > 20:
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.output(RED_LED, GPIO.HIGH)
            return GPIO.HIGH  # Parking space is occupied (red LED is on)
        else:
            GPIO.output(GREEN_LED, GPIO.HIGH)
            GPIO.output(RED_LED, GPIO.LOW)
            return GPIO.LOW  # Parking space is empty (green LED is on)
    except Exception as e:
        print("Error in get_led_status:", e)
        return -1

if __name__ == "__main__":
    try:
        while True:
            status = get_led_status()
            print(f"Set 2 - LED Status: {status}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()
