import jwt, datetime, os

def create_jwt(username, secret):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz=datetime.timezone.utc),
        },
        secret,
        algorithm="HS256"
    ).decode('utf-8')

def decode_jwt(encoded_jwt, secret):
    try:
        return jwt.decode(encoded_jwt, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None