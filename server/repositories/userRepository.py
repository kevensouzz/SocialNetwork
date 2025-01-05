from database import es

def findAll():
  response = es.search(index="users", body={"query": {"match_all": {}}}, size=100)

  users = [
    {"id": hit["_id"], "username": hit["_source"]["username"], "password": hit["_source"]["password"]}
    for hit in response['hits']['hits']
  ]

  return users, 200

def findById(userId):
  try:
    response = es.get(index="users", id=userId)

    return {
        "id": response["_id"],
        "username": response["_source"]["username"],
        "password": response["_source"]["password"]
    }, 200
  except Exception:
    return {"error": "User Not Found"}, 404
  
def findByUsername(username):
  try:
    user = es.search(index="users", body={"query": {"term": {"username.keyword": username}}})

    if user['hits']['total']['value'] == 0:
      return {"error": "User Not Found"}, 404
    
    userData = user['hits']['hits'][0]['_source']
    userId = user['hits']['hits'][0]['_id']

    return {
      "id": userId,
      "username": userData['username'],
      "password": userData['password']
    }, 200
  except Exception as e:
    return {"error": str(e)}, 500