from datetime import datetime

from pydantic import EmailStr, Field
from typing import Optional
from core.models.base_model import BaseModel as PrjBaseModel


class VDHStoreBase(PrjBaseModel):
    """Base model for VDH stores"""
    name: Optional[str] = None
    domain: Optional[str] = None
    api_key: Optional[str] = None
    secret_key: Optional[str] = None
    sub_title: Optional[str] = None
    status: Optional[int] = None
    db_host: Optional[str] = None
    db_port: Optional[str] = Field(default="3306")
    db_database: Optional[str] = None
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    setting_listing: Optional[str] = None
    listing: Optional[int] = Field(description="1 - list")
    user_listing: Optional[int] = None
    user_id: Optional[int] = None
    group_assigned: Optional[int] = None
    user_assigned: Optional[int] = None
    status_database: Optional[int] = None
    status_active: Optional[int] = None
    status_listing: Optional[int] = None
    username_login: Optional[str] = None
    password_login: Optional[str] = None
    research_group_assigned: Optional[int] = None


class VDHStoreCreate(VDHStoreBase):
    """Model for creating a new store"""
    pass


class VDHStoreUpdate(VDHStoreBase):
    """Model for updating an existing store"""
    pass


class VDHStoreInDB(VDHStoreBase):
    """Model representing a store as stored in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # V2 replacement for orm_mode
