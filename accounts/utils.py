import hashlib
import hmac
import time
from urllib.parse import parse_qsl


def verify_telegram_auth(init_data: str, bot_token: str):
    data = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_to_check = data.pop('hash', None)
    auth_data = sorted([f"{k}={v}" for k, v in data.items()])
    data_check_string = '\n'.join(auth_data)
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_hash, hash_to_check)
