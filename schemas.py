from pydantic import BaseModel, PositiveInt, constr
from typing import Optional


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class SupplierExtended(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)] = None
    HomePage: Optional[str] = None


class Config:
        orm_mode = True


class NewSupplier(BaseModel):
    SupplierID: int = 0
    CompanyName: Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]

    class Config:
        orm_mode = True

