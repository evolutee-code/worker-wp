from datetime import datetime
from enum import Enum

from bson import ObjectId
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

from ..exceptions.exceptions import ErrorCode
from ..exceptions.status_code import HTTP_400_BAD_REQUEST
from ..validators.validate import Validator


def check_object_id(value: str) -> str:
    """Validate that a string is a valid MongoDB ObjectId.

    Args:
        value: The string to validate

    Returns:
        The validated string

    Raises:
        StandardException: If the string is not a valid ObjectId
    """
    # Add more specific error message
    if not value or not isinstance(value, str):
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail="Invalid ObjectId: value must be a non-empty string"
        )

    if not ObjectId.is_valid(value):
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail=f"Invalid ObjectId format: '{value}' is not a valid 24-character hex string"
        )
    return value


def check_email(value: str) -> str:
    """Validate that a string is a valid email address.

    Args:
        value: The string to validate

    Returns:
        The validated and normalized email string

    Raises:
        StandardException: If the string is not a valid email
    """
    if not value or not isinstance(value, str):
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail="Invalid email: value must be a non-empty string"
        )

    value = value.strip().lower()
    if not Validator.check_email(value):
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail=f"Invalid email format: '{value}' is not a valid email address"
        )
    return value


def check_date_format(value: str) -> str:
    """Validate that a string is in YYYY-MM-DD format.

    Args:
        value: The string to validate

    Returns:
        The validated date string

    Raises:
        StandardException: If the string is not in the correct format
    """
    if not value or not isinstance(value, str):
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail="Invalid date: value must be a non-empty string"
        )

    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise ErrorCode.create_exception(
            HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: '{value}' must be in YYYY-MM-DD format"
        )


# Define annotated types for use in models
ObjectIdStr = Annotated[str, AfterValidator(check_object_id)]
EmailStr = Annotated[str, AfterValidator(check_email)]
DateStr = Annotated[str, AfterValidator(check_date_format)]
