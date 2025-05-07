from ..exceptions.status_code import STATUS_DESCRIPTIONS


class StandardException(Exception):
    """Standard exception class for API errors with proper HTTP status formatting.

    Attributes:
        type: The error type identifier
        title: A human-readable title for the error
        status: The HTTP status code
        detail: A detailed explanation of the error
    """

    def __init__(self, type: str, title: str, status: int, detail: str):
        self.type = type
        self.title = title
        self.status = status
        self.detail = detail
        # Call the parent class constructor with the detail message
        super().__init__(f"{title}: {detail}")


class ErrorCode:
    """Class providing standardized error responses."""

    @classmethod
    def create_exception(cls, status_code, error_type=None, title=None, detail=None):
        """Helper method to create a StandardException with consistent format.

        Args:
            status_code: HTTP status code for the error
            error_type: Optional error type identifier
            title: Optional human-readable title
            detail: Optional detailed explanation

        Returns:
            StandardException: A properly formatted exception
        """
        if not detail:
            detail = STATUS_DESCRIPTIONS.get(status_code, f"Error with status code {status_code}")

        if not title:
            title = f"Error {status_code}"

        return StandardException(
            type=error_type,
            status=status_code,
            title=title,
            detail=detail
        )