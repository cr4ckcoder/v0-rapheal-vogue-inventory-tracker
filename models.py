from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Auth Models
class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Product Models
class ProductCreate(BaseModel):
    ean: str
    style_name: str
    size: str
    brand: str
    style_design_code: Optional[str] = None
    model_no: Optional[str] = None

class ProductResponse(ProductCreate):
    pass

# Inventory Models
class InventoryResponse(BaseModel):
    inventory_id: int
    product_ean: str
    store_id: int
    quantity: int

# Transaction Models
class TransactionResponse(BaseModel):
    transaction_id: int
    product_ean: str
    store_id: int
    quantity_change: int
    transaction_type: str
    timestamp: str

# Bulk Upload Models
class ImportRow(BaseModel):
    ean: str
    style_name: str
    size: str
    brand: str
    style_design_code: Optional[str] = None
    model_no: Optional[str] = None
    store_id: int
    quantity: int

class TransferRow(BaseModel):
    ean: str
    source_store_id: int
    destination_store_id: int
    quantity: int

class SalesRow(BaseModel):
    ean: str
    store_id: int
    quantity_sold: int

# Response Models
class UploadSummary(BaseModel):
    success_count: int
    error_count: int
    errors: List[dict]
    status: str

class StockStatusResponse(BaseModel):
    ean: str
    style_name: str
    brand: str
    stores: dict  # {store_id: quantity}
    total_quantity: int

class AnalyticsResponse(BaseModel):
    most_moving: List[dict]
    least_moving: List[dict]
