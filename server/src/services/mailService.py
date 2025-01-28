from flask_mailman import EmailMessage
import secrets, time, hashlib, hmac
from database import es
import datetime

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
      response = es.index(index="codemail", body=document)
      return response
  except Exception as e:
      print(f"Error indexing document: {str(e)}")
      return None

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
  
# def verifyCodemail():