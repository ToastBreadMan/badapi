from werkzeug.routing import Rule


class Blueprint:
    def __init__(self):
        self.functions = {}
        self.url = []

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