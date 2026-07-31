
from datetime import datetime

from extensions import db


class Evento(db.Model):
    """
    Modelo responsável pelos eventos realizados pelo cerimonial.
    """

    __tablename__ = "eventos"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(200),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=False
    )

    data_evento = db.Column(
        db.Date,
        nullable=False,
        index=True
    )

    imagem_capa = db.Column(
        db.String(255),
        nullable=True
    )

    link_google_drive = db.Column(
        db.String(500),
        nullable=False
    )

    destaque = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    publicado = db.Column(
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

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "data_evento": self.data_evento.strftime("%d/%m/%Y"),
            "imagem_capa": self.imagem_capa,
            "link_google_drive": self.link_google_drive,
            "destaque": self.destaque,
            "publicado": self.publicado,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }

    @property
    def data_formatada(self):
        return self.data_evento.strftime("%d/%m/%Y")

    def __repr__(self):
        return f"<Evento {self.nome}>"
