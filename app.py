import os
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

####################################################
# CONFIGURAÇÃO
####################################################

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

app.config["SECRET_KEY"] = "encantar_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(BASE_DIR, "encantar.db")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)

####################################################
# LOGIN
####################################################

login_manager = LoginManager()

login_manager.login_view = "login"

login_manager.init_app(app)

####################################################
# MODELOS
####################################################

class Usuario(UserMixin, db.Model):

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
        nullable=False
    )

    senha = db.Column(
        db.String(255),
        nullable=False
    )


class Evento(db.Model):

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

    data = db.Column(
        db.String(30),
        nullable=False
    )

    imagem = db.Column(
        db.String(255)
    )

    drive = db.Column(
        db.String(500)
    )

    criado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Feedback(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    estrelas = db.Column(
        db.Integer,
        nullable=False
    )

    comentario = db.Column(
        db.Text,
        nullable=False
    )

    aprovado = db.Column(
        db.Boolean,
        default=False
    )

####################################################
# LOGIN
####################################################

@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(
        int(user_id)
    )

####################################################
# BANCO
####################################################

with app.app_context():

    db.create_all()

    admin = Usuario.query.filter_by(
        email="admin@encantar.com"
    ).first()

    if admin is None:

        admin = Usuario(
            nome="Administrador",
            email="admin@encantar.com",
            senha=generate_password_hash(
                "admin123"
            )
        )

        db.session.add(admin)

        db.session.commit()

####################################################
# AUXILIARES
####################################################

def salvar_imagem(arquivo):

    if arquivo is None:

        return None

    if arquivo.filename == "":

        return None

    nome = secure_filename(
        arquivo.filename
    )

    caminho = os.path.join(
        app.config["UPLOAD_FOLDER"],
        nome
    )

    arquivo.save(caminho)

    return nome

####################################################
# ROTAS PÚBLICAS
####################################################

@app.route("/")
def index():

    eventos = Evento.query.order_by(
        Evento.criado_em.desc()
    ).all()

    feedbacks = Feedback.query.filter_by(
        aprovado=True
    ).all()

    return render_template(
        "index.html",
        eventos=eventos,
        feedbacks=feedbacks
    )
  ####################################################
# ROTAS PÚBLICAS
####################################################

@app.route("/sobre")
def sobre():

    return render_template("sobre.html")


@app.route("/servicos")
def servicos():

    return render_template("servicos.html")


@app.route("/eventos")
def eventos():

    lista_eventos = Evento.query.order_by(
        Evento.data.desc()
    ).all()

    return render_template(
        "eventos.html",
        eventos=lista_eventos
    )


@app.route("/feedback")
def feedback():

    feedbacks = Feedback.query.filter_by(
        aprovado=True
    ).order_by(
        Feedback.id.desc()
    ).all()

    return render_template(
        "feedback.html",
        feedbacks=feedbacks
    )


####################################################
# ENVIAR FEEDBACK
####################################################

@app.route(
    "/enviar-feedback",
    methods=["POST"]
)
def enviar_feedback():

    nome = request.form.get("nome")

    comentario = request.form.get(
        "comentario"
    )

    estrelas = int(
        request.form.get("estrelas")
    )

    novo = Feedback(
        nome=nome,
        comentario=comentario,
        estrelas=estrelas,
        aprovado=False
    )

    db.session.add(novo)

    db.session.commit()

    flash(
        "Feedback enviado com sucesso! Aguarde aprovação.",
        "success"
    )

    return redirect(
        url_for("feedback")
    )


####################################################
# LOGIN
####################################################

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        senha = request.form.get(
            "senha"
        )

        usuario = Usuario.query.filter_by(
            email=email
        ).first()

        if (
            usuario
            and check_password_hash(
                usuario.senha,
                senha
            )
        ):

            login_user(usuario)

            flash(
                "Login realizado com sucesso!",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Email ou senha inválidos.",
            "danger"
        )

    return render_template(
        "login.html"
    )


####################################################
# LOGOUT
####################################################

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sessão encerrada.",
        "info"
    )

    return redirect(
        url_for("index")
    )


####################################################
# DASHBOARD
####################################################

@app.route("/admin")
@login_required
def dashboard():

    total_eventos = Evento.query.count()

    feedbacks_pendentes = Feedback.query.filter_by(
        aprovado=False
    ).count()

    feedbacks_aprovados = Feedback.query.filter_by(
        aprovado=True
    ).count()

    return render_template(
        "dashboard.html",
        total_eventos=total_eventos,
        feedbacks_pendentes=feedbacks_pendentes,
        feedbacks_aprovados=feedbacks_aprovados
    )
  ####################################################
# CADASTRAR EVENTO
####################################################

@app.route(
    "/admin/eventos/novo",
    methods=["GET", "POST"]
)
@login_required
def novo_evento():

    if request.method == "POST":

        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        data = request.form.get("data")
        drive = request.form.get("drive")

        imagem = salvar_imagem(
            request.files.get("imagem")
        )

        evento = Evento(
            nome=nome,
            descricao=descricao,
            data=data,
            imagem=imagem,
            drive=drive
        )

        db.session.add(evento)
        db.session.commit()

        flash(
            "Evento cadastrado com sucesso!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "novo_evento.html"
    )


####################################################
# EDITAR EVENTO
####################################################

@app.route(
    "/admin/eventos/<int:id>/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_evento(id):

    evento = Evento.query.get_or_404(id)

    if request.method == "POST":

        evento.nome = request.form.get("nome")
        evento.descricao = request.form.get("descricao")
        evento.data = request.form.get("data")
        evento.drive = request.form.get("drive")

        imagem = request.files.get("imagem")

        if imagem and imagem.filename != "":

            nome_imagem = salvar_imagem(imagem)

            if nome_imagem:
                evento.imagem = nome_imagem

        db.session.commit()

        flash(
            "Evento atualizado com sucesso!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "editar_evento.html",
        evento=evento
    )


####################################################
# EXCLUIR EVENTO
####################################################

@app.route(
    "/admin/eventos/<int:id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_evento(id):

    evento = Evento.query.get_or_404(id)

    if evento.imagem:

        caminho = os.path.join(
            app.config["UPLOAD_FOLDER"],
            evento.imagem
        )

        if os.path.exists(caminho):
            os.remove(caminho)

    db.session.delete(evento)
    db.session.commit()

    flash(
        "Evento excluído com sucesso!",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


####################################################
# APROVAR FEEDBACK
####################################################

@app.route(
    "/admin/feedback/<int:id>/aprovar",
    methods=["POST"]
)
@login_required
def aprovar_feedback(id):

    feedback = Feedback.query.get_or_404(id)

    feedback.aprovado = True

    db.session.commit()

    flash(
        "Feedback aprovado!",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


####################################################
# EXCLUIR FEEDBACK
####################################################

@app.route(
    "/admin/feedback/<int:id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_feedback(id):

    feedback = Feedback.query.get_or_404(id)

    db.session.delete(feedback)

    db.session.commit()

    flash(
        "Feedback excluído.",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )
  ####################################################
# TRATAMENTO DE ERROS
####################################################

@app.errorhandler(404)
def pagina_nao_encontrada(error):

    return (
        render_template("404.html"),
        404
    )


@app.errorhandler(500)
def erro_interno(error):

    db.session.rollback()

    return (
        render_template("500.html"),
        500
    )


####################################################
# PAINEL - LISTA DE EVENTOS
####################################################

@app.route("/admin/eventos")
@login_required
def admin_eventos():

    eventos = Evento.query.order_by(
        Evento.criado_em.desc()
    ).all()

    return render_template(
        "admin_eventos.html",
        eventos=eventos
    )


####################################################
# PAINEL - LISTA DE FEEDBACKS
####################################################

@app.route("/admin/feedbacks")
@login_required
def admin_feedbacks():

    feedbacks = Feedback.query.order_by(
        Feedback.id.desc()
    ).all()

    return render_template(
        "admin_feedbacks.html",
        feedbacks=feedbacks
    )


####################################################
# CONTEXTO GLOBAL
####################################################

@app.context_processor
def variaveis_globais():

    return {
        "usuario": current_user
    }


####################################################
# EXECUÇÃO DA APLICAÇÃO
####################################################

if __name__ == "__main__":

    porta = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=porta,
        debug=True
    )
