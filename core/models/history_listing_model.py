from typing import Optional
from pydantic import Field
from datetime import datetime
from core.models.base_model import BaseModel as PrjBaseModel


class VDHHistoryListingBase(PrjBaseModel):
    """Base model for VDH history listing"""
    store_id: Optional[int] = None
    product_image: Optional[int] = None
    price_regular: Optional[str] = None
    price_sale: Optional[str] = None
    link: Optional[str] = None
    sku: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = Field(default=1, description="1-pending, 2-success, 3-error")
    created_by: Optional[int] = None
    note: Optional[str] = None
    time_run: Optional[datetime] = None
    time_diff: Optional[str] = None
    is_clicked_submit: int = Field(default=0)
    product_wp_id: Optional[int] = None


class VDHHistoryListingCreate(VDHHistoryListingBase):
    """Model for creating a new history listing"""
    pass


class VDHHistoryListingUpdate(VDHHistoryListingBase):
    """Model for updating an existing history listing"""
    pass


class VDHHistoryListingInDB(VDHHistoryListingBase):
    """Model representing a history listing as stored in database"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # V2 replacement for orm_mode
