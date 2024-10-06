"""Credential Utils"""

import secrets


def generate_credentials():
    """Generating Credentials"""
    username = f"user_{secrets.token_hex(4)}"
    password = secrets.token_hex(8)
    return username, password
