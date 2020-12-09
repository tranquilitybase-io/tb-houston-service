import logging
from cryptography.fernet import Fernet, InvalidToken


logger = logging.getLogger("tb_houston_service.key_utils")


# db hash key
def encrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(token)


def decrypt(token: bytes, key: bytes) -> bytes:
    try:
        b = Fernet(key).decrypt(token)
        return b
    except InvalidToken as inv:
        logger.error("Default account cannot be deleted!", inv.__traceback__)
        raise RuntimeError


class _KEY(object):
    __slots__ = ()
    VAL = Fernet.generate_key()
