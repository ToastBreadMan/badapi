from web.routing import Application

app = Application()


@app.html(path="/test")
def test(request):
    return "hello"


@app.html(path="/hello")
def hello(request):
    return "test"


@app.json(path="/json")
def json(request):
    return {'message': "test"}


@app.redirect_to(path="/redirect")
def redirect_test(request):
    return "/json"


@app.render(path="/render")
def render_test(request):
    return ("index.html", {"test":"test"})

app.run(app)
