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
from database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, unique=True)
    receipt_number = Column(String, nullable=False, unique=True)
    issued_date_time = Column(String, nullable=False)

    sale = relationship("Sale", back_populates="receipt")
