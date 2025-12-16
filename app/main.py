from flask import Flask
from app.routes import main_routes

print("MAIN.PY ÇALIŞTI")

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_routes)
    return app

app = create_app()

if __name__ == "__main__":
    print("FLASK BAŞLIYOR")
    app.run(debug=True)
