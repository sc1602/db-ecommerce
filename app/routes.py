from flask_restful import Api
from app import app
from app.resources.role_resource import RoleResource
from app.resources.auth_resource import RegisterResource, LoginResource
from app.resources.category_resource import CategoryResource
from app.resources.product_resource import (
    ProductResource,
    ProductManageResource
)
from app.resources.sale_resource import (
    SaleResource,
    DownloadInvoiceResource
)

api = Api(app, prefix='/api')

api.add_resource(RoleResource, '/roles')
api.add_resource(RegisterResource, '/auth/register')
api.add_resource(LoginResource, '/auth/login')

api.add_resource(CategoryResource, '/categories')
api.add_resource(ProductResource, '/products')
api.add_resource(ProductManageResource, '/products/<int:product_id>')

api.add_resource(SaleResource, '/sales')
api.add_resource(DownloadInvoiceResource, '/sales/<int:sale_id>/pdf')