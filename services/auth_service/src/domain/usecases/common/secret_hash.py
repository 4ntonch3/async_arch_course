import hashlib


def hash_secret(secret: str) -> str:
    return hashlib.sha256(bytes(secret, "utf-8")).hexdigest()
