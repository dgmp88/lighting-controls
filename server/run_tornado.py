import tornado.ioloop
import tornado.web
import os
import json
import requests


from handlers import ChangeValuesHandler, MainHandler

def get_gpio_controls():
    import RPi.GPIO as GPIO # always needed with RPi.GPIO
    from time import sleep  # pull in the sleep function from time module

    GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD numbering schemes. I use BCM

    red_id = 2
    green_id = 24
    blue_id = 3


    GPIO.setup(red_id, GPIO.OUT)# set GPIO 25 as output for white led
    GPIO.setup(green_id, GPIO.OUT)# set GPIO 24 as output for red led
    GPIO.setup(blue_id, GPIO.OUT)# set GPIO 24 as output for red led

    # Create the PWM object at specified frequency
    freq = 200
    red = GPIO.PWM(red_id, freq)
    green = GPIO.PWM(green_id, freq)
    blue = GPIO.PWM(blue_id, freq)

    # Initiate all bulbs off
    red.start(0)
    green.start(0)
    blue.start(0)

    controls = [red, green, blue]

    return controls


def make_app():
    inputs = {lighting_settings: {'brightness_rgb': [0, 0, 0]},
              lighting_controls: get_gpio_controls()}

    handlers = [
        (r"/", MainHandler, inputs),
        (r"/dochange/", ChangeValuesHandler, inputs),
    ]

    DEBUG = False
    if os.environ.get("DEBUG") == "True":
        DEBUG = True

    settings = {
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }

    return tornado.web.Application(handlers, debug=DEBUG, **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
