from functools import wraps
from flask import request, Response
from json import loads
from os.path import isfile


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    auth_path = '/etc/check_auth.json'

    if not isfile(auth_path):
        return False

    with open(auth_path) as f:
        auth = loads(f.read())

    for entry in auth:
        if username == entry['username'] and password == entry['password']:
            return True
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
