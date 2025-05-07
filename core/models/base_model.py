from pydantic import BaseModel as PydanticBaseModel, Field
from datetime import datetime


class BaseModel(PydanticBaseModel):
    id: int | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=datetime.now)
    updated_at: datetime | None = Field(default_factory=datetime.now)
    deleted_at: datetime | None = None  # Only set if soft-deleted

    class Config:
        # from_attributes = True
        orm_mode = True  # Ensures compatibility with SQLAlchemy or row dicts
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
