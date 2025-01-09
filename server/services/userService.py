from database import es
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity
from repositories import userRepository
import re
from datetime import timedelta

def createUser(username, email, password, confirmPassword):
  if not username or not email or not password or not confirmPassword:
    return {"error": "Mandatory fields aren't filled in"}, 400
  
  if len(username) > 16 or len(username) < 3:
    return {"error": "Username must be bigger than 3 and smaller than 16"}, 400

  if not re.match("^[a-z0-9]+$", username):
    return {"error": "Username must contain only lowercase letters and numbers"}, 400
  
  if not re.search("[a-z]", password):
        return {"error": "Password must contain at least one lowercase letter"}, 400
  if not re.search("[A-Z]", password):
        return {"error": "Password must contain at least one uppercase letter"}, 400
  if not re.search("[0-9]", password):
        return {"error": "Password must contain at least one digit"}, 400
  if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return {"error": "Password must contain at least one special character"}, 400

  if len(password) < 8:
    return {"error": "password must contain at least 8 characters"}, 400
  
  if password != confirmPassword:
    return {"error": "Passwords do not match"}, 400
  
  existing_userByUsername, username_statusCode = userRepository.findByUsername(username)
  existing_userByEmail, email_statusCode = userRepository.findByEmail(email)
    
  if username_statusCode != 404:
    return {"error": "Username already taken"}, 409

  if email_statusCode != 404:
    return {"error": "Email already taken"}, 409

  HashedPassword = generate_password_hash(password)

  userDoc = {
    "username": username,
    "email": email,
    "password": HashedPassword
  }

  response = es.index(index="users", body=userDoc)
  
  userId = response['_id']
  access_token = create_access_token(identity=userId, expires_delta=timedelta(hours=1))

  return {"JWT": access_token}, 201

def loginUser(username, password):
  user, statusCode = userRepository.findByUsername(username)

  if  statusCode == 404 or not check_password_hash(user['password'], password):
    return {"error": "invalid credentials"}, 401
  
  access_token = create_access_token(identity=user['id'], expires_delta=timedelta(hours=1))

  return {"JWT": access_token}, 200
  
def updateUserById(userId, username=None, email=None):
  user, findById_statusCode = userRepository.findById(userId)

  if findById_statusCode == 404:
    return {"error": "User Not Found"}, 404
  
  # jwt_identity = get_jwt_identity()

  # if user['id'] != jwt_identity:
    # return {"error": "Access Denied, UserId and JWT Identity Doesn't Match!"}, 403

  script = []

  if username:
    if len(username) > 16 or len(username) < 3:
      return {"error": "Username must be bigger than 3 and smaller than 16"}, 400

    if not re.match("^[a-z0-9]+$", username):
      return {"error": "Username must contain only lowercase letters and numbers"}, 400
  
    username_existing_user, findByUsername_statusCode = userRepository.findByUsername(username)
    
    if findByUsername_statusCode == 200 and username_existing_user['id'] != userId:
      return {"error": "Username already taken"}, 409

  if email:
    email_existing_user, findByEmail_statusCode = userRepository.findByEmail(email)
     
    if findByEmail_statusCode == 200 and email_existing_user['id'] != userId:
      return {"error": "Email already taken"}, 409

    script.append(f"ctx._source.email = '{email}'")

  if not script:
    return {"error": "No updates provided"}, 400

  try:
    script_str = "; ".join(script)
    es.update(index="users", id=userId, body={"script": script_str})

    updated_user = es.get(index="users", id=userId)

    return {
            "id": updated_user['_id'],
            "username": updated_user['_source']['username'],
            "email": updated_user['_source']['email'],
            "password": updated_user['_source']['password']
        }, 200
  except Exception:
    return {"error": str(Exception)}, 500

def deleteUserById(userId):
  user, statusCode = userRepository.findById(userId)

  if statusCode == 404:
    return {"error": "User Not Found"}, 404

  # jwt_identity = get_jwt_identity()

  # if user['id'] != jwt_identity:
    # return {"error": "Access Denied, UserId and JWT Identity Doesn't Match!"}, 403

  try:
    response = es.delete(index="users", id=userId)
    return response, 204
  except Exception:
    return {"error": str(Exception)}, 500