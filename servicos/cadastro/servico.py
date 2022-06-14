from flask import Flask, jsonify
from kafka import KafkaClient, KafkaProducer
from kafka.errors import KafkaError
import hashlib
import random
import string
import json
from time import sleep

servico = Flask(__name__)

PROCESSO = "cadastro"
DESCRICAO = "Plataforma para a gestão de academias"
VERSAO = "0.0.1"


def iniciar():
    cliente = KafkaClient(
        bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1)
    )
    cliente.add_topic(PROCESSO)
    cliente.close()

@servico.route("/info", methods=["GET"])
def get_info():
    return jsonify(descricao=DESCRICAO, versao=VERSAO)

@servico.route("/executar/<string:nome>/<string:status>", methods=["GET", "POST"])
def executar(nome, status):
    resultado = {
        "resultado": "sucesso",
        "id_transacao": ""
    }
    sleep(4)

    ID = "".join(random.choice(string.ascii_letters + string.punctuation)
                 for _ in range(12))
    ID = hashlib.md5(ID.encode("utf-8")).hexdigest()


    try:
        produtor = KafkaProducer(
            bootstrap_servers = ["kafka:29092"],
            api_version = (0, 10, 1)
        )
        confirmacao_de_cadastro = {
            "identificacao": ID,
            "sucesso": 1, 
            "mensagem": "Aluno cadastrado com sucesso",
            "id": id,
            "nome": nome,
            "status": status
        }
        produtor.send(
            topic=PROCESSO,
            value=json.dumps(confirmacao_de_cadastro).encode("utf-8")
        )

        resultado["id_transacao"] = ID
    except KafkaError as erro:
        resultado["resultado"] = f"erro ocorrido durante a etapa do cadastro: {erro}"

    return json.dumps(resultado).encode("utf-8")

if __name__ == "__main__":
    iniciar()

    servico.run(
        host="0.0.0.0",
        debug=True
    )
