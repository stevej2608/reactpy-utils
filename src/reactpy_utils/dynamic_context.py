from __future__ import annotations
from typing import TypeVar
from pydantic import BaseModel

DataModel = TypeVar('DataModel', bound='DynamicContextModel')

class DynamicContextModel(BaseModel):
    """Base component for dynamic context models"""

    def update(self: DataModel , **kwargs) -> DataModel:
        model = self.model_copy(update=kwargs)
        return model
