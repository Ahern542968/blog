from fastapi import HTTPException, status


class FlictException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT)


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN)
