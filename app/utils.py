import json
from pydantic import BaseModel, ValidationError

from app.schemas.userschemas import UserSignupSchema

from typing import Tuple, Dict


def valid_schema_or_error(raw_data: dict,
                          SchemaModel: BaseModel) -> Tuple[Dict, Dict]:
    data = {}
    errors = []
    error_str = ""
    try:
        # validated_data = UserSignupSchema(email=email, password=password, password_confirmation=password_confirmation)
        # pass it as kwargs which satisfy the previous older line
        validated_data = SchemaModel(**raw_data)
        data = validated_data.model_dump()
    except ValidationError as e:
        error_str = e.json()
        print(error_str)
    # added this to handle incorrect credentials exception and avoid internal errors 
    except ValueError as e:
        error_str = json.dumps(
            [
                {
                    'type': 'value_error',
                    'loc': 'email',
                    'msg': f'Value error {str(e)}'
                }
            ]
        )

    try:
        errors = json.loads(error_str) if error_str else {}
    except Exception as e:
        errors = [{"loc": "non_field_error", "msg": f"Unknown error {e}"}]

    return data, errors
