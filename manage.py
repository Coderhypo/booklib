from stone.models import init_db
from stone import create_app


app = create_app()


if __name__ == "__main__":
    # init_db()
    app.run(host="0.0.0.0", port=8000, workers=3, debug=app.config.get("DEBUG"))

