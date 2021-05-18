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
    ContactName: constr(max_length=30)
    ContactTitle: constr(max_length=30)
    Address: constr(max_length=60)
    City: constr(max_length=15)
    Region: Optional[constr(max_length=15)]
    PostalCode: constr(max_length=10)
    Country: constr(max_length=15)
    Phone: constr(max_length=24)
    Fax: Optional[constr(max_length=24)] = None
    HomePage: Optional[str] = None

    class Config:
        orm_mode = True