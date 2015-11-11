import tornado.ioloop
import tornado.web
import os

changed = 0
settings = {'brightness': 50}


def update_settings(update_dict):
    global changed
    for k in update_dict.keys():
        if settings[k] != update_dict[k]:
            settings[k] = update_dict[k]
            changed = 1

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html",
                    brightness=settings['brightness'])


class ChangeValuesHandler(tornado.web.RequestHandler):
    def post(self):
        update_dict = {}
        update_dict['brightness'] = self.get_argument('brightness')
        update_settings(update_dict)
        self.redirect("/")

class HasThereBeenAChangeHandler(tornado.web.RequestHandler):
    def get(self):
        global changed
        if changed:
            self.write("1")
            changed = 0
        else:
            self.write("0")


def make_app():
    handlers = [
        (r"/", MainHandler),
        (r"/changed/", HasThereBeenAChangeHandler),
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