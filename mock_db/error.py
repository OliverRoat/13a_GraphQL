from pydantic import BaseModel

class ErrorMessage(Exception):
    def __init__(self, message: str, error_code: int):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseError(ErrorMessage):
    def __init__(self, message, error_code):
        super().__init__(message, error_code)
        
class SuccessMessage(BaseModel):
    message: str
    