from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instância do banco de dados
db = SQLAlchemy()

# Gerenciador de login
login_manager = LoginManager()

# Página para onde o usuário será redirecionado caso não esteja autenticado
login_manager.login_view = "login"

# Mensagem exibida ao tentar acessar uma rota protegida
login_manager.login_message = "Faça login para continuar."

# Categoria da mensagem
login_manager.login_message_category = "warning"
