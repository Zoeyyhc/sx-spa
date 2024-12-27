from flask_pydantic import validate
from flask_restx import Namespace, Resource
from app.order.schema import (
    OrderCreateSchema,
    OrderListSchema,
    OrderPaymentSchema,
    OrderSchema,
)
from app.order.service import order_service
from app.user import permission_required
api = Namespace("orders")
@api.route("")
class OrdersApi(Resource):
    @permission_required("order_admin")
    def get(self):
        orders = order_service().list_orders()
        return OrderListSchema.from_orm(orders)
    
    @permission_required("order_admin")
    @validate()
    def post(self, body: OrderCreateSchema):
        order_id = str(order_service().place_order(body).id)
        return order_id, 201
    
@api.route("/<string:order_id>")
class OrderApi(Resource):
    @permission_required("order_admin")
    def get(self, order_id):
        order = order_service().get_order(order_id)
        return OrderSchema.from_orm(order)
    
    @permission_required("order_admin")
    def delete(self, order_id):
        return order_service().delete_order(order_id)
    
@api.route("/<string:order_id>/payment")
class OrderPaymentApi(Resource):
    @permission_required("order_admin")
    @validate()
    def put(self, order_id, body: OrderPaymentSchema):
        return order_service().pay_order(order_id, body)