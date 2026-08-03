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

class SaleItem(Base):
    __tablename__ = "sale_items"

    sale_item_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    price_at_sale = Column(Numeric(10, 2), nullable=False)

    sale = relationship("Sale", back_populates="sale_items")
    product = relationship("Product", back_populates="sale_items")
