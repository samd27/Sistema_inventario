import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().with_name('.env'))

from app import create_app


if __name__ == "__main__":
    env_name = os.environ.get("FLASK_ENV", "development")
    app = create_app(env_name)
    app.run(host="127.0.0.1", port=8082, debug=env_name == "development")
