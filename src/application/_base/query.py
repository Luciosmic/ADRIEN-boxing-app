from typing import Optional
from pydantic import BaseModel, ConfigDict

class Query(BaseModel):
    """
    Base class for Queries.
    Queries represent a request for information.
    """
    model_config = ConfigDict(frozen=True)
    pass
