from sqlalchemy.orm import Session
from app.repositories.payment import payment_repository
from fastapi import HTTPException, status
from app.schemas.payment import PaymentCreate, PaymentUpdate


def get_payment(db: Session, id: str):
    payment = payment_repository.get(db, id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Payment Not Found")
    return payment


def list_payments(db: Session):
    return payment_repository.get_all(db)


def create_payment(db: Session, data: PaymentCreate):
    return payment_repository.create(db, data.model_dump())


def update_payment(db: Session, payment_id: str, data: PaymentUpdate):
    payment = get_payment(db, payment_id)
    return payment_repository.update(db, payment, data.model_dump(exclude_unset=True))


def delete_payment(db: Session, payment_id: str):
    payment = payment_repository.get(db, payment_id)
    return payment_repository.delete(db, payment)
