import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import List
from common.db import db
from models.product_view import ProductViewModel

class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    views = db.relationship("ProductViewModel", cascade="all, delete-orphan", back_populates="product")

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_sku(cls, _sku: str) -> "ProductModel":
        return cls.query.filter_by(sku=_sku).first()
    
    @classmethod
    def find_all(cls) -> List["ProductModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()