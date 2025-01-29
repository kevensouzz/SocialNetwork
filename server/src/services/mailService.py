from flask_mailman import EmailMessage
from database import es
from src.repositories import codemailRepository
from datetime import datetime, timedelta
import secrets, time, hashlib, hmac
from src.repositories import userRepository

def generateCode(email):
  currentTime = int (time.time())
  secret_key = secrets.token_bytes(16)
  message = f"{email}{currentTime}".encode()
  hashCode = hmac.new(secret_key, message, hashlib.sha256).hexdigest()

  resetCode = int(hashCode[:6], 16) % 1000000

  return f"{resetCode:06d}"

def saveCodemail(email, code, action):
  document = {
      "email": email,
      "code": code,
      "action": action,
      "used": False,
      "timestamp": datetime.now()
  }
  
  try:
      response = es.index(index="codemails", id=code, body=document)
      return response
  except Exception as e:
      print(f"Error indexing document: {str(e)}")
      return None
  
def useCodemail(code):
  try:
    es.update(index="codemails", id=code, body={"script": "ctx._source.used = true"})
    return {"message": "Codemail marked as used successfully"}, 200
  except Exception as e:
    return {"error": str(e)}, 500

def generateResetBody(code):
  return f"""
  <html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); padding: 20px;">
          <tr>
              <td style="text-align: center; padding: 20px 0;">
                  <h1 style="color: #0000c8; font-size: 24px;">CÓDIGO DE RECUPERAÇÃO</h1>
              </td>
          </tr>
          <tr>
              <td style="padding: 10px 20px; text-align: center;">
                  <p style="color: #555555; font-size: 16px;">
                      Recebemos uma solicitação para resetar sua senha. Por favor,
                      use o seguinte código para continuar o processo de recuperação:
                  </p>
                  <p style="font-size: 32px; color: #0000c8; font-weight: bold; margin: 20px 0;">
                      {code}
                  </p>
                  <p style="color: #555555; font-size: 16px;">
                      Esse código será expirado em 5 minutos. Se não usá-lo nesse período,
                      ignore este email e <a href="#" style="color: #0000c8;">solicite outro código.</a>
                  </p>
              </td>
          </tr>
          <tr>
              <td style="padding: 20px; text-align: center;">
                  <a href="#" style="background-color: #0000c8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                      Resetar senha
                  </a>
              </td>
          </tr>
          <tr>
              <td style="padding: 10px 20px; text-align: center; color: #777777; font-size: 12px;">
                  <p>Em caso de dúvidas, contate a equipe de suporte.</p>
                  <p>&copy; 2025 Keven Souza. Todos os direitos reservados.</p>
              </td>
          </tr>
      </table>
  </body>
  </html>
  """

def generateVerifyBody(code):
  return f"""
  <html>
  <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
      <table style="width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); padding: 20px;">
          <tr>
              <td style="text-align: center; padding: 20px 0;">
                  <h1 style="color: #0000c8; font-size: 24px;">CÓDIGO DE VERIFICAÇÃO</h1>
              </td>
          </tr>
          <tr>
              <td style="padding: 10px 20px; text-align: center;">
                  <p style="color: #555555; font-size: 16px;">
                      Recebemos uma solicitação para verificar sua conta. Por favor,
                      use o seguinte código para continuar o processo de verificação:
                  </p>
                  <p style="font-size: 32px; color: #0000c8; font-weight: bold; margin: 20px 0;">
                      {code}
                  </p>
                  <p style="color: #555555; font-size: 16px;">
                      Esse código será expirado em 5 minutos. Se não usá-lo nesse período,
                      ignore este email e <a href="#" style="color: #0000c8;">solicite outro código.</a>
                  </p>
              </td>
          </tr>
          <tr>
              <td style="padding: 20px; text-align: center;">
                  <a href="#" style="background-color: #0000c8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                      Verificar conta
                  </a>
              </td>
          </tr>
          <tr>
              <td style="padding: 10px 20px; text-align: center; color: #777777; font-size: 12px;">
                  <p>Em caso de dúvidas, contate a equipe de suporte.</p>
                  <p>&copy; 2025 Keven Souza. Todos os direitos reservados.</p>
              </td>
          </tr>
      </table>
  </body>
  </html>
  """

def sendCodemail(email, action):
  if not email or not action:
    return {"error": "Mandatory fields aren't filled in"}, 400
  
  if action == 'reset':
    userByEmail, userByEmail_statusCode = userRepository.findByEmail(email)

    if userByEmail_statusCode != 200:
      return {"error": "This email is not registered here"}, 403

  code = generateCode(email)
  
  if action == 'reset':
    subject = "USE ESSE CÓDIGO PARA RESETAR SUA SENHA | TALK CHAIN"
    body = generateResetBody(code)
  elif action == 'verify':
    subject = "USE ESSE CÓDIGO PARA VERIFICAR SUA CONTA | TALK CHAIN"
    body = generateVerifyBody(code)
  else:
    return {"Error": "Ivalid action specified"}, 400
  
  saveCodemail(email, code, action)

  try:
    msg = EmailMessage(
      subject=subject,
      body=body,
      to=[email]
    )

    msg.content_subtype = 'html'
    msg.send()

    return {"Message": "Email successfully sent!"}, 200
  except Exception as e:
     return {'error': str(e)}, 500
  
def verifyCodemail(email, code, action):
  if not email or not code or not action:
    return {"error": "Mandatory fields aren't filled in"}, 400

  # verificar se o código está no banco de dados
  existingCode, existingCode_statusCode = codemailRepository.findByCode(code)

  if existingCode_statusCode != 200:
    return {"Error": "Codemail not found"}, 404
  
  # verificar se o usuário que está submetendo é o dono do código pelo email
  if existingCode['email'] != email:
    return {"Error": "You aren't the code's owner"}, 401
  
  if existingCode['used'] == True:
    return {"Error": "This code is no longer valid"}, 410

  # verificar se a ação do código corresponde
  if existingCode['action'] != action:
    return {"Error": "This code wasn't generated for this purpose"}, 401

  # verificar se este mesmo usuário não solicitou outro código com a mesma ação posteriormente
  latestCode, latestCode_statusCode = codemailRepository.findLatestCodeByEmailAndAction(email, action)

  if latestCode_statusCode == 200:
      if latestCode and latestCode['code'] != code:
          return {"Error": "A new code has been generated for this action. Please use the latest code."}, 403
  else:
      print(f"Error finding latest code: {latestCode_statusCode}")
  
  # verificar se o código foi gerado a menos de 5 minutos
  codeTimestamp = existingCode['timestamp']
  currentTime = datetime.now()

  if isinstance(codeTimestamp, str):
    codeTimestamp = datetime.strptime(codeTimestamp, '%Y-%m-%dT%H:%M:%S.%f')

  if currentTime - codeTimestamp > timedelta(minutes=5):
    return {"Error": "The code has expired"}, 410

  useCodemail(code)

  return {"message": "Codemail verified successfully"}, 200