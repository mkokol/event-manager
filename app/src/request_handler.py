import json

import tornado_swirl as swirl
from tornado.web import RequestHandler

from src import url


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


@swirl.restapi(url.MAIN)
class MainHandler(BaseHandler):
    async def get(self):
        """Index rout

            It's just an entry point that gave you some links to explore more

            Tags:
                Main
        """
        self.write({
            'doc': 'http://localhost:8000/swagger/spec.html',
            'json': 'http://localhost:8000/swagger/spec'
        })
