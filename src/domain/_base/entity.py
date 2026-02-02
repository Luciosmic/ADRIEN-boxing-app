from typing import Any
from pydantic import BaseModel, Field, ConfigDict

class Entity(BaseModel):
    """
    Base class for Entities.
    Entities are defined by their identity, not their attributes.
    """
    # In Pydantic, fields are defined as class attributes.
    # We use PrivateAttr if we want to hide it, but usually ID is public.
    # However, Entity equality is strictly ID based.
    
    # We assume 'id' is passed in constructor or set.
    # To allow flexible types for ID (UUID, int, str), we don't strictly type it here 
    # OR we use a Generic. For simplicity in seed: Any or specific type? 
    # Let's map it to Any for generic usage, but recommended UUID.
    
    id: Any 

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id and isinstance(other, type(self))

    def __hash__(self):
        return hash(self.id)
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    def to_dict(self) -> dict:
        try:
            return self.model_dump()
        except AttributeError:
            return self.dict()




