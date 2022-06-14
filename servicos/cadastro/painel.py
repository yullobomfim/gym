from kafka import TopicPartition, KafkaConsumer
from time import sleep
import json

painel_de_cadastro = KafkaConsumer(
    bootstrap_servers = ["kafka:29092"],
    api_version = (0, 10, 1),
    auto_offset_reset = "earliest",
    consumer_timeout_ms = 1000)

topico = TopicPartition("cadastro", 0)
painel_de_cadastro.assign([topico])

painel_de_cadastro.seek_to_beginning(topico)

offset =0

while True:
    print("Aguardando o cadastro de novos alunos ...")

    for aluno in painel_de_cadastro:
        offset = aluno.offset + 1
        
        dados_do_aluno = json.loads(aluno.value)
        print(f"dados do aluno: {dados_do_aluno}")
        
        painel_de_cadastro.seek(topico, offset)

    sleep(4)