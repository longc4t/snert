from config import Blueprint,json,request,app
api = Blueprint('api', __name__)


def getjson():
    return json.loads(request.get_data().decode("utf-8"))

@api.route("/")
@api.route("/testapi")
def testapi():
    return "<h1>TEST API!"
