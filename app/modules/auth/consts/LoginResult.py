from enum import Enum

class LoginResult(Enum):
    SUCCESS = "success"
    USER_NOT_FOUND = "user_not_found"
    INVALID_PASSWORD = "invalid_password"