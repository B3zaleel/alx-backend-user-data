# Personal Data

This project contains tasks for learning to protect a user's personal data.

## Tasks To Complete

+ [x] 0. **Regex-ing**<br/>[filtered_logger.py](filtered_logger.py) contains a function called `filter_datum` that returns the log message obfuscated with the following requirements:
  + Arguments:
    + `fields`: a list of strings representing all fields to obfuscate.
    + `redaction`: a string representing by what the field will be obfuscated.
    + `message`: a string representing the log line.
    + `separator`: a string representing by which character is separating all fields in the log line (`message`).
  + The function should use a regex to replace occurrences of certain field values.
  + `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

+ [x] 1. **Log formatter**<br/>[filtered_logger.py](filtered_logger.py) contains the following updates:
  + Copy the following code into [filtered_logger.py](filtered_logger.py).
    ```python
    import logging


    class RedactingFormatter(logging.Formatter):
        """ Redacting Formatter class
        """

        REDACTION = "***"
        FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
        SEPARATOR = ";"

        def __init__(self):
            super(RedactingFormatter, self).__init__(self.FORMAT)

        def format(self, record: logging.LogRecord) -> str:
            raise NotImplementedError
    ```
  + Update the class to accept a list of strings `fields` constructor argument.
  + Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.
  + DO NOT extrapolate `FORMAT` manually. The `format` method should be less than 5 lines long.

+ [x] 2. **Create logger**<br/>[filtered_logger.py](filtered_logger.py) contains
  + Use [user_data.csv](user_data.csv) for this task.
  + Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.
  + The logger should be named `"user_data"` and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.
  + Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from [user_data.csv](user_data.csv) that are considered PII. `PII_FIELDS` can contain only 5 fields - choose the right list of fields that can are considered as “important” PIIs or information that you **must hide** in your logs. Use it to parameterize the formatter.

+ [x] 3. **Connect to secure database**<br/>[filtered_logger.py](filtered_logger.py) contains the following updates:
  + **INFO**:Database credentials should **NEVER** be stored in code or checked into version control. One secure option is to store them as environment variable on the application server.
  + In this task, you will connect to a secure `holberton` database to read a `users` table. The database is protected by a username and password that are set as environment variables on the server named as follows:
    + `PERSONAL_DATA_DB_USERNAME` (set the default as “root”).
    + `PERSONAL_DATA_DB_PASSWORD` (set the default as an empty string).
    + `PERSONAL_DATA_DB_HOST` (set the default as “localhost”).
  + The database name is stored in `PERSONAL_DATA_DB_NAME`.
  + Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).
    + Use the `os` module to obtain credentials from the environment.
    + Use the module `mysql-connector-python` to connect to the MySQL database (`pip3 install mysql-connector-python`).

+ [x] 4. **Read and filter data**<br/>[filtered_logger.py](filtered_logger.py) contains a `main` function that takes no arguments and returns nothing with the following requirements:
  + The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table and display each row under a filtered format like this:
    ```log
    [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);
    ```
  + Filtered fields:
    + name
    + email
    + phone
    + ssn
    + password
  + Only your `main` function should run when the module is executed.

+ [x] 5. **Encrypting passwords**<br/>[encrypt_password.py](encrypt_password.py) contains a script that meets the following requirements:
  + **INFO**: User *passwords* should **NEVER** be stored in *plain text* in a database.
  + Implement a `hash_password` function that expects one string argument name password and returns a salted, hashed password, which is a byte string.
  + Use the `bcrypt` package to perform the hashing (with `hashpw`).

+ [x] 6. **Check valid password**<br/>[app.py](app.py) contains an `is_valid` function that expects 2 arguments and returns a boolean:
  + Arguments:
    + `hashed_password`: `bytes` type.
    + `password`: `str` type.
  + Use bcrypt to validate that the provided password matches the hashed password.
