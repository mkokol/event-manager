import json

import tornado_swirl as swirl
from tornado.web import RequestHandler

from src import url
from src.db_manager import DbEventManager
from src.model import ErrorEntity

swirl.add_global_tag(
    name='Main',
    description='Here we collect generic info about API'
)

swirl.add_global_tag(
    name='Event',
    description='Event managing functionality'
)


class BaseHandler(RequestHandler):
    async def send(self, model):
        return await self.data_received(
            json.dumps(model)
        )

    async def data_received(self, chunk):
        self.set_header('Content-Type', 'application/json')
        self.write(chunk)
        await self.finish()

    async def rise_error(self, code=404, message='Unidentified Error'):
        self.set_status(code)
        error = ErrorEntity(message)

        await self.send(error)


class NotFoundHandler(BaseHandler):
    async def get(self):
        await self.rise_error(message='Route don\'t exist')

    async def post(self):
        await self.rise_error(message='Route don\'t exist')


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


@swirl.restapi(url.EVENT)
class EventHandler(BaseHandler):
    async def get(self, event_id):
        """Fetch event by id

            Tags:
                Event

            Path Parameter:
                event_id (string) -- Event unique id

            200 Response:
                 event (Event) -- Event data

            400 Response:
                 error (Error) -- Event do not exist
        """

        db_event_manager = DbEventManager()
        event = db_event_manager.fetch(event_id)

        if event:
            self.write(event)

            return

        await self.rise_error(400, 'Event do not exist')

    async def delete(self, event_id):
        """Delete event by id

            Tags:
                Event

            Path Parameter:
                event_id (string) -- Event unique id

            204 Response:
                 OK -- Event was deleted

            400 Response:
                 error (Error) -- Event do not exist
        """
        db_event_manager = DbEventManager()
        event = db_event_manager.fetch(event_id)

        if event:
            db_event_manager.delete(event_id)
            self.set_status(204)

            return

        await self.rise_error(400, 'Event do not exist')
