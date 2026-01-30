"""
Módulo para manejo de contraseñas
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt
    bcrypt tiene un límite de 72 bytes
    """
    # Convertir a bytes y hashear
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Retornar como string
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña coincida con el hash
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
