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
async def create_supplier(new_supplier: schemas.NewSupplier, db: Session = Depends(get_db)):
    return crud.create_supplier(db, new_supplier)


# task 5.4
@router.put("/suppliers/{supplier_id}", response_model=schemas.SupplierUpdate, status_code=200)
async def update_supplier(supplier_id: PositiveInt, supplier: schemas.SupplierUpdate, db: Session = Depends(get_db)):
    updated_supplier = crud.update_supplier(db, supplier_id, supplier)
    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    return updated_supplier
