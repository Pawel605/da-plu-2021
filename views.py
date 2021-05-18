from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud
import schemas
import models
from database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


# task 5.1
@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierExtended)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


# task 5.2
@router.get("/suppliers/{supplier_id}/products")
async def get_suppliers_products(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")

    db_suppliers_products = crud.get_suppliers_products(db, supplier_id)
    return [{
        "ProductID": product.ProductID,
        "ProductName": product.ProductName,
        "Category": {
            "CategoryID": product.CategoryID,
            "CategoryName": product.CategoryName,
        },
        "Discontinued": product.Discontinued,
    } for product in db_suppliers_products]


# task 5.3
@router.post("/suppliers", response_model=schemas.SupplierExtended, status_code=201)
async def add_supplier(add_supplier: schemas.SupplierExtended, db: Session = Depends(get_db)):
    supplier = models.Supplier()
    supplier.CompanyName = add_supplier.CompanyName
    supplier.ContactName = add_supplier.ContactName
    supplier.ContactTitle = add_supplier.ContactTitle
    supplier.Address = add_supplier.Address
    supplier.City = add_supplier.City
    supplier.PostalCode = add_supplier.PostalCode
    supplier.Country = add_supplier.Country
    supplier.Phone = add_supplier.Phone
    supplier.Fax = add_supplier.Fax
    supplier.HomePage = add_supplier.HomePage

    crud.add_supplier(db, supplier)
    return crud.get_supplier(db, supplier.SupplierID)
