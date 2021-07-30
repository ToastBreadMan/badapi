import sys

from werkzeug import run_simple, Request, Response
from werkzeug.routing import Map, Rule

from web.handler import Handler

from .Blueprints import Blueprint


class Application(Blueprint):
    def __init__(self, port=8000, host='127.0.0.1'):
        super().__init__()
        self.url = []
        self.port = port
        self.host = host
        self.map = None
        self.functions = {}
        self.handler = Handler()

    def dispatch_request(self, request):
        adapter = self.map.bind_to_environ(request.environ)
        endpoint, values = adapter.match()
        return self.handle_request(endpoint, request, values)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def handle_request(self, endpoint, request, values):
        func = self.functions[endpoint]
        value = func['function'](request, **values)
        status = func['status']
        mimetype = func['response_type']
        response = getattr(self.handler, f'handle_{mimetype}')(value, status)
        return response

    def register_blueprint(self, blueprint):
        self.functions = {**self.functions, **blueprint.functions}
        self.url = self.url + blueprint.url

    def run(self, app):
        self.map = Map(self.url)
        run_simple(self.host, self.port, app, use_debugger=True, use_reloader=True)
