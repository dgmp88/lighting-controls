import tornado.ioloop
import tornado.web
import os
import time

from handlers import ChangeValuesHandler, MainHandler

import pigpio
pgpio_obj = pigpio.pi() # connect to local Pi

red_pin = 2
green_pin = 24
blue_pin = 3

def start_tornado(app):
    app.listen(80)
    print "Starting Torando"
    tornado.ioloop.IOLoop.instance().start()
    print "Tornado finished"

def switch_off():
    pgpio_obj.set_PWM_dutycycle(red_pin, 0)
    pgpio_obj.set_PWM_dutycycle(green_pin, 0)
    pgpio_obj.set_PWM_dutycycle(blue_pin, 0)

def stop_tornado():
    pgpio_obj.stop()
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.add_callback(ioloop.stop)
    print "Asked Tornado to exit"

def make_app():
    inputs = {'lighting_settings': {'rgb': [0, 0, 0]},
              'pgpio_obj': pgpio_obj,
              'pins': [red_pin, green_pin, blue_pin]}

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
    start_tornado(app)
    switch_off()
    try:
	while True:
      	    time.sleep(1)
            print 'hi'
    except KeyboardInterrupt:
        stop_tornado()
