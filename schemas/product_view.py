from common.ma import ma
from models.product_view import ProductViewModel

class ProductViewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductViewModel
        dump_only = ("id", "produc_id", "date_visited")
        include_fk = True
        load_instance = True