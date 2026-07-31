from datetime import datetime

from extensions import db


class Servico(db.Model):
    """
    Modelo responsável pelos serviços oferecidos pelo Encantar Cerimonial.
    """

    __tablename__ = "servicos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False,
        unique=True
    )

    descricao = db.Column(
        db.Text,
        nullable=False
    )

    imagem = db.Column(
        db.String(255),
        nullable=True
    )

    ordem = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    atualizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "imagem": self.imagem,
            "ordem": self.ordem,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }

    def __repr__(self):
        return f"<Servico {self.titulo}>"
