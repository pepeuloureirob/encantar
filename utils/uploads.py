
import os
import secrets

from flask import current_app
from werkzeug.utils import secure_filename


def arquivo_permitido(nome_arquivo):
    """
    Verifica se a extensão do arquivo é permitida.
    """
    if "." not in nome_arquivo:
        return False

    extensao = nome_arquivo.rsplit(".", 1)[1].lower()

    return extensao in current_app.config["ALLOWED_EXTENSIONS"]


def salvar_imagem(arquivo, pasta="eventos"):
    """
    Salva uma imagem na pasta de uploads.

    Retorna o nome do arquivo salvo ou None.
    """

    if arquivo is None:
        return None

    if arquivo.filename == "":
        return None

    if not arquivo_permitido(arquivo.filename):
        return None

    nome_original = secure_filename(arquivo.filename)

    extensao = nome_original.rsplit(".", 1)[1].lower()

    novo_nome = f"{secrets.token_hex(16)}.{extensao}"

    destino = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        pasta
    )

    os.makedirs(destino, exist_ok=True)

    caminho = os.path.join(destino, novo_nome)

    arquivo.save(caminho)

    return f"{pasta}/{novo_nome}"


def excluir_imagem(caminho_relativo):
    """
    Remove uma imagem do diretório de uploads.
    """

    if not caminho_relativo:
        return

    caminho = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        caminho_relativo
    )

    if os.path.exists(caminho):
        os.remove(caminho)
