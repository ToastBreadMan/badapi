import json
import os

from jinja2 import Environment, FileSystemLoader
from werkzeug import Response
from werkzeug.utils import redirect


class Handler:
    def __init__(self):
        template_path = os.path.join(os.path.dirname(__file__), '../templates')
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True
        )

    @staticmethod
    def handle_html(value, status):
        return Response(value, status=status, mimetype="text/html")

    @staticmethod
    def handle_json(value, status):
        response_json = json.dumps(value)
        return Response(response_json, status=status, mimetype="application/json")

    @staticmethod
    def handle_redirect(value, status):
        return redirect(value, code=status)

    def handle_template(self, value, status):
        template = self.jinja_env.get_template(value[0])
        return self.handle_html(template.render(value[1]), status)