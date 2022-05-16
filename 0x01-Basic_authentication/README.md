# Basic authentication

This project contains tasks for learning to authenticate a user using the Basic authentication scheme.

## Tasks To Complete

+ [x] 0. **Simple-basic-API**
  + Setup and start server:
    ```powershell
    bob@dylan:~$ pip3 install -r requirements.txt
    ...
    bob@dylan:~$
    bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
     * Serving Flask app "app" (lazy loading)
    ...
    bob@dylan:~$
    ```
  + Use the API (in another tab or in your browser):
    ```powershell
    bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
    *   Trying 0.0.0.0...
    * TCP_NODELAY set
    * Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
    > GET /api/v1/status HTTP/1.1
    > Host: 0.0.0.0:5000
    > User-Agent: curl/7.54.0
    > Accept: */*
    >
    * HTTP 1.0, assume close after body
    < HTTP/1.0 200 OK
    < Content-Type: application/json
    < Content-Length: 16
    < Access-Control-Allow-Origin: *
    < Server: Werkzeug/1.0.1 Python/3.7.5
    < Date: Mon, 18 May 2020 20:29:21 GMT
    <
    {"status":"OK"}
    * Closing connection 0
    bob@dylan:~$
    ```

+ [x] 1. **Error handler: Unauthorized**
  + Edit [api/v1/app.py](api/v1/app.py):
    + Add a new error handler for this status code, the response must be:
      + A JSON: `{"error": "Unauthorized"}`.
      + Status code `401`.
      + You must use `jsonify` from Flask.
  + For testing this new error handler, add a new endpoint in [api/v1/views/index.py](api/v1/views/index.py).
    + Route: `GET /api/v1/unauthorized`.
    + This endpoint must raise a 401 error by using `abort` - [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/).
  + By calling `abort(401)`, the error handler for 401 will be executed.

+ [x] 2. **Error handler: Forbidden**
  + Edit [api/v1/app.py](api/v1/app.py):
    + Add a new error handler for this status code, the response must be:
      + A JSON: `{"error": "Forbidden"}`.
      + Status code `403`.
      + You must use `jsonify` from Flask.
  + For testing this new error handler, add a new endpoint in [api/v1/views/index.py](api/v1/views/index.py):
    + Route: `GET /api/v1/forbidden`.
    + This endpoint must raise a 403 error by using `abort` - [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/).
  + By calling `abort(403)`, the error handler for 403 will be executed.

+ [x] 3. **Auth class**
  + Create a class to manage the API authentication.
    + Create a folder [api/v1/auth](api/v1/auth).
    + Create an empty file [api/v1/auth/__init__.py](api/v1/auth/__init__.py).
    + Create the class `Auth`:
      + In the file [api/v1/auth/auth.py](api/v1/auth/auth.py).
      + Import `request` from flask.
      + Class name `Auth`.
      + Public method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` that returns `False` - `path` and `excluded_paths` will be used later, now, you don't need to take care of them.
      + Public method `def authorization_header(self, request=None) -> str:` that returns `None` - `request` will be the Flask request object.
      + Public method `def current_user(self, request=None) -> TypeVar('User'):` that returns `None` - `request` will be the Flask request object.
    + This class is the template for all authentication system you will implement.

+ [x] 4. **Define which routes don't need authentication**
  + Update the method `def require_auth(self, path: str, excluded_paths: List[str]) -> bool:` in `Auth` in [api/v1/auth/auth.py](api/v1/auth/auth.py) that returns `True` if the path is not in the list of strings `excluded_paths`:
    + Returns `True` if path is `None`.
    + Returns `True` if `excluded_paths` is `None` or empty.
    + Returns `False` if path is in `excluded_paths`.
    + You can assume `excluded_paths` contains string path always ending by a `/`.
    + This method must be slash tolerant: `path=/api/v1/status` and `path=/api/v1/status/` must be returned `False` if `excluded_paths` contains `/api/v1/status/`.

+ [x] 5. **Request validation!**
  + Now you will validate all requests to secure the API.
  + Update the method `def authorization_header(self, request=None) -> str:` in [api/v1/auth/auth.py](api/v1/auth/auth.py):
    + If request is `None`, returns `None`.
    + If `request` doesn't contain the header key `Authorization`, returns `None`.
    + Otherwise, return the value of the header request Authorization.
  + Update the file [api/v1/app.py](api/v1/app.py):
    + Create a variable `auth` initialized to None after the `CORS` definition.
    + Based on the environment variable `AUTH_TYPE`, load and assign the right instance of authentication to `auth`:
      + If `auth`:
        + Import `Auth` from `api.v1.auth.auth`.
        + Create an instance of `Auth` and assign it to the variable `auth`.
  + Now the biggest piece is the filtering of each request. For that you will use the Flask method `before_request`:
    + Add a method in [api/v1/app.py](api/v1/app.py) to handler `before_request`
      + If `auth` is `None`, do nothing.
      + If `request.path` is not part of this list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`, do nothing - you must use the method `require_auth` from the auth instance.
      + If `auth.authorization_header(request)` returns `None`, raise the error `401` - you must use `abort`.
      + If `auth.current_user(request)` returns `None`, raise the error `403` - you must use `abort`.

+ [x] 6. **Basic auth**
  + Create a class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that inherits from `Auth`. For the moment this class will be empty.
  + Update [api/v1/app.py](api/v1/app.py) for using `BasicAuth` class instead of `Auth` depending on the value of the environment variable `AUTH_TYPE`, If `AUTH_TYPE` is equal to `basic_auth`:
    + Import `BasicAuth` from `api.v1.auth.basic_auth`.
    + Create an instance of `BasicAuth` and assign it to the variable `auth`.
  + Otherwise, keep the previous mechanism with `auth` an instance of `Auth`.

+ [x] 7. **Basic - Base64 part**
  + Add the method `def extract_base64_authorization_header(self, authorization_header: str) -> str:` in the class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that returns the Base64 part of the `Authorization` header for a Basic Authentication:
    + Return None if `authorization_header` is `None`.
    + Return None if `authorization_header` is not a string.
    + Return None if `authorization_header` doesn't start by `Basic` (with a space at the end).
    + Otherwise, return the value after `Basic` (after the space).
    + You can assume `authorization_header` contains only one `Basic`.

+ [x] 8. **Basic - Base64 decode**
  + Add the method `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:` in the class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that returns the decoded value of a Base64 string `base64_authorization_header`:
    + Return `None` if `base64_authorization_header` is `None`.
    + Return `None` if `base64_authorization_header` is not a string.
    + Return `None` if `base64_authorization_header` is not a valid Base64 - you can use `try/except`.
    + Otherwise, return the decoded value as UTF8 string - you can use `decode('utf-8')`.

+ [x] 9. **Basic - User credentials**
  + Add the method `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in the class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that returns the user's email and password from the Base64 decoded value.
    + This method must return 2 values.
    + Return `None, None` if `decoded_base64_authorization_header` is `None`.
    + Return `None, None` if `decoded_base64_authorization_header` is not a string.
    + Return `None, None` if `decoded_base64_authorization_header` doesn't contain `:`.
    + Otherwise, return the user email and the user password - these 2 values must be separated by a `:`.
    + You can assume `decoded_base64_authorization_header` will contain only one `:`.

+ [x] 10. **Basic - User object**
  + Add the method `def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):` in the class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that returns the `User` instance based on the user's email and password.
    + Return `None` if `user_email` is `None` or not a string.
    + Return `None` if `user_pwd` is `None` or not a string.
    + Return `None` if your database (file) doesn't contain any `User` instance with email equal to `user_email` - you should use the class method `search` of the `User` to lookup the list of users based on their email. Don't forget to test all cases: "what if there is no user in DB?", etc.
    + Return `None` if `user_pwd` is not the password of the `User` instance found - you must use the method `is_valid_password` of `User`.
    + Otherwise, return the `User` instance.

+ [x] 11. **Basic - Overload current_user - and BOOM!**
  + Now, you have all the pieces for having a complete Basic authentication.
  + Add the method `def current_user(self, request=None) -> TypeVar('User')` in the class `BasicAuth` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) that overloads `Auth` and retrieves the `User` instance for a request:
    + You must use `authorization_header`.
    + You must use `extract_base64_authorization_header`.
    + You must use `decode_base64_authorization_header`.
    + You must use `extract_user_credentials`.
    + You must use `user_object_from_credentials`.
  + With this update, now your API is fully protected by a Basic Authentication. Enjoy!

+ [x] 12. **Basic - Allow password with ":"**
  + Improve the method `def extract_user_credentials(self, decoded_base64_authorization_header)` in [api/v1/auth/basic_auth.py](api/v1/auth/basic_auth.py) to allow password with `:`.

+ [x] 13. **Require auth with stars**
  + Improve `def require_auth(self, path, excluded_paths)` in [api/v1/auth/auth.py](api/v1/auth/auth.py) by allowing `*` at the end of excluded paths:
    + Example for `excluded_paths = ["/api/v1/stat*"]`:
      + `/api/v1/users` will return `True`.
      + `/api/v1/status` will return `False`.
      + `/api/v1/stats` will return `False`.
