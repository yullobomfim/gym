from sys import api_version
from flask_apscheduler import APScheduler
from kafka import KafkaClient, KafkaProducer, KafkaConsumer, TopicPartition
from kafka.errors import KafkaError
from time import sleep
import json

PROCESSO = "listagem"
CADASTRO = "cadastro"
    
def iniciar():
    global deslocamento
    deslocamento = 0

    cliente = KafkaClient(
        bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1)
    )
    cliente.add_topic(PROCESSO)
    cliente.close()

EXERCICIO = "/workdir/exercicios.json"


def executar():
    global deslocamento

    consumidor_de_desbloqueio = KafkaConsumer(
        bootstrap_servers=["kafka:29092"],
        api_version=(0, 10, 1),
        auto_offset_reset="earliest",
        consumer_timeout_ms=1000
    )
    topico = TopicPartition(CADASTRO, 0)
    consumidor_de_desbloqueio.assign([topico])
    consumidor_de_desbloqueio.seek(topico, deslocamento)


        try:
            produtor = KafkaProducer(
                bootstrap_servers=["kafka:29092"],
                api_version=(0, 10, 1)
            )
            produtor.send(topic=PROCESSO, value=json.dumps(
                dados_do_aluno).encode("utf-8"))
        except KafkaError as erro:
            # TODO registrar erros em log (pode ate ser um topico no kafka)
            print(f"ocorreu um erro: {erro}")


if __name__ == "__main__":
    iniciar()

    agendador = APScheduler()
    agendador.add_job(id=PROCESSO, func=executar,
                      trigger="interval", seconds=3)
    agendador.start()

    while True:
        sleep(60)
