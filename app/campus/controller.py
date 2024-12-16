from flask_restx import Namespace, Resource
from flask import jsonify
from .model import Campus
from .schema import CampusSchema, CampusListSchema  

api: Namespace = Namespace("campus")

@api.route("")
# class CampusListApi(Resource):
#     def get(self) -> list[Campus]:
#         campus_list = [campus for campus in Campus.objects()]
#         campus_schemas = [CampusSchema.model_validate(campus) for campus in campus_list]
#         return CampusListSchema(campus_schemas).model_dump()

class CampusListApi(Resource):
    def get(self):
        campus_list = [campus for campus in Campus.objects()]
        campus_schemas = [CampusSchema.model_validate(campus) for campus in campus_list]
        campus_list_schema = CampusListSchema(root=campus_schemas)
        return jsonify(campus_list_schema)