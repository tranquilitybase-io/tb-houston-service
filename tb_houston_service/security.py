import time
import connexion
import logging
import os
import six
from werkzeug.exceptions import Unauthorized
from jose import JWTError, jwt

JWT_ISSUER="com.zalando.connexion"
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'

logger = logging.getLogger("security")

def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    logger.debug("decode_token: %s", token)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        logger.debug("payload sub: %s", payload["sub"])
        return payload
    except JWTError as e:
        six.raise_from(Unauthorized, e)

def _current_timestamp() -> int:
    return int(time.time())

if __name__ == "__main__": 
    print(generate_token("karwoo.tang@gft.com"))
