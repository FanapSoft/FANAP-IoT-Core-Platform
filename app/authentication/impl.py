
from .ssoclient import get_user_token_info, get_user_profile

from app.model import User
from app import db

def _check_token_is_valid(token):
    token_data = get_user_token_info(token)

    if not token_data or not token_data['active']:
        return None
    return token_data


def _add_new_user_with_profile(user_profile):
    new_user = User(
        username = user_profile['preferred_username'],
        user_id = user_profile['id'],
        given_name = user_profile.get('given_name','UNKNOWN'),
        family_name = user_profile.get('family_name','UNKNOWN'),
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user


def _check_user_in_db(token_data, user_token):
    user_id = int(token_data['sub'])

    usr = User.query.filter_by(
        user_id = user_id
    ).first()

    if usr:
        return usr

    user_profile = get_user_profile(user_token)

    if not user_profile:
        return None

    return _add_new_user_with_profile(user_profile)


def verify_user_token(token):
    # first check if token is valid

    token_data = _check_token_is_valid(token)

    if not token_data:
        return None
    
    
    return _check_user_in_db(token_data, token)