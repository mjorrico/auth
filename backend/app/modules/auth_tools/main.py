from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def verify_password(hash_str: str, password: str) -> bool:
    """Checks a plain-text password against a stored hash."""
    try:
        return ph.verify(hash_str, password)
    except VerifyMismatchError:
        return False
    except Exception as e:
        print(f"An error occurred during verification: {e}")
        return False
