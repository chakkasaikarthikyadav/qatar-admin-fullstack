from flask import Flask
from flask_cors import CORS
from extensions import db   # ✅ changed

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)  # ✅ same
    CORS(app, supports_credentials=True)

    from routes.auth import auth_bp
    from routes.opportunity import opp_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(opp_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return "Backend Running ✅"