import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from common.db import db
from typing import List

class ProductViewModel(db.Model):
    __tablename__ = "product_views"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_visited = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey("products.id"),nullable=False)

    product = db.relationship("ProductModel", back_populates="views")

    def __init__(self, productId: str, **kwargs) -> None:
        super().__init__()
        self.product_id = productId

    @classmethod
    def find_by_id(cls, _id: str) -> "ProductViewModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["ProductViewModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()