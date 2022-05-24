# User Authentication Service

This project contains tasks for learning to create a user authentication service.

## Requirements

+ SQLAlchemy 1.3.x
+ pycodestyle 2.5
+ bcrypt
+ python3 3.7

## Tasks To Complete

+ [x] 0. **User model**<br />[user.py](user.py) contains a SQLAlchemy model named `User` for a database table named `users` (by using the [mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping) of SQLAlchemy) and meets the following requirements:
  + The model will have the following attributes:
    + `id`, the integer primary key.
    + `email`, a non-nullable string.
    + `hashed_password`, a non-nullable string.
    + `session_id`, a nullable string.
    + `reset_token`, a nullable string.

+ [x] 1. **create user**<br />[db.py](db.py) contains a completion of the `DB` class provided below to implement the `add_user` method according to the given requirements:
  + &nbsp;
    ```python
    #!/usr/bin/env python3
    """DB module.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import Session
    from sqlalchemy.ext.declarative import declarative_base

    from user import Base


    class DB:
        """DB class.
        """

        def __init__(self) -> None:
            """Initialize a new DB instance.
            """
            self._engine = create_engine("sqlite:///a.db", echo=False)
            Base.metadata.drop_all(self._engine)
            Base.metadata.create_all(self._engine)
            self.__session = None

        @property
        def _session(self) -> Session:
            """Memoized session object.
            """
            if self.__session is None:
                DBSession = sessionmaker(bind=self._engine)
                self.__session = DBSession()
            return self.__session
    ```
  + Note that `DB._session` is a private property and hence should NEVER be used from outside the DB class.
  + Implement the `add_user` method, which has two required string arguments: `email` and `hashed_password`, and returns a `User` object. The method should save the user to the database. No validations are required at this stage.

+ [x] 2. **Find user**<br />[db.py](db.py) contains the following updates:
  + Implement the `DB.find_user_by` method. This method takes in arbitrary keyword arguments and returns the first row found in the `users` table as filtered by the method’s input arguments. No validation of input arguments required at this point.
  + Make sure that SQLAlchemy’s `NoResultFound` and `InvalidRequestError` are raised when no results are found, or when wrong query arguments are passed, respectively.
  + **Warning:**
    + `NoResultFound` has been moved from `sqlalchemy.orm.exc` to `sqlalchemy.exc` between the version 1.3.x and 1.4.x of SQLAchemy - please make sure you are importing it from `sqlalchemy.orm.exc`.

+ [x] 3. **update user**<br />[db.py](db.py) contains the following updates:
  + Implement the `DB.update_user` method that takes as arguments a required `user_id` integer, an arbitrary keyword arguments, and returns `None`.
  + The method will use `find_user_by` to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.
  + If an argument that does not correspond to a user attribute is passed, raise a `ValueError`.

+ [x] 4. **Hash password**<br />[auth.py](auth.py) contains a `_hash_password` method that takes in a password string arguments and returns bytes, which is a salted hash of the input password, hashed with `bcrypt.hashpw`.

+ [x] 5. **Register user**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.register_user` in the `Auth` class provided below:
    ```python
    from db import DB


    class Auth:
        """Auth class to interact with the authentication database.
        """

        def __init__(self):
            self._db = DB()
    ```
  + Note that `Auth._db` is a private property and should NEVER be used from outside the class.
  + `Auth.register_user` should take mandatory `email` and `password` string arguments and return a `User` object.
  + If a user already exist with the passed `email`, raise a `ValueError` with the message `User <user's email> already exists`.
  + If not, hash the password with `_hash_password`, save the user to the database using `self._db` and return the `User` object.

+ [x] 6. **Basic Flask app**<br />[app.py](app.py) contains a basic Flask app with the following requirements:
  + Create a Flask app that has a single `GET` route (`"/"`) and use `flask.jsonify` to return a JSON payload of the form:
    ```json
    {"message": "Bienvenue"}
    ```
  + Add the following code at the end of the module:
    ```python
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port="5000")
    ```

+ [x] 7. **Register user**<br />[app.py](app.py) contains the following updates:
  + Implement the end-point to register a user. Define a `users` function that implements the `POST /users` route.
  + Import the `Auth` object and instantiate it at the root of the module as such:
    ```python
    from auth import Auth


    AUTH = Auth()
    ```
  + The end-point should expect two form data fields: `"email"` and `"password"`. If the user does not exist, the end-point should register it and respond with the following JSON payload:
    ```json
    {"email": "<registered email>", "message": "user created"}
    ```
  + If the user is already registered, catch the exception and return a JSON payload of the form
    ```json
    {"message": "email already registered"}
    ```
    and return a 400 status code.
  + Remember that you should only use `AUTH` in this app. `DB` is a lower abstraction that is proxied by `Auth`.

+ [x] 8. **Credentials validation**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.valid_login` method. It should expect `email` and `password` required arguments and return a boolean.
  + Try locating the user by email. If it exists, check the password with `bcrypt.checkpw`. If it matches return `True`. In any other case, return `False`.

+ [x] 9. **Generate UUIDs**<br />[auth.py](auth.py) contains the following updates:
  + Implement a `_generate_uuid` function in the `auth` module. The function should return a string representation of a new UUID. Use the `uuid` module.
  + Note that the method is private to the `auth` module and should **NOT** be used outside of it.

+ [x] 10. **Get session ID**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.create_session` method. It takes an `email` string argument and returns the session ID as a string.
  + The method should find the user corresponding to the email, generate a new UUID and store it in the database as the user’s `session_id`, then return the session ID.
  + Remember that only public methods of `self._db` can be used.

+ [x] 11. **Log in**<br />[app.py](app.py) contains the following updates:
  + Implement a `login` function to respond to the `POST /sessions` route.
  + The request is expected to contain form data with `"email"` and a `"password"` fields.
  + If the login information is incorrect, use `flask.abort` to respond with a 401 HTTP status.
  + Otherwise, create a new session for the user, store it the session ID as a cookie with key `"session_id"` on the response and return a JSON payload of the form:
    ```json
    {"email": "<user email>", "message": "logged in"}
    ```

+ [x] 12. **Find user by session ID**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.get_user_from_session_id` method. It takes a single `session_id` string argument and returns the corresponding `User` or `None`.
  + If the session ID is `None` or no user is found, return `None`. Otherwise return the corresponding user.
  + Remember to only use public methods of `self._db`.

+ [x] 13. **Destroy session**<br />[auth.py](auth.py) contains the following updates:
  + Implement `Auth.destroy_session`. The method takes a single `user_id` integer argument and returns `None`.
  + The method updates the corresponding user’s session ID to `None`.
  + Remember to only use public methods of `self._db`.

+ [x] 14. **Log out**<br />[app.py](app.py) contains the following updates:
  + Implement a `logout` function to respond to the `DELETE /sessions` route.
  + The request is expected to contain the session ID as a cookie with key `"session_id"`.
  + Find the user with the requested session ID. If the user exists destroy the session and redirect the user to `GET /`. If the user does not exist, respond with a 403 HTTP status.

+ [x] 15. **User profile**<br />[app.py](app.py) contains the following updates:
  + Implement a `profile` function to respond to the `GET /profile` route.
  + The request is expected to contain a `session_id` cookie. Use it to find the user. If the user exist, respond with a 200 HTTP status and the following JSON payload:
    ```json
    {"email": "<user email>"}
    ```
  + If the session ID is invalid or the user does not exist, respond with a 403 HTTP status.

+ [x] 16. **Generate reset password token**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.get_reset_password_token` method. It takes an `email` string argument and returns a string.
  + Find the user corresponding to the email. If the user does not exist, raise a `ValueError` exception. If it exists, generate a UUID and update the user’s `reset_token` database field. Return the token.

+ [x] 17. **Get reset password token**<br />[app.py](app.py) contains the following updates:
  + Implement a `get_reset_password_token` function to respond to the `POST /reset_password` route.
  + The request is expected to contain form data with the `"email"` field.
  + If the email is not registered, respond with a 403 status code. Otherwise, generate a token and respond with a 200 HTTP status and the following JSON payload:
    ```json
    {"email": "<user email>", "reset_token": "<reset token>"}
    ```

+ [x] 18. **Update password**<br />[auth.py](auth.py) contains the following updates:
  + Implement the `Auth.update_password` method. It takes `reset_token` string argument and a `password` string argument and returns `None`.
  + Use the `reset_token` to find the corresponding user. If it does not exist, raise a `ValueError` exception.
  + Otherwise, hash the password and update the user’s `hashed_password` field with the new hashed password and the `reset_token` field to `None`.

+ [x] 19. **Update password end-point**<br />[app.py](app.py) contains the following updates:
  + Implement the `update_password` function in the `app` module to respond to the `PUT /reset_password` route.
  + The request is expected to contain form data with fields `"email"`, `"reset_token"` and `"new_password"`.
  + Update the password. If the token is invalid, catch the exception and respond with a 403 HTTP code.
  + If the token is valid, respond with a 200 HTTP code and the following JSON payload:
    ```json
    {"email": "<user email>", "message": "Password updated"}
    ```

+ [x] 20. **End-to-end integration test**
  + Start the Flask app you created in the previous tasks. Open a new terminal window.
  + Create a new module called [main.py](main.py). Create one function for each of the following sub tasks. Use the `requests` module to query your web server for the corresponding end-point. Use `assert` to validate the response’s expected status code and payload (if any) for each sub task:
    + `register_user(email: str, password: str) -> None`.
    + `log_in_wrong_password(email: str, password: str) -> None`.
    + `log_in(email: str, password: str) -> str`.
    + `profile_unlogged() -> None`.
    + `profile_logged(session_id: str) -> None`.
    + `log_out(session_id: str) -> None`.
    + `reset_password_token(email: str) -> str`.
    + `update_password(email: str, reset_token: str, new_password: str) -> None`.
  + Copy the following code at the end of the `main` module:
    ```python
    EMAIL = "guillaume@holberton.io"
    PASSWD = "b4l0u"
    NEW_PASSWD = "t4rt1fl3tt3"


    if __name__ == "__main__":

        register_user(EMAIL, PASSWD)
        log_in_wrong_password(EMAIL, NEW_PASSWD)
        profile_unlogged()
        session_id = log_in(EMAIL, PASSWD)
        profile_logged(session_id)
        log_out(session_id)
        reset_token = reset_password_token(EMAIL)
        update_password(EMAIL, reset_token, NEW_PASSWD)
        log_in(EMAIL, NEW_PASSWD)
    ```
  + Run `python3 main.py`. If everything is correct, you should see no output.
