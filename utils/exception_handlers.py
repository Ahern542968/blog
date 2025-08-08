from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel

T = TypeVar("T")

class APIResponse(GenericModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

    @staticmethod
    def success(data: Optional[T] = None, message: str = "OK"):
        return APIResponse(code=0, message=message, data=data)

    @staticmethod
    def fail(code: int, message: str):
        return APIResponse(code=code, message=message, data=None)
