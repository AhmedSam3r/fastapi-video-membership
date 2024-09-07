Questions
1. What's BaseSettings class in pydantic_settings ? what does it do ?
2. What's lru_cache ?

Run server
```
uvicorn app.main:app
uvicorn package.filename:app_name
```

1. Video
    - where're we going to HOST it ? -> Youtube 
                                     -> Also we can use Private Video-> Udacity
                                     -> Vimeo, Wistia
                                     -> self hosted - nginx (hard to do) (3rd party service is recommended because of ease of it)
    - how're we going to perform ANALYTICS ? for user to resume where they have been watching
        - Lots of data e.g: 1 user watches 10 seconds on 100 videos = 1,000 rows per one user only
        - Lot of write 
        - Frame By Frame anaylsis -> 30 FPS per 120 second = 3,600 rows
        - Cassandra database

2. Members
    - Sign up
    - Login
    - Remember things for them
    - Email validation / confirmation
    - Payments (not in this course)


AstraDB - Managed NOSQL Cassandra 

- Database name
    - keyspace name
        - tables
    - keyspace name A
        - Table A
        - Table B


To run Jupyter Notebook, type
```
jupyter notebook
```


- Pydantic v2 has breaking changes compared to Pydantic v1
(
    /tmp/ipykernel_516519/3186061029.py:5: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.4/migration/
)
    - for example if you're validating fields, use validator in v1 like this:
        class UserSignupSchema(BaseModel):
            email: EmailStr
            password: SecretStr
            password_confirmation: SecretStr
            @validator('password_confirmation')
            def password_match(cls, v, values, **kwargs):
                password = values.get('password')
                password_confirmation = v
                if password != password_confirmation:
                    raise ValueError("passwords don't match")
                return v
    - for example if you're validating fields, use validator in v2 like this():
        class UserSignupSchema(BaseModel):
            email: EmailStr
            password: SecretStr
            password_confirmation: SecretStr

        @field_validator("password_confirmation")
        def passwords_match(cls,value: SecretStr, info: ValidationInfo):
            # print(type(cls), cls) # class 'pydantic._internal._model_construction.ModelMetaclass
            password = info.data.get('password').get_secret_value()
            password_confirmation = value.get_secret_value()
            if password != password_confirmation:
                raise ValueError("Passwords don't match")

            return password

    - another example to display the validated data as dict format:
            validated_data = UserSignupSchema(email=email, password=password, password_confirmation=password_confirmation)
            v1: validated_data.dict()
            v2: validated_data.model_dump()


        
Cookies:
   * Setting cookies in web applications is a common practice for various purposes, such as maintaining user sessions, storing user preferences, and tracking user behavior. 
   
   * The httponly attribute for cookies is a security feature that helps protect cookies from certain types of client-side attacks, like Cross-Site Scripting (XSS).
   
   * Security: When a cookie is marked as httponly, it can only be accessed and modified via HTTP requests. This means that client-side scripts, such as JavaScript, cannot access or modify the cookie. This helps protect the cookie from XSS attacks, where an attacker injects malicious scripts into a web page to steal cookies.
   
   * Preventing Unauthorized Access: By setting httponly, you reduce the risk of an attacker stealing user session cookies via JavaScript injection. This is an important security measure to protect user sessions and sensitive data.


redirect issue:
inside redirect method in shortcuts
response = responses.RedirectResponse(path, status_code=307)

* The issue you're encountering is due to the use of the HTTP status code 307 in your redirect response. 
A 307 status code means "Temporary Redirect" and is typically used to indicate that the requested resource can be found at a different URL, but the user agent should not change the HTTP method when making the redirected request. 
In other words, it preserves the original HTTP method.

In your code, the initial request is a POST request, and you are responding with a 307 Temporary Redirect to a GET request (the "/" path). This is likely why you're seeing the "405 Method Not Allowed" error, as the server is receiving a POST request to the "/" URL, which is not configured to handle POST requests.

To resolve this issue, you can do one of the following:

1. Change the HTTP status code to 303:
   
   ```python
   response = responses.RedirectResponse(path, status_code=303)
   ```

   A 303 status code is similar to 307 but explicitly specifies that the user agent should use a GET request when following the redirect.

2. If you intend to redirect to a GET request, you can change your redirect target to a URL that handles GET requests.

Choose the option that best aligns with your desired behavior. If you want the redirected request to use a GET method, option 2 is the better choice. If you want to preserve the original HTTP method, use a 303 status code as in option 1.

302 vs 302 status codes:
- 302:

    - The 302 status code indicates that the requested resource has been temporarily moved to a different URL.
    - The client is allowed to change the request method (e.g., from POST to GET) when following the redirect.
    - This status code is often used in scenarios where the original HTTP method can be safely changed for the redirected request.

- 303:
- The 303 status code also indicates that the requested resource is temporarily available at a different URL.
- However, the client is explicitly instructed to use a GET request when making the redirected request, regardless of the  original request method. In other words, the request method is not preserved.
- The 303 status code is useful when you want to ensure that the client always uses a GET request for the redirected URL, irrespective of the original request method.




- noqa (no quality assurance) is a comment that is typically used to indicate to code analysis tools (like linters) to ignore any "unused import" warnings. It's a way to suppress warnings or errors that might be raised because you're importing everything from the module but not using all the imported items.

- changed the app initialization be in the package __init__ file to imported without circular imports errors

- Exceptions
    - login_required_exception_handler() if it exists or not won't cause issues, why ? 
        since there's a generic method http_exception(HTTPException) that handles the generic exception error raising  

- we can't access the request.user inside our APIs
    - AssertionError: AuthenticationMiddleware must be installed to access request.user

- docstrings in empty class works instead of pass

- I got that error when awaiting non async function, declared by mistake videos API without "async" (not focusing lead to mistakes which I learn from):
    Traceback (most recent call last):
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/uvicorn/protocols/http/h11_impl.py", line 408, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/uvicorn/middleware/proxy_headers.py", line 84, in __call__
        return await self.app(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/fastapi/applications.py", line 292, in __call__
        await super().__call__(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/applications.py", line 122, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/middleware/errors.py", line 184, in __call__
        raise exc
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/middleware/errors.py", line 162, in __call__
        await self.app(scope, receive, _send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/middleware/authentication.py", line 48, in __call__
        await self.app(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 79, in __call__
        raise exc
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/middleware/exceptions.py", line 68, in __call__
        await self.app(scope, receive, sender)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 20, in __call__
        raise e
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/fastapi/middleware/asyncexitstack.py", line 17, in __call__
        await self.app(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/routing.py", line 718, in __call__
        await route.handle(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/routing.py", line 276, in handle
        await self.app(scope, receive, send)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/starlette/routing.py", line 66, in app
        response = await func(request)
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/fastapi/routing.py", line 273, in app
        raw_response = await run_endpoint_function(
    File "/home/ahmed/development/fastpi_course/venv/lib/python3.10/site-packages/fastapi/routing.py", line 190, in run_endpoint_function
        return await dependant.call(**values)
    <b> 
    File "/home/ahmed/development/fastpi_course/app/decorators.py", line 57, in wrapper
        return await func(request, *args, **kwargs)
    TypeError: object HTMLResponse can't be used in 'await' expression
    <b>


- We can add exceptions.py file in each module like users and videos or make it in the main app directory 
    each has its pros and cons.
    - making separate exceptions per each app (users/videos) make it easier to drag and drop but configs will be scattered
    - making central exceptions file will make it easier to add stuff but it will be messy if the app gets bigger
Example on routers 
- FASTAPI documentation
```
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   └── routers
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── internal
│       ├── __init__.py
│       └── admin.py
```
- Our Implementation
```
├── app
│   ├── users
│   │   ├── auth.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── __pycache__
│   │   ├── security.py
│   │   └── validators.py
│   ├── utils.py
│   └── videos
│       ├── extractors.py
│       ├── __init__.py
│       ├── models.py
│       ├── __pycache__
│       ├── routers.py
│       └── schemas.py
│   ├── backend.py
│   ├── config.py
│   ├── db.py
│   ├── decorators.py
│   ├── exceptions.py
│   ├── handlers.py
│   ├── __init__.py
│   ├── main.py
│   ├── schemas
│   │   ├── __pycache__
│   │   └── userschemas.py

```
- next is read now from the login.html form where it's passed from the login get view as form field

- To check youtube iframe documentation check the following:
        https://developers.google.com/youtube/player_parameters
