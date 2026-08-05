import hashlib
import secrets


def create_token(user_id: str, emp_id: int) -> str:
    payload = f"{user_id}:{emp_id}:{secrets.token_hex(8)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
