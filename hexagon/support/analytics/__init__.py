from enum import Enum
import datetime

from hexagon.support.storage import store_local_data
from hexagon.support.analytics import google_analytics

_data_file_name = "events"


class Event(Enum):
    session = "session"
    selection = "selection"
    execution = "execution"


def session_start():
    s = {
        "datetime": str(datetime.datetime.now()),
        "type": Event.session.value,
        "name": "session_start",
    }
    store_local_data(_data_file_name, str(s))
    google_analytics.session_start()


def session_end():
    s = {
        "datetime": str(datetime.datetime.now()),
        "type": Event.session.value,
        "name": "session_end",
    }
    store_local_data(_data_file_name, str(s))
    google_analytics.session_end()


def user_action(name: Event, **kwargs):
    s = {
        **{
            "datetime": str(datetime.datetime.now()),
            "type": "user_action",
            "name": name.value,
        },
        **kwargs,
    }
    store_local_data(_data_file_name, str(s))
    google_analytics.event(name.value, **kwargs)


def event(name: Event, **kwargs):
    s = {
        **{
            "datetime": str(datetime.datetime.now()),
            "type": "hexagon",
            "name": name.value,
        },
        **kwargs,
    }
    store_local_data(_data_file_name, str(s))
    google_analytics.event(name.value, **kwargs)
