from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    ValidationInfo,
    root_validator
)

from app.users.models import User
from app.users.auth import (
    authenticate,
    login,
    verify_token
)
from pydantic import model_serializer
from app import config

settings = config.get_settings()

class UserSignupSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirmation: SecretStr

    @field_validator("password_confirmation")
    def passwords_match(cls, field: SecretStr, info: ValidationInfo):
        password = info.data.get('password').get_secret_value()
        password_confirmation = field.get_secret_value()
        if password != password_confirmation:
            raise ValueError("Passwords don't match")
        # instead of returning password, why ? in order to display it in the secretstr format
        return info.data.get('password')

    @field_validator("email")
    def email_exists(cls, field: EmailStr, info: ValidationInfo):
        q = User.objects.filter(email=field)
        if q.count() != 0:
            raise ValueError('Email is not available')

        return field


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr
    session_id: str = None

    @field_validator("email")
    def email_exists(cls, value: EmailStr, info: ValidationInfo):
        q = User.objects.filter(email=value)
        if q.count() == 0:
            raise ValueError('Please sign up')

        return value

    @model_serializer(mode="plain")
    def validate_user(self, value, **kawrgs):
        '''
        The return of this function is returned when we use the UserLoginSchema
        to solve this error:
            1)pydantic.errors.PydanticUserError: Unrecognized model_serializer function signature for <function UserLoginSchema.validate_user at 0x7f4ee61c3eb0> with `mode=plain`:(self, value, info)
        I made the function delecaration arguments  (mode="plain)
            2)pydantic.errors.PydanticUserError: `@model_serializer` must be applied to instance methods
            def validate_user(self, value, **kawrgs) 
        instead of 
            def validate_user(cls, value, info: ValidationInfo)
        '''
        err_msg = "Incorrect Credentials, please try again"
        email = self.email
        password = self.password
        if email is None or password is None:
            raise ValueError(err_msg)
        password = password.get_secret_value()
        user = authenticate(email, password)
        if user is None:
            raise ValueError(err_msg)
        
        token = login(user, settings.session_duration_sec)

        return {'session_id': token}
