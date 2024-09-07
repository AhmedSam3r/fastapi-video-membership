from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
# pydantic validating all kind of data & load env vars
# from dotenv import load_dotenv
import os

from pathlib import Path

from fastapi.templating import Jinja2Templates

# Load the .env file
# load_dotenv()

# Print the value of ASTRADB_KEYSPACE to check if it's loaded
# print("ASTRADB_KEYSPACE =", os.getenv("ASTRADB_KEYSPACE"))

'''
to resolve this error:
    /home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/cassandra/cqlengine/management.py:545: 
    UserWarning: CQLENG_ALLOW_SCHEMA_MANAGEMENT environment variable is not set. 
    Future versions of this package will require this variable to enable management functions.
'''
os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"


class Settings(BaseSettings):
    # it doesn't read from the .env file & it raises issues
    #   Extra inputs are not permitted [type=extra_forbidden, input_value='examplekeyspace', input_type=str]
    # keyspace: str = Field(..., env="ASTRADB_KEYSPACE")
    # worked when we changed the fieldname similar to the one in the .env 
    # (in capital or small)
    astradb_keyspace: str
    db_client_id: str
    db_client_secret: str
    secret_key: str
    jwt_algorithm: str = Field(default="HS256")
    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = base_dir / "templates"
    templates: Jinja2Templates = Jinja2Templates(directory=str(template_dir))
    session_duration_sec: int = Field(default=600)

    class Config:
        env_file = '.env'


@lru_cache  # more efficient when i get call it, it's called one time and it will just create one instance, instead of creating more
def get_settings():
    return Settings()
