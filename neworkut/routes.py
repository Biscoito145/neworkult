from neworkut import app, database, bcrypt
from neworkut.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from flask import render_template, flash, redirect, url_for, request,abort
from neworkut.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required # para fazer e sair do login, respectivamente. Ja o current user verfica o usuario que esta mexendo naquele momento. O loguin_required é uma função que usamos como decorator para atribuir caracreristcas ás nossas funções
import secrets # gerar numeros aleatorios
import os # separar o filename em nome do arquivo mais a extensão, para que no meio deles eu adicione o código aleatório
from PIL import Image # vamos usar isso para reduir o tamanho da imagem




@app.route("/")  # uma funcao que vai dizer o que vai acontecer com uma pagina, no parenteses temos o caminho, ou seja, onde essa função vai ser rodada, como não estamos passando nada, depois da barra, esse é o caminho da nossa homepage -> em qual link vai ficar nossa página
def home():
    posts = Post.query.order_by(Post.id.desc()) # poderia ter usado o query.all(), mas dessa maneira eu exibo primeiro os posts mais recentes
    return render_template('home.html', posts=posts)  # agr ele vai retornar o arquivo html, basta passar como parametro o nome do arquivo html


@app.route("/contato")  # esse @app.route('') é o que chamamos de decorator. O app é uma instância da classe Flask, e o route é um método dessa classe. Decorator é uma função que você cloca antes de outra função e sempre vem com o @ antes. Ele é uma função que atribuiu a outra função uma funcionalidade, ou seja, atribuindo uma funcionalidade nova ao cara que ta embaixo dele
def contato():
    return render_template('contato.html')


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:  # verifica se o formulario de login foi preenchido corretamente e verifica se foi o botao de login, ja que temos dois formularios na pagina, a gente precisa diferenciar, e ai a gente usa o nome do botão para isso, se foi entao. Porque como temos duas condições, pelo fato dos dois forms estarem na mesma página, ele vai querer verifcar os dois, mas a pessoa so vai ter preenchido 1, entao é por isso que usamos esse and...  vai verificar se nessa requisao post que fizemos tem o submit login para o login e o criarconta para o criarconta, entao em suma, ele ta verificando se o formulario foi preecnhido e se o botao clicado foi o de login
        # exibir login bem sucedido
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() # definindo o usuario, onde email é o que ele preencheu, e usando um filtro para localizá-lo no banco de dados
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'),form_login.senha.data): # se o usuario existe no banco de dados e a senha que esta no banco de dados bate com a que ele preencheu no login esta correta:
            login_user(usuario, remember= form_login.lembrar_dados.data)  # fazendo efetivamente o login do usuario, se a pessoa marcou a caixa é true senão é falso
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')  # para ecibir o email da pessoa, o data exibe o resultado do que a pessoa preecheu
            # redirecionar para homepage
            par_next = request.args.get('next') # pegando o parametro next da url, que é para onde ele quer ir
            if par_next: # se existe ent o usuario vai ser redirecionado para a pagina que estava tentando acessar
                return redirect(par_next)
            else: # so esta tentando fazer login para acessar a conta
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos','alert-danger') # tipo de alerta danger -> caixa vermelha
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # criar o Usuario no banco de dados, criamos uma instancia da classe usuario, mas agora os parametros devem ser o que a pessoa digitou
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)  # vou adicionar o que o usuario escreveu
        database.session.add(usuario)  # adicionando no banco de dados
        database.session.commit()
        # criou conta com sucesso
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) # definindo a foto padrão de um usuario / url_for('nome da pasta', filename='nome do arquivo') -> se o arquivo tiver dentro de mais uma pasta coloque url_for('nome da pasta', filename='pasta_que_ele_ta/nome_arquivo') current_user.foto_peril vai dar o nome da foto do usuario, como haviamos definido no models, isso torna essa foto_perfil dinamica, pq o parametro foto_perfil é o nome do arquivo da foto da pessoa
    return render_template('perfil.html', foto_perfil=foto_perfil) # vamos passar a variavel foto_perfil para o html


@app.route('/post/criar',  methods=['GET', 'POST'])
@login_required # restringindo a pagina apenas para usuarios
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

# if current_user.is_authenticated() # verificar se o usuário está logado se for verdadeiro siginifca que está logado, falso não, vamos aplicar isso na nossa barra de nacegação para personalizar a página para um usuário que está logado

def salvar_imagem(imagem): # para ficar mais organizado vamos colocar essas etapas numa função que retorna o nome do arquivo
    # adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8)  # gerar um token aleatorio
    nome, extensão = os.path.splitext(imagem.filename)  # separando o nome do arquivo e a extensão
    nome_arquivo = nome + codigo + extensão  # juntando os nomes
    caminho_completo = os.path.join(app.root_path,'static/fotos_perfil', nome_arquivo)  # app.rooth_path  é o caminho do nosso aplicativo e temos que juntá-lo com a pasta static, a pasta fotos_perfil e o default.jpg
    # reduzir o tamanho da imagem
    tamanho = (400, 400) # vamos deixar 200 px por 200 px
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'hero_' in campo.name:
            if campo.data: # se o campo esta marcado eu adiciono
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar',methods=['GET', 'POST']) # quando o usuari clicou no botão editar perfil vamos redirecioná-lo para essa página, mas essa pagina vai ser igual a que ele tava, mas  agora aparecendo o formulario
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data: # verficando se ele está fazendo o upload de algum arquivo
            # adicionar um código aleatório no nome da imagem
            # reduzir o tamanho da imagem
             # salvar a imagem na pasta fotos_perfil
            # mudar o campo foto_perfil do usuario para o nome da imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET': # quando clicamos para validar o formulario fazemos um request no site, entao quando clicamos no formulario a função roda, quando eu clico no formulario estou enviando uma informação do método POST, ous eja estamos fazendo um request do método POST para o site  e ai ele preecnhe conforme colocamos na função, agora se for GET, ou seja, estamos apenas carregando a página ai eu vou querer que o campo apareça preenchido
        form.email.data = current_user.email # quando carregar a página, os campos já estarão preenchidos com o email e username do cara
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) # para aparcer a imagem de perfil quando ele for para essa pagina
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Editado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
        
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)


