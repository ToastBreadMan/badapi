import sys

from werkzeug import run_simple, Request, Response
from werkzeug.routing import Map, Rule

from web.handler import Handler


class Application:
    def __init__(self):
        self.url = []
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

    def html(self, *args, **kwargs):
        def inner(func):
            self.url.append(Rule(kwargs['path'], endpoint=func.__name__))
            self.functions[func.__name__] = {
                'function': func,
                'response_type': 'html',
                'status': 200
            }
        return inner

    def json(self, *args, **kwargs):
        def inner(func):
            self.url.append(Rule(kwargs['path'], endpoint=func.__name__))
            self.functions[func.__name__] = {
                'function': func,
                'response_type': 'json',
                "status": 200
            }
        return inner

    def redirect_to(self, *args, **kwargs):
        def inner(func):
            self.url.append(Rule(kwargs['path'], endpoint=func.__name__))
            self.functions[func.__name__] = {
                'function': func,
                'response_type': 'redirect',
                'status': 302
            }
        return inner

    def render(self, *args, **kwargs):
        def inner(func):
            self.url.append(Rule(kwargs['path'], endpoint=func.__name__))
            self.functions[func.__name__] = {
                'function': func,
                'response_type': 'template',
                'status': 200
            }
        return inner

    def handle_request(self, endpoint, request, values):
        func = self.functions[endpoint]
        value = func['function'](request, **values)
        status = func['status']
        mimetype = func['response_type']
        response = getattr(self.handler, f'handle_{mimetype}')(value, status)
        return response

    def run(self, app):
        self.map = Map(self.url)
        run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)






