from sqlalchemy import(
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)  # Optional per doc
    sale_date_time = Column(String, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    sub_total = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    sale_items = relationship("SaleItem", back_populates="sale")
    payment = relationship("Payment", back_populates="sale", uselist=False)
    receipt = relationship("Receipt", back_populates="sale", uselist=False)
