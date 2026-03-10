import os
from flask import Flask
from flask_cors import CORS
from datetime import timedelta
from flask_jwt_extended import JWTManager
from router.auth import AuthRouter
from router.user import UserRouter
from router.set import SetRouter
from router.word import WordRouter
from router.search import SearchRouter
from errors.errors import register_error_handlers
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(
    app, 
    supports_credentials=True, 
    resources={r"/*": {"origins": os.getenv("FRONT_URL")}},
)

register_error_handlers(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_COOKIE_SECURE"] = True
app.config['JWT_COOKIE_SAMESITE'] = 'None'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
app.config["JWT_REFRESH_COOKIE_PATH"] = "/"
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"
app.json.ensure_ascii = False
app.json.sort_keys = False

jwt = JWTManager(app)


@app.route('/', methods=['GET'])
def welcome():
    return "welcome to word not api", 200

app.register_blueprint(AuthRouter, url_prefix='/auth')
app.register_blueprint(UserRouter, url_prefix='/user')
app.register_blueprint(SetRouter, url_prefix='/set')
app.register_blueprint(WordRouter, url_prefix='/words')
app.register_blueprint(SearchRouter, url_prefix='/search')

if __name__ == '__main__':
    app.run()
