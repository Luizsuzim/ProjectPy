from flask import Flask, request, jsonify, render_template
from database import criar_tabelas, inserir_cliente, listar_clientes

app = Flask(__name__)

criar_tabelas()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clientes")
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


if __name__ == "__main__":
    app.run(debug=True)
