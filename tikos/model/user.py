from werkzeug.security import check_password_hash, generate_password_hash

def model_user(name_user, login, password):
    model = {
        "nome_do_usuario":name_user.lower(),
        "login":login,
        "pass":generate_password_hash(password)
    }
    return model