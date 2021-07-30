from web.Blueprints import Blueprint

blueprint = Blueprint()


@blueprint.html(path="/blueprint")
def test2(request):
    return "world"