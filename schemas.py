from pydantic import BaseModel
from typing import Any, Dict, List, Union

class GenericResponse(BaseModel):
    data: Union[List[Any], Dict[str, Any]]
    meta: Dict[str, Any]
