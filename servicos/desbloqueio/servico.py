from flask_apscheduler import APScheduler
from kafka import KafkaClient, KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from time import sleep
import random
import json

PROCESSO = "desbloqueio"
STATUS = "status"

def iniciar():
    global deslocamento
    deslocamento = 0

    cliente = KafkaClient(
        bootstrap_servers = [ "kafka:29092" ],
        api_version = (0, 10, 1)
    )
    cliente.add_topic(PROCESSO)
    cliente.close()

    LISTA = "/workdir/listagem.json"

    def validar_cadastro(confirmacao_de_cadastro):
        valida, nome, mensagem  = (confirmacao_de_cadastro["sucesso"] == 1), "", "", ""

    if valida:
        with open(LISTA, "r") as arquivo_listagem:
            listagem = json.load(arquivo_listagem)
            alunos = listagem["alunos"]

            for aluno in alunos:
                print(aluno)

                if aluno["id"] == confirmacao_de_cadastro["id"]:
                    nome = aluno["nome"]
                    
                    valida = (confirmacao_de_cadastro["status"] == aluno["ativo"])
                    if valida:
                        mensagem = "Aluno com acesso liberado. Código de identificação #" + confirmacao_de_cadastro["identificacao"]
                    else:
                        mensagem = "Aluno não cadastrado"
                    break

            arquivo_listagem.close()
    else:
        mensagem = "O cadastro não foi realizado"

    return valida, nome, mensagem

def executar():
    global deslocamento

    consumidor_de_status = KafkaConsumer(
        bootstrap_servers = [ "kafka:29092" ],
        api_version = (0, 10, 1),
        auto_offset_reset = "earliest",
        consumer_timeout_ms = 1000
    )
    topico = TopicPartition(STATUS, 0)
    consumidor_de_status.assign([topico])
    consumidor_de_status.seek(topico, deslocamento)

        for status in consumidor_de_status:
            offset = status.offset + 1

        informacoes_do_status = status.value
        informacoes_do_status = json.loads(informacoes_do_status)

        valida, mensagem = validar_status(informacoes_do_status)
        sleep(4)

        if valida:
            informacoes_do_status["sucesso"] = 1
        else:
            informacoes_do_status["sucesso"] = 0
            
        informacoes_do_status["mensagem"] = mensagem

        try:
            produtor = KafkaProducer(
                bootstrap_servers=["kafka:29092"],
                api_version=(0, 10, 1)
            )
            produtor.send(topic=PROCESSO, value=json.dumps(informacoes_do_status).encode("utf-8"))
            
        except KafkaError as erro:
            resultado = f"erro: {erro}"

    # deveria enviar para um log
    print(resultado)


if __name__ == "__main__":
    iniciar()

    agendador = APScheduler()
    agendador.add_job(id=PROCESSO, func=executar, 
        trigger="interval", seconds=3)
    agendador.start()

    while True:
        sleep(60)
