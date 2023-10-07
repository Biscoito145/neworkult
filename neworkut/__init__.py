# Primeira coisa que vamos fazer é instalar o Flask no nosso ambiente vortual -> pip install flask
from flask import Flask  # da biblioteca flask, estamos importando a classe Flask, o render_template, uma função, por meio dele que iremos retornar o arquivo html, podemos usar o url_for dentro dos templates, ao inves de no href a gente passar o caminho, a gente vai passar para ele ir pro link que ta na funcao, ou seja, vamos associar o link a funcao del, la no arquivo html vc passa uma variavel: {{url_for('nome_da_funcao'}}, flash serve para exibir mensagem de alerta, como a mensagem de sucesso no login e senha, redirect para redirecionar o usuairo para uma outra pagina
from flask_sqlalchemy import SQLAlchemy # criando nosso banco de dados
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # gerenciador de login do nosso site
import os
# colocando no site no ar (codigo padrão)
app = Flask(__name__)   # Inicializa nosso site


app.config['SECRET_KEY'] = 'dmD4W8ZW644lu7J7FjSnEV0r7zvdkI75'  # importante para segurança do formulário
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # configuração padra para a construção do banco de dados

database = SQLAlchemy(app) # criando uma instância da classe SQLAlchemy
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # aplicando a classe LoginManager dentro no nosso app
login_manager.login_view = 'login' # o cara nao fez o login, clicou numa pagina que precisa estar logado, entao ele a gente redireciona o cara para a pagina de login
login_manager.login_message_category = 'alert-info'# para exibir a mensagem, mas numa caixa azul, lembrando que essas coias de alert-sucsses ou danger ou info é coisa do bootstrap
from neworkut import routes
