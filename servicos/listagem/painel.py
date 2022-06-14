from kafka import KafkaClient, TopicPartition, KafkaConsumer
from time import sleep
import json

painel_de_listagem = KafkaConsumer(
    bootstrap_servers = [ "kafka:29092" ],
    api_version = (0, 10, 1),
    auto_offset_reset = "earliest",
    consumer_timeout_ms = 1000)

topico = TopicPartition("listagem", 0)
painel_de_listagem.assign([topico])

painel_de_listagem.seek_to_beginning(topico)

offset = 0

while True:
    print("Aguardando a lista dos exercícios...")

    for aluno in painel_de_listagem:
        offset = aluno.offset + 1

        dados_do_aluno = json.loads(aluno.value)
        print(f"dados do aluno: {dados_do_aluno}")

        painel_de_listagem.seek(topico, offset)

    sleep(4)
