from common.ma import ma
from models.product import ProductModel

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductModel
        load_only = ("id",)
        dump_only = ("id",)
        load_instance = True