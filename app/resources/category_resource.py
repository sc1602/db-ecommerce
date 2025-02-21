from flask import request
from flask_restful import Resource
from app.schemas.category_schema import (
    CreateCategorySchema,
    CategorySchema
)
from app.models.category_model import CategoryModel
from db import db
from pydantic import ValidationError
from flask_jwt_extended import jwt_required

class CategoryResource(Resource):
    @jwt_required()
    def get(self):
        try:
            categories = CategoryModel.query.all()

            response_data = []
            for category in categories:
                response_data.append(
                    CategorySchema(
                        id=category.id,
                        name=category.name,
                        status=category.status,
                        created_at=str(category.created_at),
                        updated_at=str(category.updated_at)
                    ).model_dump()
                )

            return response_data, 200
        except Exception as e:
            return {
                'message': 'Unexpected error',
            }, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validated_data = CreateCategorySchema(**data)
            category = CategoryModel(
                name=validated_data.name
            )
            db.session.add(category)
            db.session.commit()

            response_data = CategorySchema(
                id=category.id,
                name=category.name,
                status=category.status,
                created_at=str(category.created_at),
                updated_at=str(category.updated_at)
            )
            return response_data.model_dump(), 200
        except ValidationError as e:
            return {
                'message': e.errors()
            }, 400
        except Exception as e:
            return {
                'message': 'Unexpected error',
            }, 500