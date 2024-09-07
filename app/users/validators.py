# installed package email_validator
from email_validator import EmailNotValidError, validate_email

def _validate_email(email: str):
    msg = ""
    valid = False
    try:
        validated_email = validate_email(email)
        email = validated_email.email
        valid = True
    except EmailNotValidError as e:
        msg = str(e)

    return valid, msg, email
