# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from builtins import object, str

from bottle import ServerAdapter as _ServerAdapter
from future import standard_library

standard_library.install_aliases()


class ServerAdapter(_ServerAdapter):

    __slots__ = ['NAME', 'SSL', 'cert', 'connection', 'debug', 'key']

    SSL = False
    NAME = ""

    def __init__(self, host, port, key, cert, connections, debug, **kwargs):
        _ServerAdapter.__init__(self, host, port, **kwargs)
        self.key = key
        self.cert = cert
        self.connection = connections
        self.debug = debug

    @classmethod
    def find(cls):
        """
        Check if server is available by trying to import it

        :raises Exception: importing  C dependant library could also fail with other reasons
        :return: True on success
        """
        try:
            __import__(cls.NAME)
            return True
        except ImportError:
            return False

    def run(self, handler):
        raise NotImplementedError


class CherryPyWSGI(ServerAdapter):

    __slots__ = ['NAME', 'SSL']

    SSL = True
    NAME = "threaded"

    @classmethod
    def find(cls):
        return True

    def run(self, handler):
        from wsgiserver import CherryPyWSGIServer

        if self.cert and self.key:
            CherryPyWSGIServer.ssl_certificate = self.cert
            CherryPyWSGIServer.ssl_private_key = self.key
        server = CherryPyWSGIServer(
            (self.host, self.port), handler, numthreads=self.connection)
        server.start()


class FapwsServer(ServerAdapter):
    """
    Does not work very good currently.
    """
    __slots__ = ['NAME']

    NAME = "fapws"

    def run(self, handler):  #: pragma: no cover
        import fapws._evwsgi as evwsgi
        from fapws import base, config

        port = self.port
        if float(config.SERVER_IDENT[-2:]) > 0.4:
            # fapws3 silently changed its API in 0.5
            port = str(port)
        evwsgi.start(self.host, port)
        evwsgi.set_base_module(base)

        def app(environ, start_response):
            environ['wsgi.multiprocess'] = False
            return handler(environ, start_response)

        evwsgi.wsgi_cb(('', app))
        evwsgi.run()


# TODO: ssl
class MeinheldServer(ServerAdapter):

    __slots__ = ['NAME', 'SSL']

    SSL = True
    NAME = "meinheld"

    def run(self, handler):
        from meinheld import server

        if self.quiet:
            server.set_access_logger(None)
            server.set_error_logger(None)

        server.listen((self.host, self.port))
        server.run(handler)


# TODO: ssl
class TornadoServer(ServerAdapter):
    """
    The super hyped asynchronous server by facebook. Untested.
    """
    __slots__ = ['NAME', 'SSL']

    SSL = True
    NAME = "tornado"

    def run(self, handler):  #: pragma: no cover
        import tornado.wsgi
        import tornado.httpserver
        import tornado.ioloop

        container = tornado.wsgi.WSGIContainer(handler)
        server = tornado.httpserver.HTTPServer(container)
        server.listen(port=self.port)
        tornado.ioloop.IOLoop.instance().start()


class BjoernServer(ServerAdapter):
    """
    Fast server written in C: https://github.com/jonashaag/bjoern.
    """
    __slots__ = ['NAME']

    NAME = "bjoern"

    def run(self, handler):
        from bjoern import run
        run(handler, self.host, self.port)


# TODO: ssl
class EventletServer(ServerAdapter):

    __slots__ = ['NAME', 'SSL']

    SSL = True
    NAME = "eventlet"

    def run(self, handler):
        from eventlet import wsgi, listen

        try:
            wsgi.server(listen((self.host, self.port)), handler,
                        log_output=(not self.quiet))
        except TypeError:
            # Needed to ignore the log
            class NoopLog(object):
                __slots__ = []

                def write(self, *args):
                    pass
            # Fallback, if we have old version of eventlet
            wsgi.server(listen((self.host, self.port)), handler, log=NoopLog())


class FlupFCGIServer(ServerAdapter):

    __slots__ = ['NAME', 'SSL']

    SSL = False
    NAME = "flup"

    def run(self, handler):  #: pragma: no cover
        import flup.server.fcgi
        from flup.server.threadedserver import ThreadedServer

        def noop(*args, **kwargs):
            pass

        # Monkey patch signal handler, it does not work from threads
        ThreadedServer._installSignalHandlers = noop

        self.options.setdefault('bindAddress', (self.host, self.port))
        flup.server.fcgi.WSGIServer(handler, **self.options).run()


# Order is important and gives every server precedence over others!
all_server = [TornadoServer, EventletServer, CherryPyWSGI]
# Some are deactivated because they have some flaws
##all_server = [FapwsServer, MeinheldServer, BjoernServer, TornadoServer, EventletServer, CherryPyWSGI]
