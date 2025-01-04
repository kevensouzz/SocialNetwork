from database import es
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token

def createUser(username, password):
  existing_user = es.search(index="users", body={"query": {"term": {"username.keyword": username}}})
    
  if existing_user['hits']['total']['value'] > 0:
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
  user = es.search(index="users", body={"query": {"term": {"username.keyword": username}}})
  
  if user['hits']['total']['value'] == 0:
    return {"error": "invalid credentials"}, 401
  
  userData = user['hits']['hits'][0]['_source']

  if not check_password_hash(userData['password'], password):
    return {"error": "invalid credentials"}, 401
  
  userId = user['hits']['hits'][0]['_id']
  access_token = create_access_token(identity=userId)

  return {"JWT": access_token}, 200

def getAllUsers():
  response = es.search(index="users", body={"query": {"match_all": {}}}, size=100)

  users = [
    {"id": hit["_id"], "username": hit["_source"]["username"], "password": hit["_source"]["password"]}
    for hit in response['hits']['hits']
  ]

  return users, 200
  
def getUserById(userId):
  try:
    response = es.get(index="users", id=userId)

    return {
        "id": response["_id"],
        "username": response["_source"]["username"],
        "password": response["_source"]["password"]
    }, 200
  except Exception:
    return {"error": "User Not Found"}, 404
  
def updateUserById(userId, username=None):
  user, statusCode = getUserById(userId)

  if statusCode == 404:
    return {"error": "User Not Found"}, 404

  script = []

  if username:
    existing_user = es.search(index="users", body={"query": {"term": {"username.keyword": username}}})
    
    if existing_user['hits']['total']['value'] > 0 and existing_user['hits']['hits'][0]['_id'] != userId:
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
  user, statusCode = getUserById(userId)

  if statusCode == 404:
    return {"error": "User Not Found"}, 404

  try:
    response = es.delete(index="users", id=userId)
    return response, 204
  except Exception:
    return {"error": str(Exception)}, 500