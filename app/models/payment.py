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

class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, unique=True)
    payment_method = Column(String, nullable=False)  
    amount_paid = Column(Numeric(10, 2), nullable=False)

   
    sale = relationship("Sale", back_populates="payment")
