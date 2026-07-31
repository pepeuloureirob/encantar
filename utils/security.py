
from functools import wraps

from flask import (
    flash,
    redirect,
    url_for,
    abort
)

from flask_login import (
    current_user
)


def admin_required(func):
    """
    Decorador para proteger rotas administrativas.

    Exige que o usuário esteja autenticado.
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):

        if not current_user.is_authenticated:
            flash(
                "Faça login para acessar esta página.",
                "warning"
            )

            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return decorated_function


def apenas_post():
    """
    Função auxiliar para impedir acesso indevido
    por métodos GET.
    """

    abort(405)


def validar_avaliacao(valor):
    """
    Garante que a avaliação esteja entre 1 e 5.
    """

    try:
        valor = int(valor)
    except (TypeError, ValueError):
        return False

    return 1 <= valor <= 5


def limpar_texto(texto):
    """
    Remove espaços excedentes.
    """

    if texto is None:
        return ""

    return str(texto).strip()


def validar_whatsapp(numero):
    """
    Mantém apenas os números do telefone.
    """

    numeros = "".join(filter(str.isdigit, str(numero)))

    if len(numeros) < 10:
        return None

    return numeros


def validar_url(url):
    """
    Validação simples para URLs.
    """

    if not url:
        return False

    return (
        url.startswith("http://")
        or url.startswith("https://")
    )
