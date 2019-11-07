from datetime import datetime
from typing import Union

from tornado_swirl import schema


class Serializable(dict):
    def __init__(self):
        super().__init__()
        # hack to fix _json.so make_encoder serialize properly
        self.__setitem__('dummy', 1)

    def __repr__(self):
        return '<%s.%s object at %s>' % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self))
        )

    def _my_attrs(self):
        parent = self.__class__.__bases__[0]()

        return [
            (x, Serializable._value_representation(getattr(self, x)))
            for x in parent.__dir__() if x != 'schema_spec' and x[:1] != '_'
        ]

    @classmethod
    def _value_representation(cls, value):
        if isinstance(value, (str, int, float, list, tuple, dict)):
            return value

        if isinstance(value, datetime):
            return value.isoformat()

        if value is None:
            return None

        return repr(value)

    def items(self):
        return iter(self._my_attrs())


@schema
class Error:
    """Model that represent error message

    Properties:
        message (string) -- Error message
    """

    def __init__(self):
        super().__init__()

        self.__message: str = ''

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value


class ErrorEntity(Error, Serializable):
    def __init__(self, message=''):
        super().__init__()

        self.message = message


@schema
class Event:
    """The model describes a price used in the offer

    Properties:
        id (string) -- Event uuid
        device_type (enum[desktop, mobile, tablet]) -- Devise type
        category (int) -- Category id
        client (int) -- Event uuid
        client_group (int) -- Event uuid
        valid (bool) -- Event uuid
        value (float) -- Event uuid
        timestamp (date-time) -- Event uuid
    """

    def __init__(self):
        super().__init__()

        self.__id: str = ''
        self.__device_type: str = ''
        self.__category: int = 0
        self.__client: int = 0
        self.__client_group: int = 0
        self.__valid: Union[bool, None] = None
        self.__value: float = 0.0
        self.__timestamp: Union[datetime, None] = None

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, val: str):
        self.__id = val

    @property
    def device_type(self) -> str:
        return self.__device_type

    @device_type.setter
    def device_type(self, val: str):
        self.__device_type = val

    @property
    def category(self) -> int:
        return self.__category

    @category.setter
    def category(self, val: int):
        self.__category = val

    @property
    def client_group(self) -> int:
        return self.__client_group

    @client_group.setter
    def client_group(self, val: int):
        self.__client_group = val

    @property
    def valid(self) -> Union[bool, None]:
        return self.__valid

    @valid.setter
    def valid(self, val: Union[bool, None]):
        self.__valid = val

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, val: float):
        self.__value = val

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, val: datetime):
        self.__timestamp = val


class EventEntity(Event, Serializable):
    pass
