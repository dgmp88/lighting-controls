import tornado.ioloop
import tornado.web
import os
import json
import requests

class PiLightingHandler(tornado.web.RequestHandler):
    pgpio_obj = None
    pins = None
    lighting_settings = None

    def initialize(self, pgpio_obj, lighting_settings, pins):
        self.pgpio_obj = pgpio_obj
        self.pins = pins
        self.lighting_settings = lighting_settings


class MainHandler(PiLightingHandler):
    def get(self):
        self.render("templates/index.html",
                r=self.lighting_settings['brightness_rgb'][0],
                g=self.lighting_settings['brightness_rgb'][1],
                b=self.lighting_settings['brightness_rgb'][2])

class ChangeValuesHandler(PiLightingHandler):
    def post(self):
        default_change(self)
    def get(self):
        default_change(self)


def default_change(handler):
    handler.lighting_settings['rgb'] = [handler.get_argument('r'),
            handler.get_argument('g'),
            handler.get_argument('b')]

    # Convert all values to integers
    for idx, val in enumerate(handler.lighting_settings['rgb']):
        handler.lighting_settings['rgb'][idx] = int(val)
        handler.pgpio_obj.set_PWM_dutycycle(handler.pins[idx], int(val))

    handler.redirect('/')
