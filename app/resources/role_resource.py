from flask import request
from app.models.role_model import RoleModel
from flask_restful import Resource
from app.schemas.role_schema import CreateRoleSchema, RoleSchema
from pydantic import ValidationError
from db import db

class RoleResource(Resource):
    def get(self):
        try:
            roles = RoleModel.query.all()

            response_data = []
            for role in roles:
                response_data.append(
                    RoleSchema(
                        id=role.id,
                        name=role.name,
                        status=role.status
                    ).model_dump()
                )

            return response_data, 200
        except Exception as e:
            return {
                'message': 'Unexpected error',
            }, 500

    def post(self):
        try:
            data = request.get_json()
            validated_data = CreateRoleSchema(**data)
            role = RoleModel(
                name=validated_data.name
            )
            db.session.add(role)
            db.session.commit()

            response_data = RoleSchema(
                id=role.id,
                name=role.name,
                status=role.status
            )

            return response_data.model_dump(), 200
        except ValidationError as e:
            return {
                'message': e.errors()
            }, 400
        except Exception as e:
            db.session.rollback()
            return {
                'message': 'Unexpected error',
            }, 500