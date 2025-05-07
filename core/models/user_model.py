from pydantic import EmailStr, Field
from datetime import datetime, date
from typing import Optional
from core.models.base_model import BaseModel as PrjBaseModel  


class VDHUserBase(PrjBaseModel):
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    status: int = 0
    fullname: Optional[str] = None
    birthday: Optional[date] = None
    passport: Optional[str] = None
    role_id: Optional[int] = None
    address: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    forgot_pass_token: Optional[str] = None
    updated_forgot_token: Optional[datetime] = None
    remember_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    kpi_listing_website: Optional[int] = None
    kpi_listing_amz: Optional[int] = None
    kpi_listing_fb: Optional[int] = None
    kpi_listing_etsy: Optional[int] = None
    sheet: Optional[str] = None
    lark_type: Optional[str] = None  # Valid JSON string
    lark_hook_ids: Optional[str] = None  # Valid JSON string
    lark_code: Optional[str] = None
    key_login: Optional[str] = None
    key_login_2: Optional[str] = None
    key_login_3: Optional[str] = None
    key_login_4: Optional[str] = None


class VDHUserCreate(VDHUserBase):
    password: str
    created_by: Optional[int] = None


class VDHUserUpdate(PrjBaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    fullname: Optional[str] = None
    password: Optional[str] = None
    birthday: Optional[date] = None
    passport: Optional[str] = None
    role_id: Optional[int] = None
    address: Optional[str] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    sheet: Optional[str] = None
    lark_type: Optional[str] = None
    lark_hook_ids: Optional[str] = None
    lark_code: Optional[str] = None
    key_login: Optional[str] = None
    key_login_2: Optional[str] = None
    key_login_3: Optional[str] = None
    key_login_4: Optional[str] = None


class VDHUserInDB(VDHUserBase):
    id: int
    password: str
    created_by: Optional[int]

    class Config:
        from_attributes = True  # V2 replacement for orm_mode



class VDHUserOut(VDHUserBase):
    id: int

    class Config:
        from_attributes = True  # V2 replacement for orm_mode

