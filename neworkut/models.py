# o que o banco de dados vai armazenar, a estrutua do banco de dados será construida aqui
from neworkut import database, login_manager #como reestruturamos o projeto a forma de importar muda,from main import database # precisa disso para funcionar, é o cara que usa o SQLAlchemy
# Vamos ter uma tabela de Usuario e caada coluna é uma informação do usuario, como id, nome etc
from datetime import datetime # vai permitir colocarmos a data da criação do post
from flask_login import UserMixin # sera um parametro que vamos passar para a nossa clase e que vai atribuir a essa classe todas as características que o login_manager precisa para gerencian o login

@login_manager.user_loader # temos que dizer para o login_maager que essa é a função de encontrar usuario, entao basicamente diz que aquela é a função que carrega um usuario
def load_usuario(id_usuario): # funçao que vai encontrar um usuario existente no nosso banco de dados
    return Usuario.query.get(int(id_usuario)) # ao inves de usarmos um filter by, podemos usar direto um get, porque o metodo get é uma funcao que encontra um item da sua tabela de acordo com a primary key dela e como definimos que essa key seria o id, podemos usar esse método, o int é apenas uma garantia

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) # no pareenteses vc passa o tipo de coluna que que vai ser, se é de texto, numero, etc. Integer para dizer que é um número inteiro. primary_key=True) -> chave primarioa, cada usuario tera um id diferente, esse valor vai ser o que identfica o usuario como unico. Quando definimos essa chave, automaticament o banco vai preenhcer
    username = database.Column(database.String, nullable=False) # String para dizer que é um texto, nullable=False indica que o campo deve ser preenchido
    email = database.Column(database.String, nullable=False, unique=True) #  unique=True indica que não pode haver dois usuarios ou mais com o mesmo email, ou seja, o email é unico para cada usuario
    senha = database.Column(database.String, nullable=False) # vamos criptografar a senha para que nao seja fique a mostra no banco de dados
    foto_perfil = database.Column(database.String, default='default.jpg')  # vamos armazenar o nome do arquivo da foto do usuário, vamos definir um valor padrão -> se a pessoa não preencher a foto de perfil vamoos colocar essse padrão, tipo quando uma pessoa não tem foto de perfil em uma rede social
    posts = database.relationship('Post', backref='autor', lazy=True)  # relacao usuraio pode ter vários posts, não será uma coluna do nosso banco de dados, mas apenas fará essa relação, como parâmetros vc deve passar qual a tabela que está relacionada com ela, depois no parametro backref vc deve dizer como vai ser o nome de Usuários dentro da tabela de Post (isso é importante se quisermos pegar a informação do usuario que fez o post ex (post = Post() ai eu faco post.autor), já o lazy=True é que quando vc escrever post.autor ele ja vai dar todas as informações do autor, agora na Tabela do Post a gente tem que criar a coluna do autor, geralmente para isso usamos o id do usuario. Em suma, é como se fosse uma lista de posts, que na verdade diz que essa tabela pode receber várias informações que vem de outra tabela, e o backref diz qual vai ser o nome dessa coluna na outra tabela, depois la no Post, criamos um id_usuario que  vai ser a chave estrangeira que vai fazer a relação com a informação do usuario, que é o id (unico para cada usuario)
    cursos = database.Column(database.String, nullable=False, default='Não Informado') # como  to dizendo que ela não poide ser vazia e na area de login não tem uma opção para a pessoa escolher quais cursos ela ta, a gente passa esse default, e nao vamos criar uma relação pois so queremos exibir os cursos que a pessoa fez/faz

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)  #-> um é o id da classe Usuario e o outro é o id da classe Post
    titulo = database.Column(database.String, nullable=False)
    corpo =database.Column(database.Text, nullable=False) # quando são textos pequenos, definimos como String, quando não sao pequenos como no caso do corpo (pessoa pode escrever um texto), e por isso usamos o Text
    data_criacao = database.Column(database.DateTime,nullable=False, default=datetime.utcnow) # armaena uma data e hora, vamos definir um valor padrão também, precisamos que a data seja preenchida automaticamente quando criar um post, entao vamos importar a biblioteca datetime, no banco de dados é interessante armazenar a data e hora em formato utc, pois padroniza, ja que cada regiao tem um fuso diferente. A gente ta passando datetime.utcnow e nao datetime.utcnow(), o que estamos passando nada mais é do que a função que calcula a data e hora de agr, pois se colocassemos com o parenteses ele ia calcular a data da construção do post, passando dessa maneira garantimos que quando o usuario for criar o post, a função será chamada automáticamente
    id_usuario = database.Column(database.Integer,database.ForeignKey('usuario.id'), nullable=False,) #temos que colocar aqui uma informação que seja unica para cada usuario e que olhando a tabela de Post vc consiga identificar quem é esse usuário, database.ForeignKey('') -> chave estrangeira, dentro dela vvc passa um texto com o nome da classe e o atributo que vc quer pegar (usuario.id), classe Usuario, id da classe usuario (tem que passar a classe com letra minuscula). Ess chave estrangeira basicamente diz que a informação que ta no id_usuario é a chave que me diz quem é  o usuário, que é único
    # alem disso vamos criar uma relação entre essas duas classes,  ja que falta ainda a informação acerca de quem é dono do post
    # Cada usuario pode ter vários posts, então na tabela de Usuarios eu vou criar uma relação que pode puxar vários posts diferentes, é o que chamamos de uma relação de um para muitos, ou seja, cada usuário pode ter vários posts e ai vc cria essa relação dentro da tabela de Usuários
