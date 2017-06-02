# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import io
from builtins import dict, str
from contextlib import closing
from traceback import format_exc, print_exc
from urllib.parse import unquote

from bottle import HTTPError, parse_auth, request, response, route
from future import standard_library
from pyload.core.datatype import ExceptionObject
from pyload.rpc.jsonconverter import BaseEncoder, dumps, loads
from pyload.utils import purge

from .iface import API, session
from .utils import add_json_header, get_user_api, set_session

standard_library.install_aliases()

# used for gzip compression
try:
    import gzip
except ImportError:
    pass


def json_response(obj):
    accept = 'gzip' in request.headers.get('Accept-Encoding', '')
    result = dumps(obj)
    # do not compress small string
    if not accept or len(result) <= 500:
        return result
    response.headers['Vary'] = 'Accept-Encoding'
    response.headers['Content-Encoding'] = 'gzip'
    zbuf = io.StringIO()
    try:
        with closing(gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)) as fp:
            fp.write(result)
    except NameError:
        pass
    return zbuf.getvalue()


# returns http error
def error(code, msg):
    return HTTPError(code, dumps(msg), **dict(response.headers))

# accepting positional arguments, as well as kwargs via post and get
# only forbidden path symbol are "?", which is used to separate GET data and #


@route("/api/<func><args:re:[^#?]*>")
@route("/api/<func><args:re:[^#?]*>", method="POST")
def call_api(func, args=""):
    add_json_header(response)

    s = request.environ.get('beaker.session')
    # Accepts standard http auth
    auth = parse_auth(request.get_header('Authorization', ''))
    if 'session' in request.POST or 'session' in request.GET:
        # removes "' so it works on json strings
        s = s.get_by_id(purge.chars(request.params.get('session'), "'\""))
    elif auth:
        user = API.check_auth(
            auth[0], auth[1], request.environ.get('REMOTE_ADDR', None))
        # if auth is correct create a pseudo session
        if user:
            s = {'uid': user.uid}

    api = get_user_api(s)
    if not api:
        return error(401, "Unauthorized")

    if not API.is_authorized(func, api.user):
        return error(403, "Forbidden")

    if not hasattr(API.EXTERNAL, func) or func.startswith("_"):
        print("Invalid API call", func)
        return error(404, "Not Found")

    # TODO: possible encoding
    # TODO: Better error codes on invalid input

    args = [loads(unquote(arg)) for arg in args.split("/")[1:]]
    kwargs = {}

    # accepts body as json dict
    if request.json:
        kwargs = request.json

    # file upload, reads whole file into memory
    for name, file in request.files.items():
        kwargs['filename'] = file.filename
        with closing(io.StringIO()) as content:
            file.save(content)
            kwargs[name] = content.getvalue()

    # convert arguments from json to obj separately
    for x, y in request.params.items():
        try:
            if not x or not y or x == "session":
                continue
            kwargs[x] = loads(unquote(y))
        except Exception as e:
            # Unsupported input
            msg = "Invalid Input {0}, {1} : {2}".format(x, y, str(e))
            print_exc()
            print(msg)
            return error(415, msg)

    try:
        result = getattr(api, func)(*args, **kwargs)
        # null is invalid json response
        if result is None:
            result = True
        return json_response(result)

    except ExceptionObject as e:
        return error(400, str(e))
    except Exception as e:
        print_exc()
        return error(500, {'error': str(e), 'traceback': format_exc()})


@route("/api/login")
@route("/api/login", method="POST")
def login():
    add_json_header(response)

    username = request.params.get('username')
    password = request.params.get('password')

    user = API.check_auth(
        username, password, request.environ.get('REMOTE_ADDR', None))

    if not user:
        return json_response(False)

    s = set_session(request, user)

    # get the session id by dirty way, documentations seems wrong
    try:
        sid = s._headers['cookie_out'].split("=")[1].split(";")[0]
    # reuse old session id
    except Exception:
        sid = request.get_header(session.options['key'])

    result = BaseEncoder().default(user)
    result['session'] = sid

    # Return full user information if needed
    if request.params.get('user'):
        return dumps(result)

    return json_response(sid)


@route("/api/logout")
@route("/api/logout", method="POST")
def logout():
    add_json_header(response)

    s = request.environ.get('beaker.session')
    s.delete()

    return json_response(True)
