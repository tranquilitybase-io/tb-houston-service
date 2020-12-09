from cryptography.fernet import Fernet, InvalidToken


# db hash key
def encrypt(token: bytes, key: bytes) -> bytes:
    try:
        b = Fernet(key).encrypt(token)
        return b
    except InvalidToken as inv:
        print("Default account cannot be deleted!", inv)
        raise RuntimeError


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


class _KEY(object):
    __slots__ = ()
    VAL = Fernet.generate_key()
