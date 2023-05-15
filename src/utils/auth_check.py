from functools import wraps
from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from src.core.config import settings


def decorator(*args, request: Request, **kwargs):
    token = request.headers.get('Authorization', None)
    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Authorization token needed'
        )
    token = token.replace('Bearer', '')


def decode_jwt(jwt_token: str):
    try:
        decoded = jwt.decode(
            jwt_token, settings.token_secret_key, algorithms="HS256"
        )
    except InvalidSignatureError:
        return (
            jsonify(msg="Signature verification failed"),
            HTTPStatus.UNAUTHORIZED,
        )

    except ExpiredSignatureError:
        return jsonify(msg="Signature has expired"), HTTPStatus.UNAUTHORIZED

    if verify_type:
        if refresh and decoded.get("type") == "access":
            return (
                jsonify(msg="Need refresh token, but got access token"),
                HTTPStatus.UNAUTHORIZED,
            )
        if not refresh and decoded.get("type") == "refresh":
            return (
                jsonify(msg="Need access token, but got refresh token"),
                HTTPStatus.UNAUTHORIZED,
            )

    return decoded