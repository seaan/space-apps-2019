# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 24
GPIO_ECHO = 23
GPIO_LED = 26

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    start_sample = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0 and time.time() - start_sample < 1:
        StartTime = time.time()

    if time.time() - start_sample > 1:
        return None

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist = (TimeElapsed * 34300) / 2

    return TimeElapsed


def is_ice(data):
    if data is None:
        return False

    result = False

    if (data < 0.00054):
        result = True
        time.sleep(1)
        return result
    else:
        return result


if __name__ == '__main__':
    #GPIO.output(GPIO_LED, True)

    try:
        while True:
            runs = []
            total = 0
            count = 0

            for i in range(0, 10):
                dist = distance()
                if dist:
                    total += dist
                    count += 1
                time.sleep(.01)

            sample = total/count
            runs.append(sample)
            print(total/50*1000000)

            if is_ice(sample):
                print("Ice.")
                GPIO.output(GPIO_LED, True)
            else:
                print("Not ice.")
                GPIO.output(GPIO_LED, False)

            # GPIO.output(GPIO_LED, False)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
