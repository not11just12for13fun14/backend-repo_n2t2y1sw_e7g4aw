"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List

# Example schemas (you can still use these elsewhere if needed):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Candle business specific schemas
class Candle(BaseModel):
    """
    Candle products
    Collection name: "candle"
    """
    name: str = Field(..., description="Candle name")
    scent: str = Field(..., description="Fragrance blend")
    description: Optional[str] = Field(None, description="Marketing description")
    price: float = Field(..., ge=0, description="Price in USD")
    size_oz: float = Field(..., gt=0, description="Size in ounces")
    burn_time_hours: Optional[int] = Field(None, ge=0, description="Estimated burn time in hours")
    image_urls: List[HttpUrl] = Field(default_factory=list, description="Image gallery URLs")
    in_stock: bool = Field(True, description="Inventory availability")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating 0-5")

class Inquiry(BaseModel):
    """Contact form submissions
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., min_length=10, max_length=2000, description="Message body")

class Subscriber(BaseModel):
    """Newsletter subscribers
    Collection name: "subscriber"
    """
    email: EmailStr = Field(..., description="Subscriber email")
    source: Optional[str] = Field(None, description="Where subscription was made")
