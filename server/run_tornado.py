import tornado.ioloop
import tornado.web
import os
import json
import requests

changed = 0

lighting_settings = {'brightness_rgb': [50, 50, 50]}
ip_settings = json.load(open("secret_stuff.json"))
arduino_set_rgb_endpoint = ip_settings['arduino_set_rgb']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html",
                    brightness_r=lighting_settings['brightness_rgb'][0],
                    brightness_g=lighting_settings['brightness_rgb'][1],
                    brightness_b=lighting_settings['brightness_rgb'][2])


class ChangeValuesHandler(tornado.web.RequestHandler):
    def post(self):
        lighting_settings['brightness_rgb'] = [self.get_argument('brightness_r'),
                                                self.get_argument('brightness_g'),
                                                self.get_argument('brightness_b')]
        for idx, val in enumerate(lighting_settings['brightness_rgb']):
            lighting_settings['brightness_rgb'][idx] = int(val)

        end_vals = '%03d%03d%03d' % (lighting_settings['brightness_rgb'][0],
                                     lighting_settings['brightness_rgb'][1],
                                     lighting_settings['brightness_rgb'][2])
        set_url = arduino_set_rgb_endpoint + end_vals

        requests.get(set_url)

        self.redirect("/")

def make_app():
    handlers = [
        (r"/", MainHandler),
        (r"/dochange/", ChangeValuesHandler),
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
