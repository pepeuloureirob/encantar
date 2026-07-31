from datetime import datetime

from extensions import db


class Configuracao(db.Model):
    """
    Configurações gerais do site.
    Deve existir apenas um registro, que poderá ser editado
    pelo painel administrativo.
    """

    __tablename__ = "configuracoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Informações do cerimonial
    nome_empresa = db.Column(
        db.String(150),
        nullable=False,
        default="Encantar Cerimonial"
    )

    slogan = db.Column(
        db.String(255),
        nullable=True
    )

    # Página inicial
    texto_principal = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    subtitulo_principal = db.Column(
        db.Text,
        nullable=True
    )

    # Sobre nós
    texto_sobre = db.Column(
        db.Text,
        nullable=False,
        default=""
    )

    # Contatos
    whatsapp = db.Column(
        db.String(20),
        nullable=False,
        default="5583999999999"
    )

    telefone = db.Column(
        db.String(20),
        nullable=True
    )

    email = db.Column(
        db.String(150),
        nullable=True
    )

    endereco = db.Column(
        db.String(255),
        nullable=True
    )

    instagram = db.Column(
        db.String(255),
        nullable=False,
        default="https://instagram.com/"
    )

    facebook = db.Column(
        db.String(255),
        nullable=True
    )

    # Identidade visual
    logo = db.Column(
        db.String(255),
        nullable=True,
        default="logo.png"
    )

    imagem_principal = db.Column(
        db.String(255),
        nullable=True,
        default="capa_principal.jpg"
    )

    imagem_sobre = db.Column(
        db.String(255),
        nullable=True,
        default="sobre.jpg"
    )

    # Mensagem usada no orçamento via WhatsApp
    mensagem_orcamento = db.Column(
        db.Text,
        nullable=True,
        default="Olá! Gostaria de solicitar um orçamento."
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
            "nome_empresa": self.nome_empresa,
            "slogan": self.slogan,
            "texto_principal": self.texto_principal,
            "subtitulo_principal": self.subtitulo_principal,
            "texto_sobre": self.texto_sobre,
            "whatsapp": self.whatsapp,
            "telefone": self.telefone,
            "email": self.email,
            "endereco": self.endereco,
            "instagram": self.instagram,
            "facebook": self.facebook,
            "logo": self.logo,
            "imagem_principal": self.imagem_principal,
            "imagem_sobre": self.imagem_sobre,
            "mensagem_orcamento": self.mensagem_orcamento,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }

    def __repr__(self):
        return f"<Configuracao {self.nome_empresa}>"
