from resource.userObject import UserModel
from werkzeug.security import safe_str_cmp #string comparision 


def authenticate(name, password):
    user = UserModel.findby_username(name)
    if user and safe_str_cmp(user.password, password):
        return user


def get_identity(payLoad):
    user_id = payLoad["identity"]
    return UserModel.findby_id(user_id)


