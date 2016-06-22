from flask_login import LoginManager, login_required, login_user, \
    current_user, logout_user
from flask import render_template, request, redirect, url_for
from models.user import User
import passwordmeter
import logging
from configuration.configuration import Configurator

configurator = Configurator()


def register_auth(app):

    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.errorhandler(404)
    def page_not_found(self):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def unauthorized(self):
        return render_template('401.html'), 401

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.get(id=user_id)
        except Exception as userNotFound:
            logging.info('User not found (user loader)', userNotFound)

    @login_manager.request_loader
    def load_user_from_request(request):
        if not request.form:
            return None

        try:
            user = User.get(email=request.form['email'])
        except Exception as userNotFound:
            logging.info('User not found (user loader)', userNotFound)
            return None

        if user.check(request.form['password']):
            return user
        return None

    @app.route('/', methods=['GET'])
    def auth_form():
        return render_template(
            'auth.html',
            message=request.args.get('message')
        )

    @app.route('/login', methods=['POST'])
    def login():

        try:
            user = User.get(email=request.form['email'])
        except Exception as userNotFound:
            logging.info('User not found on login {0}'.format(userNotFound))
            return redirect(
                url_for('auth_form', message='user_not_found')
            )

        if user.check(request.form['password']):
            login_user(user)
            return redirect(url_for(configurator.get('on_login_success')))
        else:
            return redirect(
                url_for('auth_form', message='wrong_password')
            )

    @app.route('/logout', methods=['GET'])
    @login_required
    def logout():
        current_user.authenticated = False
        logout_user()
        return redirect(url_for('auth_form'))

    @app.route('/register', methods=['POST'])
    def register():

        if request.form['email'] != request.form['email1']:
            return redirect(url_for('new', message='email'))

        if request.form['password'] != request.form['password']:
            return redirect(url_for('new', message='password'))

        if passwordmeter.test(request.form['password'])[0] < 0.4:
            return redirect(url_for('new', message='password_weak'))

        l = len(request.form['fullname'])
        if l < 1 or l > 40:
            return redirect(url_for('new', message='fullname_invalid'))

        User.create(
            request.form['email'],
            request.form['password'],
            fullname=request.form['fullname'],
        ).save()

        return redirect(url_for('index', message='register_success'))

    @app.route('/nouveau-compte', methods=['GET'])
    @login_required
    def new():
        return render_template(
            'register.html', message=request.args.get('message')
        )
