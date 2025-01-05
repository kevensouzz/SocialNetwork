from database import es
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from repositories import userRepository

def createUser(username, password):
  existing_user, statusCode = userRepository.findByUsername(username)
    
  if statusCode != 404:
    return {"error": "Username already taken"}, 409

  if not username or not password:
    return jsonify(), 400
  
  if len(username) > 16 or len(username) < 3:
    return jsonify(), 400

  if len(password) < 8:
    return jsonify(), 400

  HashedPassword = generate_password_hash(password)

  userDoc = {
    "username": username,
    "password": HashedPassword,
  }

  response = es.index(index="users", body=userDoc)
  
  userId = response['_id']
  access_token = create_access_token(identity=userId)

  return {"JWT": access_token}, 201

def loginUser(username, password):
  user, statusCode = userRepository.findByUsername(username)

  if statusCode == 404:
    return {"error": "User Not Found"}, 404

  if not check_password_hash(user['password'], password):
    return {"error": "invalid credentials"}, 401
  
  access_token = create_access_token(identity=user['id'])

  return {"JWT": access_token}, 200
  
def updateUserById(userId, username=None):
  user, findById_statusCode = userRepository.findById(userId)

  if findById_statusCode == 404:
    return {"error": "User Not Found"}, 404
  
  jwt_identity = get_jwt_identity()

  if user['id'] != jwt_identity:
    return {"error": "Access Denied, UserId and JWT Identity Doesn't Match!"}, 403

  script = []

  if username:
    existing_user, findByUsername_statusCode = userRepository.findByUsername(username)
    
    if findByUsername_statusCode == 200 and existing_user['id'] != userId:
      return {"error": "Username already taken"}, 409
    
    script.append(f"ctx._source.username = '{username}'")

  if not script:
    return {"error": "No updates provided"}, 400

  try:
    script_str = "; ".join(script)
    es.update(index="users", id=userId, body={"script": script_str})

    updated_user = es.get(index="users", id=userId)

    return {
            "id": updated_user['_id'],
            "username": updated_user['_source']['username'],
            "password": updated_user['_source']['password']
        }, 200
  except Exception:
    return {"error": str(Exception)}, 500

def deleteUserById(userId):
  user, statusCode = userRepository.findById(userId)

  if statusCode == 404:
    return {"error": "User Not Found"}, 404

  jwt_identity = get_jwt_identity()

  if user['id'] != jwt_identity:
    return {"error": "Access Denied, UserId and JWT Identity Doesn't Match!"}, 403

  try:
    response = es.delete(index="users", id=userId)
    return response, 204
  except Exception:
    return {"error": str(Exception)}, 500