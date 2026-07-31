from datetime import datetime

from extensions import db
from models.usuario import Usuario
from models.configuracao import Configuracao
from models.visita import Visita


def formatar_data(data):
    """
    Retorna uma data no formato brasileiro.
    """
    if data is None:
        return ""

    return data.strftime("%d/%m/%Y")


def criar_configuracao_padrao():
    """
    Cria o registro padrão das configurações do sistema,
    caso ainda não exista.
    """
    configuracao = Configuracao.query.first()

    if configuracao:
        return configuracao

    configuracao = Configuracao(
        nome_empresa="Encantar Cerimonial",
        slogan="Transformando sonhos em momentos inesquecíveis.",
        texto_principal=(
            "Bem-vindo ao Encantar Cerimonial. "
            "Somos especialistas em transformar sonhos "
            "em eventos memoráveis."
        ),
        texto_sobre=(
            "Nossa equipe atua com dedicação, organização "
            "e atenção aos detalhes para tornar cada evento "
            "único."
        ),
        whatsapp="5583999999999",
        instagram="https://instagram.com/encantarcerimonial",
        mensagem_orcamento=(
            "Olá! Gostaria de solicitar um orçamento."
        )
    )

    db.session.add(configuracao)
    db.session.commit()

    return configuracao


def criar_admin_padrao():
    """
    Cria o administrador padrão apenas na primeira execução.
    """

    admin = Usuario.query.filter_by(
        email="admin@encantar.com"
    ).first()

    if admin:
        return admin

    admin = Usuario(
        nome="Administrador",
        email="admin@encantar.com",
        chave_recuperacao="ENCANTAR2026"
    )

    admin.set_senha("admin123")

    db.session.add(admin)
    db.session.commit()

    return admin


def inicializar_visitas():
    """
    Garante que exista um registro para o contador de visitas.
    """

    visita = Visita.query.first()

    if visita:
        return visita

    visita = Visita(
        quantidade=0,
        ultima_visita=datetime.utcnow()
    )

    db.session.add(visita)
    db.session.commit()

    return visita


def registrar_visita():
    """
    Incrementa o contador de visitas.
    """

    visita = Visita.query.first()

    if visita is None:
        visita = inicializar_visitas()

    visita.registrar_visita()

    db.session.commit()

    return visita


def inicializar_sistema():
    """
    Inicializa o banco de dados e cria os registros básicos.
    """

    db.create_all()

    criar_configuracao_padrao()
    criar_admin_padrao()
    inicializar_visitas()
