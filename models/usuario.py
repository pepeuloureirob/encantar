from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class Usuario(UserMixin, db.Model):
    """
    Modelo do usuário administrador.
    """

    __tablename__ = "usuarios"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False
    )

    chave_recuperacao = db.Column(
        db.String(120),
        nullable=False
    )

    ativo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def set_senha(self, senha: str):
        """
        Gera o hash da senha.
        """
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha: str) -> bool:
        """
        Verifica se a senha informada está correta.
        """
        return check_password_hash(
            self.senha_hash,
            senha
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }

    def __repr__(self):
        return f"<Usuario {self.email}>"
