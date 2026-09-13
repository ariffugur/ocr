from flask import Flask

from routes import api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    return app


app = create_app()

if __name__ == "__main__":
    # Yerel test icin. Render'da gunicorn kullanilacak (Procfile'a bak).
    app.run(host="0.0.0.0", port=5000, debug=True)
