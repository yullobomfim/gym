Monitoramento de Frequencia e Liberação de catraca de Acesso

Enviar pergunta. Quem vai participar do treino do dia?

1º serviço para registrar a matricula do aluno na academia; 

nome_aluno,string
aula, string
aluno_presente, boolean (inicia false)
treino_realizado, false
    
2º serviço desbloqueia o acesso à catraca ; 
aluno(ID,nome)
nome

aula(ID,professor,data)


id_aula, string
exercicios, string
aluno_presente, true


3º envia a lista dos exercicíos do treino do dia para os alunos registrados
lista o nome do aluno matriculado e envia listagem dos exercicios
serviço confirma os alunos que marcaram presença no dia(ex:segunda,terça...)

id_aluno,string
id_aula, string
treino_realizado, true
aluno_presente, false

4º serviço verifica os exercicios feitos e confirma os alunos participantes

id_aluno,string
id_aula, string
lista_alunos, string
aluno_presente, boolean

"O meu tema para a atividade de Desenvolvimento Distribuído na internet será para a criação de uma solução baseada em uma plataforma para a gestão de alunos em academia onde serão utilizados micro serviços e o apache kafka para coreografar os serviços.

1- Serviço para realizar a Matrícula de um novo aluno,
                registrar o status de aluno.... presença do aluno ao BOX
2- Serviço para o desbloqueio de acesso na catraca e o acesso ao treino,
                alterar o status do aluno que acessar e alterar para Treino realizado(true)
3- Serviço de listagem dos exercícios a serem realizados na semana,
                envia uma relação dos exercícios do dia
4- Serviço que atualiza a relação dos alunos e sua situação financeira."
                atualiza o status do treino 