import os
import jwt
import json
import requests
from core import cache
from functools import wraps
from flask import request, abort, g


def login_required(func):
    """
    Decorator to check the validity of the Okta JWT
    JWT are also decoded to get user data which is set in g object
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        JWT_ISSUER = os.environ.get('OKTA_ISSUER')
        authorization = request.headers.get("authorization", None)
        if not authorization:
            abort(403)
        try:
            token = authorization.split(' ')[1]
            key_id = jwt.get_unverified_header(token)['kid']
            jwk = get_jwk(
                JWT_ISSUER, os.environ.get('OKTA_CLIENT_ID'),
                key_id, cache=cache
            )
            token_data = jwt.decode(
                token, jwk, verify=True, issuer=JWT_ISSUER,
                audience=os.environ.get('OKTA_AUDIENCE'), algorithms=['RS256']
            )
            g.user = token_data['sub']
            g.user_id = token_data['uid']
        except Exception as e:
            print(e, "exception occured.", flush=True)
            abort(403)
        return func(*args, **kwargs)
    return wrap


def get_jwk(issuer, client_id, kid, cache=None):
    """
    Gets JWK with key id
    """
    # if cache exists then load from cache
    key = None
    if cache:
        key = cache.get(kid)
    if key is None:
        keys = get_jwks(issuer, client_id)
        for k in keys:
            if cache:
                cache.set(k['kid'], k)
            if k['kid'] == kid:
                key = k
    if key:
        return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
    raise Exception


def get_jwks(issuer, client_id):
    """
    Get JWKs from OpenID Provider
    """
    jwks_uri = os.environ.get('OKTA_JWKS_URI')
    jwks = requests.get(jwks_uri)
    return jwks.json().get('keys')
