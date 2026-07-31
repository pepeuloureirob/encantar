from datetime import datetime

from extensions import db


class Visita(db.Model):
    """
    Armazena estatísticas simples de acesso ao site.
    A aplicação utilizará apenas um registro (ID = 1),
    incrementando o contador sempre que uma nova visita
    for registrada.
    """

    __tablename__ = "visitas"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    ultima_visita = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
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

    def registrar_visita(self):
        """
        Incrementa o contador de visitas e atualiza a data
        da última visita.
        """
        self.quantidade += 1
        self.ultima_visita = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "quantidade": self.quantidade,
            "ultima_visita": (
                self.ultima_visita.isoformat()
                if self.ultima_visita
                else None
            ),
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat(),
        }

    def __repr__(self):
        return (
            f"<Visita total={self.quantidade}>"
        )
