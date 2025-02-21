from app.models.user_model import UserModel
from flask_restful import Resource
from flask import request
from app.schemas.auth_schema import (
    RegisterSchema,
    UserSchema,
    LoginSchema
)
from pydantic import ValidationError
from app.utils.passwords import (
    hash_password,
    verify_password
)
from db import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from cryptography.fernet import Fernet
import os

class RegisterResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            validated_data = RegisterSchema(**data)

            existing_user = UserModel.query.filter_by(email=validated_data.email).first()

            if existing_user:
                return {
                    'message': 'User already exists'
                }, 400

            user = UserModel(
                name=validated_data.name,
                last_name=validated_data.last_name,
                email=validated_data.email,
                password=hash_password(validated_data.password),
                role_id=validated_data.role_id
            )
            db.session.add(user)
            db.session.commit()

            response_data = UserSchema(
                id=user.id,
                name=user.name,
                last_name=user.last_name,
                email=user.email,
                status=user.status,
                created_at=str(user.created_at),
                updated_at=str(user.updated_at),
                role_id=user.role_id
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

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            validated_data = LoginSchema(**data)

            existing_user = UserModel.query.filter_by(email=validated_data.email).first()

            if not existing_user:
                return {
                    'message': 'Email or password incorrect',
                }, 401
            
            pwd_valid = verify_password(
                validated_data.password,
                existing_user.password
            )

            if not pwd_valid:
                return {
                    'message': 'Email or password incorrect',
                }, 401
            
            key = os.environ.get('FERNET_SECRET_KEY').encode('utf-8')
            fernet = Fernet(key)
            user_id_bytes = str(existing_user.id).encode('utf-8')
            hashed_user_id = fernet.encrypt(user_id_bytes)

            access_token = create_access_token(
                identity=hashed_user_id.decode('utf-8'),
                additional_claims={
                    'name': existing_user.name,
                    'email': existing_user.email
                }
            )
            refresh_token = create_refresh_token(identity=hashed_user_id.decode('utf-8'))

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        except Exception as e:
            print(e)
            return {
                'message': 'Unexpected error',
            }, 500