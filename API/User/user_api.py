from flasgger import swag_from
from flask import request, jsonify, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from config import Config
from database import db
from models.user import User

user_blueprint = Blueprint('user_api', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY, options={"verify_signature": False})
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@user_blueprint.route('/login')
@swag_from('login.yaml')
def login():
    """
    Login method
    Returns: JSON with Token or Error

    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # Make sure password is correct and create token valid for 30 minutes
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'user_id': user.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            },
            Config.SECRET_KEY
        )
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@user_blueprint.route('/user', methods=['POST'])
@swag_from('create_user.yaml')
def create_user():
    """
    Creates a new user in the DB
    Returns: JSON
    """
    try:
        data = request.get_json(force=True)
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': f'User {new_user.username} created!'})
    except KeyError as e:
        return jsonify({'error': 'Missing values in request'}), 400

