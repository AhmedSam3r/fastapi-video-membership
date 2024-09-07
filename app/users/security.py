from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

'''
    better to make it this way to provide abstract methods
    in case we want to the change the algorithm internally,
    it would be easier, since other parts of the app already calling these functions
'''


def generate_hash(password):
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(password_hash, password_raw):
    ph = PasswordHasher()
    verified = False
    msg = ""
    try:
        verified = ph.verify(password_hash, password_raw)
    except VerifyMismatchError:
        msg = "Invalid password"
    except Exception as e:
        msg = f"unexpected error {e}"

    return verified, msg
