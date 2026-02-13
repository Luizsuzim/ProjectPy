from flask import Flask, request, jsonify, render_template
from database import (
    criar_tabelas,
    inserir_cliente,
    listar_clientes,
    inserir_atendimento,
    listar_atendimentos,
    finalizar_atendimento,
    atualizar_cliente,
    excluir_cliente
)

from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from database import buscar_usuario, criar_usuario
from functools import wraps
from database import existe_usuario


app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorada


criar_tabelas()

if not existe_usuario():
    senha_hash = generate_password_hash("123456")
    criar_usuario("luiz@spacesc.com.br", senha_hash)
    print("Usuário admin criado: luiz@spacesc.com.br / 123456")

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/clientes")
@login_required
def tela_clientes():
    return render_template("clientes.html")

@app.route("/api/clientes", methods=["GET"])
def get_clientes():
    clientes = listar_clientes()

    resultado = []
    for cliente in clientes:
        resultado.append({
            "id": cliente[0],
            "nome": cliente[1],
            "telefone": cliente[2]
        })

    return jsonify(resultado)


@app.route("/api/clientes", methods=["POST"])
def post_cliente():
    dados = request.get_json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")

    if not nome or not telefone:
        return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400

    inserir_cliente(nome, telefone)
    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 201

@app.route("/api/atendimentos", methods=["GET"])
def get_atendimentos():
    atendimentos = listar_atendimentos()

    resultado = []
    for a in atendimentos:
        resultado.append({
            "id": a[0],
            "cliente": a[1],
            "descricao": a[2],
            "status": a[3]
        })

    return jsonify(resultado)

@app.route("/api/atendimentos", methods=["POST"])
def post_atendimento():
    dados = request.get_json()

    cliente_id = dados.get("cliente_id")
    descricao = dados.get("descricao")

    if not cliente_id or not descricao:
        return jsonify({"erro": "Dados obrigatórios"}), 400

    inserir_atendimento(cliente_id, descricao)
    return jsonify({"mensagem": "Atendimento criado"}), 201

@app.route("/api/atendimentos/<int:id>", methods=["PUT"])
def put_atendimento(id):
    finalizar_atendimento(id)
    return jsonify({"mensagem": "Atendimento finalizado"})

@app.route("/atendimentos")
@login_required
def tela_atendimentos():
    return render_template("atendimentos.html")

@app.route("/api/dashboard")
def dashboard():
    clientes = listar_clientes()
    atendimentos = listar_atendimentos()

    abertos = [a for a in atendimentos if a[3] == "Aberto"]

    return jsonify({
        "total_clientes": len(clientes),
        "atendimentos_abertos": len(abertos)
    })

app.secret_key = "chave-super-secreta"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = buscar_usuario(email)

        if usuario and check_password_hash(usuario[2], senha):
            session["usuario_id"] = usuario[0]
            return redirect("/")
        
        return render_template("login.html", erro="Login inválido")

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/api/clientes/<int:id>", methods=["PUT"])
def put_cliente(id):
    dados = request.get_json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")

    if not nome or not telefone:
        return jsonify({"erro": "Dados obrigatórios"}), 400

    atualizar_cliente(id, nome, telefone)
    return jsonify({"mensagem": "Cliente atualizado"})

@app.route("/api/clientes/<int:id>", methods=["DELETE"])
def delete_cliente(id):
    excluir_cliente(id)
    return jsonify({"mensagem": "Cliente excluído"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

