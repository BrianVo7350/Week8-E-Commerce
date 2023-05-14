# from .auth_forms import SignUpForm, LogInForm
# from app.models import Users
# from email_validator import EmailNotValidError, validate_email
# from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import current_user, login_required, login_user, logout_user

# auth = Blueprint('auth',__name__,template_folder='auth_templates')

# @auth.route('/signup',methods=['GET','POST'])
# def signupPage():
#     form = SignUpForm()
#     if request.method == 'GET':
#         return render_template('signup.html',form=form)
    
#     if not form.validate():
#         flash("Sorry, what you  typed in was not valid, please try again","danger")
#         return render_template('signup.html',form=form)
    
#     email = form.email.data
#     password = form.password.data
#     first_name = form.first_name.data
#     last_name = form.last_name.data

#     email = check_email(email)
#     if not email:
#         flash("The email you entered is invalid","danger")
#         return render_template('signup.html',form=form)
    
#     if Users.query.filter_by(email=email).first():
#         flash("Email already in use","danger")
#         return render_template('signup.html',form=form,existing_username=True)
    
#     user = Users(email,password,first_name,last_name)

#     user.saveToDB()
#     login_user(user)
#     return redirect(url_for('homePage'))


# @auth.route('/login',methods=['GET','POST'])
# def loginPage():
#     form = LogInForm()
#     if request.method == 'GET':
#         return render_template('login.html',form=form)
    
#     if not form.validate():
#         flash("Sorry, what you typed in was not valid, please try again","danger")
#         return render_template('login.html',form=form)
    
#     if request.method == 'GET':
#         return render_template('login.html',form=form)

#     if not form.validate():
#         return render_template('login.html',form=form)
    
#     email = form.email.data
#     password = form.password.data

#     user = Users.query.filter_by(email=email).first()
    
#     if user and user.password == password:
#         login_user(user)
#         return redirect(url_for('homePage'))
#     else:
#         flash("There was no username")
#         return render_template('login.html',form=form)

# @auth.route('/logout',methods=['GET','POST'])
# def logoutUser():
#     logout_user()
#     return redirect(url_for('auth.loginPage'))

# def check_email(email):
#     try:
#         validated = validate_email(email)
#         email = validated['email']
#         return email.lower()
#     except EmailNotValidError as e:
#         return None
    