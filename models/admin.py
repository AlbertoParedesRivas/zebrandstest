from email.policy import default
import uuid
from sqlalchemy.dialects.postgresql import UUID
from common.db import db
from typing import List

class AdminModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    @classmethod
    def find_by_email(cls, email: str) -> "AdminModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: str) -> "AdminModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["AdminModel"]:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()