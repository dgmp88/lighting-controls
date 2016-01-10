import tornado.ioloop
import tornado.web
import os
import json
import requests

class PiLightingHandler(tornado.web.RequestHandler):
    lighting_controls = None
    lighting_settings = None
    
    def initialize(self, lighting_controls, lighting_settings):
        self.lighting_controls = lighting_controls
        self.lighting_settings = lighting_settings


class MainHandler(PiLightingHandler):
    def get(self):
        self.render("templates/index.html",
                    brightness_r=self.lighting_settings['brightness_rgb'][0],
                    brightness_g=self.lighting_settings['brightness_rgb'][1],
                    brightness_b=self.lighting_settings['brightness_rgb'][2])

class ChangeValuesHandler(tornado.web.RequestHandler):
    def post(self):
        self.lighting_settings['brightness_rgb'] = [self.get_argument('brightness_r'),
                                                self.get_argument('brightness_g'),
                                                self.get_argument('brightness_b')]

        # Convert all values to integers
        for idx, val in enumerate(lighting_settings['brightness_rgb']):
            self.lighting_settings['brightness_rgb'][idx] = int(val)
            self.lighting_controls[i].ChangeDutyCycle(val)

        self.redirect("/")
