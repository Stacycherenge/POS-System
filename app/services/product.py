from sqlalchemy.orm import Session
from repositories.product import product_repository
from fastapi import HTTPException, status
from schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, id: str):
    product = product_repository.get(db, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    return product


def list_products(db: Session):
    return product_repository.get_all(db)


def create_product(db: Session, data: ProductCreate):
    return product_repository.create(db, data.model_dump())


def update_product(db: Session, product_id: str, data: ProductUpdate):
    product = get_product(db, product_id)
    return product_repository.update(db, product, data.model_dump(exclude_unset=True))


def delete_product(db: Session, product_id: str):
    product = product_repository.get(db, product_id)
    return product_repository.delete(db, product)
