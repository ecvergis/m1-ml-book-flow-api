from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from m1_ml_book_flow_api.core.database import Base

class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    category = Column(String, nullable=True, index=True)
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    available = Column(Boolean, default=True)
    image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

