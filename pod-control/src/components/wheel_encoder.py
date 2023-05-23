import time

import RPi.GPIO as GPIO

outputA = 4  # green/black/black
outputB = 2  # white/red/white,  brown/orange/blue
counter = 0
aState = 0
aLastState = 0
t1 = 0
t2 = 0
deltad = 0.0
deltat = 0.0
calc = 0.0


def setup():
    global aLastState, t1
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(outputA, GPIO.IN)
    GPIO.setup(outputB, GPIO.IN)
    t1 = time.time() * 1000
    aLastState = GPIO.input(outputA)
    print("Setup complete.")


def loop():
    global aState, counter, t2, bLastState, deltat, t1, t2, aLastState
    aState = GPIO.input(outputA)

    deltad = 1.0 / 8.0

    if aState != aLastState:
        t2 = time.time() * 1000

        if GPIO.input(outputB) != aState:
            counter -= 1
        else:
            counter += 1
            print("counter: ", counter)
            deltat = t2 - t1
            calc = 1000 * deltad / deltat
            print("Instantaneous Speed:", calc)
            t1 = t2

    aLastState = aState


def main():
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program terminated.")


if __name__ == "__main__":
    main()
