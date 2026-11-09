from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, validate

class ProductInSchema(Schema):
    name = fields.Str(required=True)

    price = fields.Int(
        required=True,
        validate=validate.Range(min=0)
    )

class ProductOutSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Int()

blp = Blueprint(
    "products",
    __name__,
    url_prefix="/products"
)

@blp.route("")
class ProductList(MethodView):

    @blp.arguments(ProductInSchema)
    @blp.response(201, ProductOutSchema)
    def post(self, data):
        product = {
            "id": 1,
            **data
        }
        return product

    @blp.response(200, ProductOutSchema(many=True))
    def get(self):
        return [
            {"id": 1, "name": "Laptop", "price": 1000}
        ]

app = Flask(__name__)

app.config["API_TITLE"] = "Product API"
app.config["API_VERSION"] = "1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.3"

app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_JSON_PATH"] = "openapi.json"

app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

api = Api(app)
api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(port=5001)