import bcrypt


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
