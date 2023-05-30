from . import api
from ..models import Users
from flask import request
from werkzeug.security import check_password_hash
from .apiauthhelper import basic_auth_required, basic_auth
import requests

@api.post('/Signup')
def SignUpAPI():
    data = request.json

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']
    print(data)

    user = Users.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email is already in use.'
        }, 400
    
    user = Users(email, password, first_name,last_name)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': "You have successfully created an account."
    }, 201


@api.post('/Login')
@basic_auth_required
def LoginAPI():
    data = requests.json

    email = data['email']
    password = data['password']

    user = Users.query.filter_by(email = email).first()
    if user:
        if check_password_hash(user.password, password):
            return {
                'status' : 'ok',
                'message' : 'You have Logged in',
                'data': user.to_dict()
            }, 200
        else:
            return {
                'status': 'not ok',
                'message' : 'Incorrect password',
            }, 400    
    else:
        return {
            'status' : 'not ok',
            'message' : 'Email already exists',
        }, 400