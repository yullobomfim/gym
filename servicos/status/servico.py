from flask_apscheduler import APScheduler

from kafka import KafkaClient, KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

from time import sleep
import random
import json

PROCESSO = "status"
LISTAGEM = "listagem"

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

def validar_status(informacoes_do_status):
    valida, mensagem, email, mensagem_de_entrega = (informacoes_do_status["sucesso"] == 1), "", "", ""

    if valida:
        mensagem = "Acesso permitido para o aluno #" + \
        informacoes_do_status["identificacao"]
        
        gerador_de_dados_falsos = faker.Faker("pt-BR")
        email = gerador_de_dados_falsos.email()
        mensagem_de_entrega = "Prezado(a), " +", o seu e-book se encontra no link abaixo:\\"
    else:
        mensagem = "Acesso não permitido para o aluno"

    return valida, mensagem, email, mensagem_de_entrega



def validar_status(dados_do_aluno):
    valido, mensagem = True, ""

    sleep(random.randint(1, 6))

    if valido:
        mensagem = "status do aluno: Autorizado"
    else: 
        mensagem = "status do aluno: Não autorizado"

    return valido, mensagem

def executar():
    global deslocamento

    consumidor_de_listagem = KafkaConsumer(
        bootstrap_servers = [ "kafka:29092" ],
        api_version = (0, 10, 1),
        auto_offset_reset = "earliest",
        consumer_timeout_ms = 1000
    )
    topico = TopicPartition(LISTAGEM, 0)
    consumidor_de_listagem.assign([topico])
    consumidor_de_listagem.seek(topico, deslocamento)

    for aluno in consumidor_de_listagem:
        deslocamento = aluno.offset + 1

        dados_do_aluno = aluno.value
        dados_do_aluno = json.loads(dados_do_aluno)

        valido, mensagem = validar_status(dados_do_aluno)
        if valido:
            dados_do_aluno["sucesso"] = 1
        else:
            dados_do_aluno["sucesso"] = 0
        dados_do_aluno["mensagem"] = mensagem

        try:
            produtor = KafkaProducer(
                bootstrap_servers = [ "kafka:29092" ],
                api_version = (0, 10, 1)
            )
            produtor.send(topic=PROCESSO, value= json.dumps(
                dados_do_aluno
            ).encode("utf-8"))
        except KafkaError as erro:
            # TODO registrar o erro em log
             print(f"ocorreu um erro: {erro}")

if __name__ == "__main__":
    iniciar()

    agendador = APScheduler()
    agendador.add_job(id=PROCESSO, func=executar, 
        trigger="interval", seconds=3)
    agendador.start()

    while True:
        sleep(60)
