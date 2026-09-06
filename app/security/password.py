from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Computes a secure cryptographic hash from a plain-text password.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The generated password hash string.
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a stored password hash.

    Args:
        password (str): The plain-text password candidate to verify.
        hashed_password (str): The stored cryptographic hash string.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return password_hash.verify(password, hashed_password)
