from flask_wtf import FlaskForm # FlaskForm é o formulario web, ao inves de criar toda logica e só precisamos criar classe do formulário que queremos construir, uma classe para cada formulário
from flask_wtf.file import FileField, FileAllowed # FileField é um campo de arquivo, quando  a pessoa clica abre aquele popup para ela selecionar o a arquivo, já o FileAllowed é um validador, e nele vamos escolher quais são as extensões de arquivos que serão permitidas
from wtforms import StringField,PasswordField,SubmitField, BooleanField,TextAreaField # sao os tipos de campo que nosso formulario pode ter, Text Are Field para textos mais longos
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # vaalidators vai fazer validação dos ccampos do nosso formulário, se preecnheu o campo, se escreveu um e-mail, DataRequired diz que o preenchimento de um campo é obrigatório, o Lengh diz que um campo deve conter um número mínimo de caracteres, Email para ver se é válido ou não e o EqualTo para ver se um campo é igual ao outro, importante no confirmação de senha para passar esses caras vc usa o parametro validators e coloca o que vc quer numa lista, para validação do email faça um pip install email_validator, ValidationError para exibir uma mensagem de erro na nossa função
from neworkut.models import Usuario # para criar a nossa validação se o email ja existe no banco de dados
from flask_login import current_user # vamos usá-lo para verificar se ao editar um email com um novo email, esse novo email já existe no banco de dados

class FormCriarConta(FlaskForm): # é uma subclasse do FlaskForm, recebe os metodos e atributos dele, cada variavel é um campo do formulário, e cada campo vai ser um tipo de Field, ex username e email sao campo de texto, já a senha é um campo de senha
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email): # tem que começar com validate_, pois é assim que o submit verifca esse cara
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email already registered.Register with another email or log in to continue')  # raise é como se tivesse chamando o erro


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login') # os dois botoes não podem ter o mesmo nome, pq na nosso site eles vao estar na mesma pagina, se eu clico em um o python vai achar que to clicando nos dois e isso daria uma série de problemas


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])]) # é um campo diferente, já que é a foto de perfi do usuario, enquanto o outro a gente armazenava o nome do arquivo, vem do flask_wtf
    hero_ben = BooleanField('Ben 10')
    hero_batman = BooleanField('Batman')
    hero_superman = BooleanField('SuperMan')
    hero_flash = BooleanField('Flash')
    hero_spider = BooleanField('Homem Aranha')
    hero_capitao = BooleanField('Capitão América')
    hero_iron = BooleanField('Homem de Ferro')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email): # Evitar que a pessoa ao editar o email, acabe colocando um email que ja exista no banco de dados, tem que começar com validate_, pois é assim que o submit verifca esse cara
        # verificar se o cara mudou de email para so ai fazer a validacao e ver se o email novo ja existe no banco de dados
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('There is already a user with this email.Register another email')  # raise é como se tivesse chamando o erro


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit =SubmitField('Criar Post')