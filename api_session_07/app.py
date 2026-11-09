import connexion
import products

app = connexion.FlaskApp(
    __name__,
    specification_dir="openapi/"
)

app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

products.db.init_app(app.app)

with app.app.app_context():
    products.db.create_all()

app.add_api(
    "products.yaml",
    validate_responses=True
)

if __name__ == "__main__":
    app.run(port=5000)
