PLACEHOLDERS = {
    "username": "Your username",
    "email": "Your e-mail",
    "first_name": "Ex.: John",
    "last_name": "Ex.: Doe",
    "password": "Type your password",
    "password2": "Repeat your password",
}

EMAIL_HELP_TEXT = "The e-mail must be valid"

COMMON_LENGTH_ERRORS = {
    "min_length": (
        "Ensure this value has at least %(limit_value)d characters "
        "(it has %(show_value)d)."
    ),
    "max_length": (
        "Ensure this value has at most %(limit_value)d characters "
        "(it has %(show_value)d)."
    ),
}

PASSWORD_COMPLEXITY_ERROR = (
    "Password must have at least one uppercase letter, "  # noqa: S105
    "one lowercase letter and one number. The length should be "
    "at least 8 characters."
)
