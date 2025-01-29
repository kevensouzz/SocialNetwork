from flask import Blueprint, jsonify, request
from src.services.mailService import sendCodemail, verifyCodemail
from src.repositories import codemailRepository

cm_bp = Blueprint('codemails', __name__, url_prefix='/codemails')

@cm_bp.route('', methods=['GET'])
def readAll():
  result, statusCode = codemailRepository.findAll()
  return jsonify(result), statusCode

@cm_bp.route('/send', methods=['POST'])
def send():
  email = request.json.get('email')
  action = request.json.get('action')
  result, statusCode = sendCodemail(email, action)
  return jsonify(result), statusCode

@cm_bp.route('/verify', methods=['POST'])
def verify():
  email = request.json.get('email')
  code = request.json.get('code')
  action = request.json.get('action')
  result, statusCode = verifyCodemail(email, code, action)
  return jsonify(result), statusCode