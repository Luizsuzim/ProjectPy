from flask import Flask, request, jsonify, render_template
from database import (
    criar_tabelas,
    inserir_cliente,
    listar_clientes,
    inserir_atendimento,
    listar_atendimentos,
    finalizar_atendimento
)


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
def tela_atendimentos():
    return render_template("atendimentos.html")


if __name__ == "__main__":
    app.run(debug=True)
