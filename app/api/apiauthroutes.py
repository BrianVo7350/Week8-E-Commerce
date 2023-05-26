from . import api
from ..models import Users
from flask import request
from werkzeug.security import check_password_hash
from .apiauthhelper import basic_auth

@api.post('/Signup')
def signUpAPI():
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

    user = Users(first_name, last_name, email, password)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': "You have successfully created an account."
    }, 201


@api.post('/Login')
@basic_auth.login_required
def loginAPI():
    # data = request.json

    # email = data['email']
    # password = data['password']

    return {
        'status': 'ok',
        'message': "You have successfully logged in.",
        'data': basic_auth.current_user().to_dict()
    }, 200