from sqlalchemy.orm import Session
from app.repositories.sale import sale_repository
from fastapi import HTTPException, status
from app.schemas.sale import SaleCreate, SaleUpdate


def get_sale(db: Session, id: str):
    sale = sale_repository.get(db, id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale Not Found")
    return sale


def list_sales(db: Session):
    return sale_repository.get_all(db)


def create_sale(db: Session, data: SaleCreate):
    return sale_repository.create(db, data.model_dump())


def update_sale(db: Session, sale_id: str, data: SaleUpdate):
    sale = get_sale(db, sale_id)
    return sale_repository.update(db, sale, data.model_dump(exclude_unset=True))


def delete_sale(db: Session, sale_id: str):
    sale = sale_repository.get(db, sale_id)
    return sale_repository.delete(db, sale)
