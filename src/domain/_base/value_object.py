from pydantic import BaseModel, ConfigDict

class ValueObject(BaseModel):
    """
    Base class for Value Objects.
    Value Objects are defined by their attributes and are immutable.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    
    def to_dict(self) -> dict:
        try:
            return self.model_dump()
        except AttributeError:
            return self.dict()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


