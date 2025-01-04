from flask import Flask
from controllers.userController import user_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv, dotenv_values

load_dotenv()
JWT_SECRET_KEY = dotenv_values('.env').get('JWT_SECRET_KEY')

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)

app.register_blueprint(user_bp)

if __name__ == "__main__":
  app.run(debug=True)