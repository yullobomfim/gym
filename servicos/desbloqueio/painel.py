from kafka import TopicPartition, KafkaConsumer
from time import sleep
import json

painel_de_desbloqueio = KafkaConsumer(
    bootstrap_servers = [ "kafka:29092" ],
    api_version = (0, 10, 1),
    auto_offset_reset = "earliest",
    consumer_timeout_ms = 1000)

topico = TopicPartition("desbloqueio", 0)
painel_de_desbloqueio.assign([topico])

painel_de_desbloqueio.seek_to_beginning(topico)

offset = 0

while True:
    print("Aguardando registro dos alunos...")

    for desbloqueio in painel_de_desbloqueio:
        offset = desbloqueio.offset + 1
        
        dados_do_desbloqueio = json.loads(aluno.value)
        print(f"Código de Acesso Liberado: {dados_do_desbloqueio}")

        painel_de_desbloqueio.seek(topico, offset)

    sleep(4)
