import json

import tornado_swirl
from tornado import autoreload
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    async def data_received(self, chunk):
        self.set_header('Content-Type', 'application/json')
        self.write(chunk)
        await self.finish()


class NotFoundHandler(BaseHandler):
    response_object = {
        'error': 'Route doesn\'t exist'
    }

    async def rise_error(self):
        self.set_status(404)

        await self.data_received(
            json.dumps(self.response_object)
        )

    async def get(self):
        await self.rise_error()

    async def post(self):
        await self.rise_error()


@tornado_swirl.restapi(r'/')
class MainHandler(BaseHandler):
    async def get(self):
        """Index rout
        """
        self.write({
            "Hello": "world."
        })


class Core:
    def run(self):
        self.init_swagger()

        app = tornado_swirl.Application(
            [(r'/', MainHandler)],
            default_handler_class=NotFoundHandler
        )

        server = HTTPServer(
            app,
            xheaders=True
        )
        server.bind(8000)
        autoreload.start()
        server.start()

        IOLoop.current().start()

    @classmethod
    def init_swagger(cls):
        tornado_swirl.describe(
            title='Event Manager',
            description='API for managing events.',
            api_version='1.0.0'
        )
