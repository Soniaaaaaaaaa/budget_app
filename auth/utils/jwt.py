import jwt, datetime, os

def create_jwt(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
            "admin": is_admin,
        },
        secret,
        algorithm="HS256"
    )

def decode_jwt(encoded_jwt, secret):
    try:
        return jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None