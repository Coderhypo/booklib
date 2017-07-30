import os
from pathlib import Path

from stone.models import init_db
from stone import create_app

app = create_app()
DATA_PATH = app.config['DATA_PATH']


def create_data(data_path):
    for path in ["", "db", "images"]:
        try:
            os.mkdir(os.path.join(data_path, path))
        except:
            pass

    file = os.path.join(data_path, "server_info")
    Path(file).touch()


if __name__ == "__main__":
    create_data(DATA_PATH)
    init_db()
    app.run(host="0.0.0.0", port=8000, workers=3, debug=app.config.get("DEBUG"))
