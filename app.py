import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename



# =====================================
# CONFIGURAÇÃO DO APP
# =====================================


app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "encantar-chave-secreta"
)



app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///encantar.db"
)


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False



app.config["UPLOAD_FOLDER"] = (
    "static/uploads"
)


app.config["IMG_FOLDER"] = (
    "static/img"
)



db = SQLAlchemy(app)





# =====================================
# MODELOS DO BANCO
# =====================================



class Usuario(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    email = db.Column(
        db.String(120),
        unique=True
    )


    senha = db.Column(
        db.String(255)
    )





class Evento(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    nome = db.Column(
        db.String(150)
    )


    data = db.Column(
        db.String(50)
    )


    descricao = db.Column(
        db.Text
    )


    drive = db.Column(
        db.String(500)
    )


    imagem = db.Column(
        db.String(255)
    )





class Feedback(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    nome = db.Column(
        db.String(100)
    )


    estrelas = db.Column(
        db.Integer
    )


    comentario = db.Column(
        db.Text
    )


    aprovado = db.Column(
        db.Boolean,
        default=False
    )





class Configuracao(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    whatsapp = db.Column(
        db.String(30),
        default="5583999999999"
    )


    instagram = db.Column(
        db.String(300)
    )


    texto_inicio = db.Column(
        db.Text
    )





class ImagemSite(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    logo = db.Column(
        db.String(255),
        default="logo.png"
    )


    capa = db.Column(
        db.String(255),
        default="capa.jpg"
    )


    sobre = db.Column(
        db.String(255),
        default="sobre.jpg"
    )




# =====================================
# CRIAÇÃO DO BANCO E CONFIGURAÇÕES INICIAIS
# =====================================


with app.app_context():


    db.create_all()



    # Criar administrador padrão

    usuario = Usuario.query.first()


    if usuario is None:


        usuario = Usuario(

            email="admin@encantar.com",

            senha=generate_password_hash(
                "admin123"
            )

        )


        db.session.add(usuario)



    # Criar configurações padrão

    config = Configuracao.query.first()



    if config is None:


        config = Configuracao(

            whatsapp="5583988293316",

            instagram="https://instagram.com/encantarcerimonial",

            texto_inicio=(
                "Transformando sonhos em "
                "momentos inesquecíveis."
            )

        )


        db.session.add(config)




    # Criar imagens padrão

    imagens = ImagemSite.query.first()



    if imagens is None:


        imagens = ImagemSite(

            logo="logo.png",

            capa="capa.jpg",

            sobre="sobre.jpg"

        )


        db.session.add(imagens)



    db.session.commit()







# =====================================
# CONTEXTOS GLOBAIS
# =====================================


@app.context_processor

def dados_globais():


    config = Configuracao.query.first()


    imagens = ImagemSite.query.first()



    return {


        "config": config,


        "imagens": imagens


    }









# =====================================
# FUNÇÕES AUXILIARES
# =====================================



def usuario_logado():


    return (
        "usuario"
        in session
    )







def salvar_upload(
        arquivo,
        pasta,
        nome_padrao
):

    if not arquivo:
        return None


    if arquivo.filename == "":
        return None



    os.makedirs(
        pasta,
        exist_ok=True
    )


    nome = secure_filename(
        arquivo.filename
    )


    extensao = nome.rsplit(".", 1)[-1]


    novo_nome = (
        nome_padrao
        +
        "."
        +
        extensao
    )



    caminho = os.path.join(
        pasta,
        novo_nome
    )



    arquivo.save(caminho)



    return novo_nome


    if not arquivo:

        return None



    if arquivo.filename == "":

        return None




    nome = secure_filename(
        arquivo.filename
    )



    extensao = nome.split(".")[-1]



    novo_nome = (
        nome_padrao
        +
        "."
        +
        extensao
    )



    caminho = os.path.join(

        pasta,

        novo_nome

    )



    arquivo.save(caminho)



    return novo_nome







def salvar_imagem_site(
        arquivo,
        nome
):


    return salvar_upload(

        arquivo,

        app.config["IMG_FOLDER"],

        nome

    )







def login_required(func):


    def wrapper(*args, **kwargs):


        if not usuario_logado():


            return redirect(
                url_for("login")
            )


        return func(
            *args,
            **kwargs
        )



    wrapper.__name__ = func.__name__


    return wrapper




# =====================================
# ROTAS PÚBLICAS
# =====================================



@app.route("/")
def index():


    eventos = Evento.query.order_by(
        Evento.id.desc()
    ).all()



    return render_template(

        "index.html",

        eventos=eventos

    )






@app.route("/sobre")
def sobre():


    return render_template(

        "sobre.html"

    )






@app.route("/servicos")
def servicos():


    return render_template(

        "servicos.html"

    )







@app.route("/eventos")
def eventos():


    lista_eventos = Evento.query.all()



    return render_template(

        "eventos.html",

        eventos=lista_eventos

    )








@app.route(
    "/feedback",
    methods=["GET","POST"]
)

def feedback():


    if request.method == "POST":


        novo = Feedback(

            nome=request.form["nome"],

            estrelas=int(
                request.form["estrelas"]
            ),

            comentario=request.form["comentario"],

            aprovado=False

        )


        db.session.add(novo)

        db.session.commit()



        flash(

            "Obrigado pelo seu feedback!",

            "success"

        )



        return redirect(

            url_for("feedback")

        )





    feedbacks = Feedback.query.filter_by(

        aprovado=True

    ).all()



    return render_template(

        "feedback.html",

        feedbacks=feedbacks

    )







# =====================================
# LOGIN ADMINISTRATIVO
# =====================================



@app.route(

    "/login",

    methods=["GET","POST"]

)

def login():


    if request.method == "POST":



        email = request.form["email"]


        senha = request.form["senha"]



        usuario = Usuario.query.filter_by(

            email=email

        ).first()



        if usuario and check_password_hash(

            usuario.senha,

            senha

        ):


            session["usuario"] = usuario.id



            return redirect(

                url_for("dashboard")

            )



        flash(

            "Login inválido",

            "danger"

        )



    return render_template(

        "login.html"

    )







@app.route("/logout")

def logout():


    session.clear()



    return redirect(

        url_for("index")

    )








# =====================================
# DASHBOARD
# =====================================



@app.route("/dashboard")

@login_required

def dashboard():


    total_eventos = Evento.query.count()



    pendentes = Feedback.query.filter_by(

        aprovado=False

    ).count()



    aprovados = Feedback.query.filter_by(

        aprovado=True

    ).count()



    ultimo = Evento.query.order_by(

        Evento.id.desc()

    ).first()



    return render_template(

        "dashboard.html",

        total_eventos=total_eventos,

        feedbacks_pendentes=pendentes,

        feedbacks_aprovados=aprovados,

        ultimo_evento=ultimo

    )






# =====================================
# CADASTRAR EVENTO
# =====================================



@app.route(

    "/admin/evento/novo",

    methods=["GET","POST"]

)

@login_required

def novo_evento():



    if request.method == "POST":



        imagem = request.files.get(

            "imagem"

        )



        nome_imagem = salvar_upload(

            imagem,

            app.config["UPLOAD_FOLDER"],

            "evento_" + request.form["nome"]

        )



        evento = Evento(


            nome=request.form["nome"],


            data=request.form["data"],


            descricao=request.form["descricao"],


            drive=request.form["drive"],


            imagem=nome_imagem


        )



        db.session.add(evento)


        db.session.commit()



        flash(

            "Evento cadastrado!",

            "success"

        )



        return redirect(

            url_for("admin_eventos")

        )



    return render_template(

        "novo_evento.html"

    )







# =====================================
# LISTAR EVENTOS ADMIN
# =====================================



@app.route("/admin/eventos")

@login_required

def admin_eventos():


    eventos = Evento.query.all()



    return render_template(

        "admin_eventos.html",

        eventos=eventos

    )


# =====================================
# EDITAR EVENTO
# =====================================


@app.route(

    "/admin/evento/editar/<int:id>",

    methods=["GET","POST"]

)

@login_required

def editar_evento(id):


    evento = Evento.query.get_or_404(id)



    if request.method == "POST":



        evento.nome = request.form["nome"]


        evento.data = request.form["data"]


        evento.descricao = request.form["descricao"]


        evento.drive = request.form["drive"]



        imagem = request.files.get("imagem")



        if imagem:


            evento.imagem = salvar_upload(

                imagem,

                app.config["UPLOAD_FOLDER"],

                "evento_" + str(id)

            )



        db.session.commit()



        flash(

            "Evento atualizado!",

            "success"

        )


        return redirect(

            url_for("admin_eventos")

        )



    return render_template(

        "editar_evento.html",

        evento=evento

    )







# =====================================
# EXCLUIR EVENTO
# =====================================


@app.route(

    "/admin/evento/excluir/<int:id>",

    methods=["POST"]

)

@login_required

def excluir_evento(id):


    evento = Evento.query.get_or_404(id)



    db.session.delete(evento)


    db.session.commit()



    flash(

        "Evento excluído!",

        "success"

    )



    return redirect(

        url_for("admin_eventos")

    )







# =====================================
# ADMIN FEEDBACKS
# =====================================



@app.route("/admin/feedbacks")

@login_required

def admin_feedbacks():


    feedbacks = Feedback.query.all()



    return render_template(

        "admin_feedbacks.html",

        feedbacks=feedbacks

    )






@app.route(

    "/admin/feedback/aprovar/<int:id>",

    methods=["POST"]

)

@login_required

def aprovar_feedback(id):


    feedback = Feedback.query.get_or_404(id)



    feedback.aprovado = True



    db.session.commit()



    return redirect(

        url_for("admin_feedbacks")

    )







@app.route(

    "/admin/feedback/excluir/<int:id>",

    methods=["POST"]

)

@login_required

def excluir_feedback(id):


    feedback = Feedback.query.get_or_404(id)



    db.session.delete(feedback)



    db.session.commit()



    return redirect(

        url_for("admin_feedbacks")

    )







# =====================================
# CONFIGURAÇÕES DO SITE
# =====================================



@app.route(

    "/admin/configuracoes",

    methods=["GET","POST"]

)

@login_required

def configuracoes():


    config = Configuracao.query.first()



    if request.method == "POST":


        config.whatsapp = request.form["whatsapp"]


        config.instagram = request.form["instagram"]


        config.texto_inicio = request.form["texto_inicio"]



        db.session.commit()



        flash(

            "Configurações alteradas!",

            "success"

        )


        return redirect(

            url_for("configuracoes")

        )




    return render_template(

        "configuracoes.html",

        config=config

    )








# =====================================
# GERENCIADOR DE IMAGENS
# =====================================



@app.route(

    "/admin/imagens",

    methods=["GET","POST"]

)

@login_required

def gerenciar_imagens():


    imagens = ImagemSite.query.first()



    if request.method == "POST":



        logo = request.files.get("logo")


        capa = request.files.get("capa")


        sobre = request.files.get("sobre")



        if logo:


            imagens.logo = salvar_imagem_site(

                logo,

                "logo"

            )



        if capa:


            imagens.capa = salvar_imagem_site(

                capa,

                "capa"

            )



        if sobre:


            imagens.sobre = salvar_imagem_site(

                sobre,

                "sobre"

            )



        db.session.commit()



        flash(

            "Imagens atualizadas!",

            "success"

        )


        return redirect(

            url_for("gerenciar_imagens")

        )




    return render_template(

        "imagens.html",

        imagens=imagens

    )







# =====================================
# ERROS
# =====================================



@app.errorhandler(404)

def pagina_nao_encontrada(e):


    return render_template(

        "404.html"

    ),404






@app.errorhandler(500)

def erro_servidor(e):


    return render_template(

        "500.html"

    ),500







# =====================================
# INICIAR SERVIDOR
# =====================================
print(app.url_map)


if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=int(

            os.environ.get(

                "PORT",

                5000

            )

        )

    )
