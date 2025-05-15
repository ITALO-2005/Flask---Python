from flask import Flask, render_template, request

app = Flask(__name__)

listaUsuarios = []
convidados = []  # Inicializa uma lista de convidados

@app.route("/")
def principal():
    return render_template("index.html")

@app.route("/paginaLogin")
def paginaLogin():
    return render_template("login.html")

@app.route("/paginaCadastro")
def paginaCadastro():
    return render_template("cadastro.html")

@app.route("/verificarLogin", methods=["POST"])
def verificarLogin():
    login = request.form.get("loginUsuario")
    senha = request.form.get("senhaUsuario")
    
    usuario = next((u for u in listaUsuarios if u[1] == login and u[2] == senha), None)
    if usuario:
        mensagem = "Login realizado com sucesso!"
    else:
        mensagem = "Credenciais inválidas! Por favor, tente novamente."
    
    return render_template("resultado.html", mensagem=mensagem)

@app.route("/paginaBuscar")
def paginaBuscar():
    return render_template("buscar.html")

@app.route("/alterarSenha", methods=["POST"])
def alterarSenha():
    login = request.form.get("loginUsuario")
    nova_senha = request.form.get("novaSenha")
    
    for usuario in listaUsuarios:
        if usuario[1] == login:
            usuario[2] = nova_senha
            mensagem = f"Senha do usuário '{login}' alterada com sucesso!"
            break
    else:
        mensagem = "Usuário não encontrado."
    
    return render_template("resultado.html", mensagem=mensagem)

@app.route("/buscarUsuario", methods=["POST"])
def buscarUsuario():
    nome = request.form.get("nomeUsuario")
    resultados = [u for u in listaUsuarios if nome.lower() in u[0].lower()]
    
    if resultados:
        mensagem = "Usuário(s) encontrado(s):"
    else:
        mensagem = "Nenhum usuário encontrado com esse nome."

    return render_template("resultadoBusca.html", mensagem=mensagem, usuarios=resultados)

@app.route("/paginaLista")
def paginaLista():
    return render_template("listar.html", usuarios=listaUsuarios)

@app.route("/cadastrarUsuario", methods=["POST"])
def cadastrar():
    nome = request.form.get("nomeUsuario")
    login = request.form.get("loginUsuario")
    senha = request.form.get("senhaUsuario")
    
    listaUsuarios.append([nome, login, senha])
    mensagem = "Usuário Cadastrado com Sucesso"
    return render_template("resultado.html", mensagem=mensagem)

@app.route("/paginaExcluir")
def paginaExcluir():
    return render_template("excluir.html")

@app.route("/verificarUsuario", methods=['POST'])
def verificar():
    nome = request.form.get("nomeUsuario")
    if nome in convidados:
        mensagem = "Você está convidado"
    else:
        mensagem = "Você NÃO está convidado"
    return render_template("resultado.html", mensagem=mensagem)


@app.route("/excluirUsuario", methods=["POST"])
def excluir():
    login = request.form.get("loginUsuario")
    global listaUsuarios
    listaUsuarios = [u for u in listaUsuarios if u[1] != login]
    mensagem = f"Usuário com login '{login}' excluído com sucesso!" 
    return render_template("resultado.html", mensagem=mensagem)

@app.route("/listarConvidados")
def listar():
    return render_template("listar.html", convidados=convidados)

app.run(debug=True)