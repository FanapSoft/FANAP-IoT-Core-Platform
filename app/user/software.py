from app.model import Token, utils
from app.common import get_ok_response_body
from app import db


def _register_token(user):
    
    t = utils.unique_user_token()
    
    new_token = Token(
        token=t,
        user=user
    )

    # ToDo: Add cache entry
    db.session.add(new_token)
    db.session.commit()

    return new_token

def _get_token_by_user(user):
    return Token.query.filter_by(
        user = user
    ).first()

def software_register(user, params):
    # Check if current user is registered 

    tk = _get_token_by_user(user)

    if tk:
        token_str = tk.token
        state = "existed"
    else:
        t = _register_token(user)
        token_str = t.token
        state = "new"


    return get_ok_response_body(
        data=dict(
            token=token_str,
            state=state
        )
    )

def software_delete(user, params):
    tk = _get_token_by_user(user)

    if not tk:
        state = "not found"
    else:
        state = "deleted"
        # ToDo: Invalidate cache entry
        db.session.delete(tk)
        db.session.commit()

    return get_ok_response_body(
        data=dict(
            state=state
        )
    )
