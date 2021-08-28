import uuid

import pkg_resources
import requests

from hexagon.support.storage import load_user_data, store_user_data


def event(name: str, **kwargs):
    __collect(name, **{**{"ea": name}, **kwargs})


def __collect(name: str, **kwargs):
    version = pkg_resources.require("hexagon")[0].version

    cid = load_user_data("user_id")
    if not cid:
        cid = str(uuid.uuid4())
        store_user_data("user_id", cid)

    mid = "G-Y28H5KHQEZ"

    # params = {
    #     **{
    #         "v": 1,
    #         # "tid": "UA-204311640-1",
    #         "aip": 1,  # https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters#aip
    #         "npa": 1,  # https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters#npa
    #         "cid": cid,
    #         "t": "event",
    #         "an": "hexagon",
    #         "av": version,
    #     },
    #     **kwargs,
    # }
    params = {"client_id": cid, "events": [{"name": name}]}
    res = requests.post(
        f"https://www.google-analytics.com/mp/collect?measurement_id={mid}&api_secret=lalUv8tgR4OfjXl88FjrFw",
        json=params,
    )
    print(res.text)
