import tornado_swirl as swirl
from tornado import autoreload
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import StaticFileHandler

from src import url
from src.request_handler import MainHandler, NotFoundHandler, EventHandler, AddEventHandler, ReportHandler


class Core:
    def run(self):
        self.init_swagger()

        app = swirl.Application(
            self.get_urls_handler_mapping(),
            default_handler_class=NotFoundHandler
        )

        server = HTTPServer(
            app,
            xheaders=True
        )
        server.bind(8000)
        autoreload.start()
        server.start()

        try:
            IOLoop.current().start()
        except KeyboardInterrupt:
            IOLoop.current().stop()

    @classmethod
    def init_swagger(cls):
        swirl.describe(
            title='Stylight - PAM Challenge',
            description='Stylight - PAM Challenge API Specification',
            api_version='1.0.0'
        )

    @classmethod
    def get_urls_handler_mapping(cls):
        return [
            (url.FAVICON, StaticFileHandler, {'path': 'static/'}),
            (url.MAIN, MainHandler),
            (url.EVENT, EventHandler),
            (url.ADD_EVENT, AddEventHandler),
            (url.REPORT, ReportHandler),
        ]
