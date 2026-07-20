"""
File: auth.py

Purpose:
Provides cryptographic utility functions for securing user passwords.
It ensures that plain text passwords are never stored in the database.

Dependencies:
- hashlib (For SHA-256 secure hashing)

"""

import hashlib

# Purpose:
# Takes a raw plain-text password and converts it into a secure, irreversible 256-bit hash.
#
# Parameters:
# password (str): The plain-text password typed by the user.
#
# Returns:
# str: The 64-character hexadecimal SHA-256 hash.
def hash_password(password: str) -> str:
    """
    Generates a secure SHA-256 hash of the provided password.

    Args:
        password (str):
            The raw string password to hash.

    Returns:
        str:
            The resulting hexadecimal hash string.
    """
    # We must encode the string to bytes using UTF-8 before the hashing algorithm can process it.
    # We use hexdigest() to get a readable alphanumeric string instead of raw binary bytes.
    return hashlib.sha256(password.encode()).hexdigest()

# Purpose:
# Validates whether a given plain-text password matches a previously hashed password stored in the DB.
#
# Parameters:
# password (str): The password attempt provided by the user during login.
# hashed (str): The known good hash retrieved from the users database table.
#
# Returns:
# bool: True if the passwords match, False otherwise.
def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies a password against a known hash.

    Args:
        password (str):
            The password attempt.
        hashed (str):
            The correct hash from the database.

    Returns:
        bool:
            True if valid, False otherwise.
    """
    # We hash the incoming password attempt using the exact same algorithm.
    # If the resulting hash exactly matches the stored hash, the password is correct.
    # This proves the user knows the password without us ever knowing what it is.
    return hash_password(password) == hashed
