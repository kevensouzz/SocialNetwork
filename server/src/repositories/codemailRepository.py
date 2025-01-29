from database import es

def findAll():
  response = es.search(index="codemails", body={"query": {"match_all": {}}}, size=100)

  codemails = [
    {"id": hit["_id"], "code": hit["_source"]["code"], "email": hit["_source"]["email"], "action": hit["_source"]["action"],"used": hit["_source"]["used"], "timestamp": hit["_source"]["timestamp"]}
    for hit in response['hits']['hits']
  ]

  return codemails, 200

def findByCode(code):
  try:
    response = es.get(index="codemails", id=code)

    return {
        "code": response["_id"],
        "action": response["_source"]["action"],
        "email": response["_source"]["email"],
        "used": response["_source"]["used"],
        "timestamp": response["_source"]["timestamp"],
    }, 200
  except Exception:
    return {"error": "Codemail Not Found"}, 404
  
def findLatestCodeByEmailAndAction(email, action):
  try:
      query = {
          "query": {
              "bool": {
                  "must": [
                      {"term": {"email.keyword": email}},
                      {"term": {"action.keyword": action}}
                  ]
              }
          },
          "sort": [
              {"timestamp": {"order": "desc"}}
          ],
          "size": 1
      }

      response = es.search(index="codemails", body=query)

      if response['hits']['total']['value'] > 0:
          latestCode = response['hits']['hits'][0]['_source']
          return latestCode, 200
      else:
          return None, 404
  except Exception as e:
      print(f"Error searching for latest code: {str(e)}")
      return None, 500
