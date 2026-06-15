from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    disabled: bool

    model_config = {"from_attributes": True}


class DocumentBase(BaseModel):
    telegram_file_id: str
    original_filename: str
    mime_type: str = "application/pdf"
    google_drive_file_id: str
    google_drive_link: Optional[str] = None
    summary_text: Optional[str] = None
    summary_status: str = "pending"
    notes: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    uploaded_at: datetime

    model_config = {"from_attributes": True}


class FinanceMovementBase(BaseModel):
    type: str = Field(pattern=r"^(income|expense)$")
    amount: Decimal = Field(gt=0, decimal_places=2)
    movement_date: date
    description: str
    origin: str = "telegram_manual"


class FinanceMovementCreate(FinanceMovementBase):
    pass


class FinanceMovementResponse(FinanceMovementBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
