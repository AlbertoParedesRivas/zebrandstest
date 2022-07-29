from typing import Dict
from marshmallow import pre_load
from common.ma import ma
from models.admin import AdminModel
from common.util import hash_password

class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdminModel
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True

    @pre_load
    def _pre_load(self, data: Dict, **kwargs):
        data["password"] = hash_password(data["password"])
        return data