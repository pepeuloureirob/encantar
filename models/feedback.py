
from datetime import datetime

from extensions import db


class Feedback(db.Model):
    """
    Modelo responsável pelos feedbacks enviados pelos clientes.
    Somente os feedbacks aprovados serão exibidos no site.
    """

    __tablename__ = "feedbacks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    comentario = db.Column(
        db.Text,
        nullable=False
    )

    avaliacao = db.Column(
        db.Integer,
        nullable=False
    )

    aprovado = db.Column(
        db.Boolean,
        default=False,
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

    __table_args__ = (
        db.CheckConstraint(
            "avaliacao >= 1 AND avaliacao <= 5",
            name="check_avaliacao"
        ),
    )

    @property
    def estrelas(self):
        """
        Retorna uma lista para facilitar a renderização
        das estrelas no template.
        """
        return list(range(self.avaliacao))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "comentario": self.comentario,
            "avaliacao": self.avaliacao,
            "aprovado": self.aprovado,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }

    def __repr__(self):
        return (
            f"<Feedback "
            f"{self.nome} "
            f"{self.avaliacao}★>"
        )
