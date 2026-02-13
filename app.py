from flask import Flask, render_template
from database import criar_tabelas, inserir_cliente, listar_clientes

app = Flask(__name__)

criar_tabelas()

@app.route("/api/clientes", methods=["POST"])
def post_cliente():
    dados = request.get_json()

    nome = dados.get("nome")
    telefone = dados.get("telefone")

    if not nome or not telefone:
        return jsonify({"erro": "Nome e telefone são obrigatórios"}), 400

    inserir_cliente(nome, telefone)
    return jsonify({"mensagem": "Cliente cadastrado com sucesso"}), 201
if __name__ == '__main__':
    app.run(debug=True)

