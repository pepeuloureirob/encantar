import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    """
    Configurações gerais da aplicação
    """

    # Chave secreta
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        secrets.token_hex(32)
    )

    # Banco SQLite
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(INSTANCE_DIR, "encantar.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pasta de uploads
    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    # Limite máximo dos uploads (8 MB)
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    # Extensões permitidas
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "webp"
    }

    # Cookies seguros
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

    # Em produção (HTTPS), altere para True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
