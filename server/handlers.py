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
                    brightness_r=self.lighting_settings['brightness_rgb'][0],
                    brightness_g=self.lighting_settings['brightness_rgb'][1],
                    brightness_b=self.lighting_settings['brightness_rgb'][2])

class ChangeValuesHandler(PiLightingHandler):
    def post(self):
        self.lighting_settings['brightness_rgb'] = [self.get_argument('brightness_r'),
                                                self.get_argument('brightness_g'),
                                                self.get_argument('brightness_b')]

        # Convert all values to integers
        for idx, val in enumerate(self.lighting_settings['brightness_rgb']):
            self.lighting_settings['brightness_rgb'][idx] = int(val)
            self.pgpio_obj.set_PWM_dutycycle(self.pins[idx], int(val))

        self.redirect("/")


