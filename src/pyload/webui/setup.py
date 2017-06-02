# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import time
from builtins import dict

from bottle import HTTPError, request, response, route
from future import standard_library

from .iface import SETUP
from .utils import add_json_header

standard_library.install_aliases()


# returns http error
def error(code, msg):
    return HTTPError(code, json.dumps(msg), **dict(response.headers))


def setup_required(func):
    def _view(*args, **kwargs):
        global timestamp

        # setup needs to be running
        if SETUP is None:
            return error(404, "Not Found")

        # setup finished
        if timestamp == 0:
            return error(409, "Done")

        # setup timed out due to inactivity
        if timestamp + TIMEOUT * 60 < time.time():
            return error(410, "Timeout")

        timestamp = time.time()

        return func(*args, **kwargs)

    return _view

# setup will close after inactivity
TIMEOUT = 15
timestamp = time.time()


@route("/setup")
@setup_required
def setup():
    add_json_header(response)

    return json.dumps({
        'system': SETUP.check_system(),
        'deps': SETUP.check_deps()
    })


@route("/setup_done")
@setup_required
def setup_done():
    global timestamp
    add_json_header(response)

    SETUP.add_user(
        request.params.get('user'),
        request.params.get('password')
    )

    SETUP.save()

    # mark setup as finished
    timestamp = 0

    return error(409, "Done")
