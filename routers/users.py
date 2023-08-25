import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List

from orm import DatabaseManagerBase
from dependencies import get_db
from utilities.exceptions import EntityNotFoundException, ApiException
import schemas
from domain.user_model import UserCreate, UserPartialUpdate
from service.active_directory import ActiveDirectoryManager




router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=201,)
async def add_user(new_user_request: UserCreate):
    """
    Create a user:

    - **title**: Title of the product
    - **description**: Description of the product
    - **purch_price**: The purch price of the product
    - **sales_price**: The sales price of the product
    """
    server = os.environ.get('AD_SERVER')
    username = os.environ.get('AD_USERNAME')
    password = os.environ.get('AD_PASSWORD')

    ad_manager = ActiveDirectoryManager(server, username, password)
    ad_manager.connect()
    try:
        ad_manager.add_new_user(new_user_request)
        return {"message": "User added successfully"}
    except HTTPException as e:
        raise e


@router.put("/", status_code=204)
async def modify_user(dn: str, extension_attributes: UserPartialUpdate):
    server = os.environ.get('AD_SERVER')
    username = os.environ.get('AD_USERNAME')
    password = os.environ.get('AD_PASSWORD')

    ad_manager = ActiveDirectoryManager(server, username, password)
    ad_manager.connect()
    try:
        ad_manager.modify_user_attributes(dn, extension_attributes)
        return {"message": "User attributes modified successfully"}
    except HTTPException as e:
        raise e


# @router.post("/", response_model=schemas.Product, summary="Creates a product")
# async def add_product(product_create: schemas.ProductCreate, db: DatabaseManagerBase = Depends(get_db)):
#     """
#     Create a product:

#     - **title**: Title of the product
#     - **description**: Description of the product
#     - **purch_price**: The purch price of the product
#     - **sales_price**: The sales price of the product
#     """
#     logging.debug("Products: Add product")
#     product = db.add_product(product_create)
#     return product


# @router.get(
#     "/",
#     response_model=Optional[List[schemas.Product]],
#     summary="Retrieves all prodcuts",
#     description="Retrieves all available products from the API")
# async def read_products(db: DatabaseManagerBase = Depends(get_db)):
#     logging.debug("Product: Fetch products")
#     products = db.get_products()
#     return products


# @router.get(
#     "/{product_id}",
#     response_model=Optional[schemas.Product],
#     summary="Retrieve a product by ID",
#     description="Retrieves a specific product by ID, if no product matches the filter criteria a 404 error is returned")
# async def read_product(product_id: int, db: DatabaseManagerBase = Depends(get_db)):
#     logging.debug("Prouct: Fetch product by id")
#     product = db.get_product(product_id)
#     if not product:
#         raise EntityNotFoundException(code="Unable to retrieve product",
#                                       description=f"Product with the id {product_id} does not exist")
#     return product


# @router.patch("/{product_id}", response_model=schemas.Product, summary="Patches a product")
# async def update_product(product_id: int, product_update: schemas.ProductPartialUpdate, db: DatabaseManagerBase = Depends(get_db)):
#     """ 
#     Patches a product, this endpoint allows to update single or multiple values of a product

#     - **title**: Title of the product
#     - **description**: Description of the product
#     - **purch_price**: The purch price of the product
#     - **sales_price**: The sales price of the product
#     """
#     logging.debug("Product: Update product")

#     if len(product_update.dict(exclude_unset=True).keys()) == 0:
#         raise ApiException(status_code=400, code="Invalid request",
#                            description="Please specify at least one property!")

#     product = db.update_product(product_id, product_update)
#     if not product:
#         raise EntityNotFoundException(
#             code="Unable to update product", description=f"Product with the id {product_id} does not exist")
#     return product


# @router.delete("/{product_id}", summary="Deletes a product", description="Deletes a product permanently by ID")
# async def delete_product(product_id: int, db: DatabaseManagerBase = Depends(get_db)):
#     logging.debug("Product: Delete product")
#     db.delete_product(product_id)