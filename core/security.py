import bcrypt

def hash_password(password: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve un hash seguro.
    """
    pw = password.encode("utf-8")
    hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """
    Verifica si la contraseña coincide con el hash almacenado.
    Retorna True si es correcta, False si no.
    """
    pw = password.encode("utf-8")
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(pw, hashed_bytes)
