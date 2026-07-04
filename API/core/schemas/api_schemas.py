from pydantic import BaseModel
from typing import Any

class ApiResponse(BaseModel):
    data: Any