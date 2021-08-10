from urllib import parse
import uuid

import pkg_resources
import requests

from hexagon.support.storage import load_user_data, store_user_data

import posthog

posthog.api_key = "phc_3s18YdftB0tjs1WlQpPCTspkPfkdsqflWppyBvxnbJB"
posthog.host = "https://app.posthog.com"


def session_start():
    __collect(sc="start", ni=1)


def session_end():
    __collect(sc="end", ni=1)


def event(name: str, **kwargs):
    __collect(**{**{"ea": name}, **kwargs})


def __collect(**kwargs):
    version = pkg_resources.require("hexagon")[0].version

    cid = load_user_data("user_id")
    if not cid:
        cid = str(uuid.uuid4())
        store_user_data("user_id", cid)

    posthog.capture(cid, kwargs.get("ea", kwargs.get("sc")))
    params = parse.urlencode(
        {
            **{
                "v": 1,
                "tid": "UA-204311640-1",
                "aip": 1,  # https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters#aip
                "npa": 1,  # https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters#npa
                "cid": cid,
                "t": "event",
                "an": "hexagon",
                "av": version,
            },
            **kwargs,
        }
    )
    requests.post("https://www.google-analytics.com/collect", data=params)
