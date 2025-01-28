from flask import Flask
from src.controllers.userController import user_bp
from src.controllers.codemailController import cm_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv, dotenv_values
from mailman import mail

load_dotenv()
JWT_SECRET_KEY = dotenv_values('.env').get('JWT_SECRET_KEY')

MAIL_SERVER = dotenv_values('.env').get('MAIL_SERVER')
MAIL_PORT = dotenv_values('.env').get('MAIL_PORT')
MAIL_USERNAME = dotenv_values('.env').get('MAIL_USERNAME')
MAIL_PASSWORD = dotenv_values('.env').get('MAIL_PASSWORD')

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config['MAIL_DEFAULT_SENDER'] = "MAIL_USERNAME"

jwt = JWTManager(app)
mail.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(cm_bp)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)