from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    """
    Product base schema
    """
    dn: Optional[str] = None
    s_am_account_name: Optional[str] = None
    user_principal_name: Optional[str] = None
    mail: Optional[str] = None
    given_name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    title: Optional[str] = None
    script_path: Optional[str] = None

    class Config:
        fields = {
            "title": {"description": "Product name"},
            "description": {"description": "Product description"},
            "purch_price": {"description": "Purchase price of the product"},
            "sales_price": {"description": "Sales price of the product"}
        }


class UserCreate(UserBase):
    """
    User create schema
    """
    dn: str
    s_am_account_name: str
    user_principal_name: str
    mail: str
    given_name: str
    display_name: str
    description: str
    postal_code: str
    country: str
    company: str
    department: str
    title: str
    script_path: str


class UserPartialUpdate(UserBase):
    """
    User update schema
    """
    ...
