from neworkut import app #  precisa do app para rodar o site, que ele precisa para inicializar, no caso temos que importar do init, mas como a pasta ja roda o init automaticamente podemos importar o app diretamente dela


if __name__ == '__main__':  # garantir que  codigo acima so vai rodar se eu estiver excutando o arquivo main
    app.run(debug=True) # rodar o site, já o debug=True faz com que nosso site rode em modo Debug, significa que toda mudança que vc fizer no codigo vai ser implementada automaticamente no site