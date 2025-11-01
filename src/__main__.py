from app import create_app

from dotenv import load_dotenv
import os


HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 6767))
DEBUG = bool(os.environ.get("DEBUG"))


load_dotenv()


if __name__ == "__main__":
    app = create_app()

    app.run(host=HOST, port=PORT, debug=DEBUG)
