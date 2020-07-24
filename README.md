# caixaregistradora-sql

Este projeto foi desenvolvido para uma disciplina da faculdade.

A estrutura é composta por um banco de dados para o controle de estoque, o qual:
* Permitirá a entrada de produtos, atualizando a quantidade e, se quiser, o valor de venda
* Permitirá a saída (venda de produtos), de acordo com o estoque da empresa

Para isso, há duas interfaces:
* A interface para o cliente, isto é: funcionário da empresa, realiza todas as operações do banco de dados (entrada e saída de materiais, atualizações e relatórios gerenciais)
* A interface de servidor simulará uma balança conectada à máquina, que proverá um valor aleatório para o peso dos materiais a serem vendidos

Os materiais vendidos pela empresa são cadastrados com um código de 4 números, iniciados com o dígito 7 para reconhecimento. Por outro lado, códigos iniciados com o dígito 8 reconhecem códigos de barras para o pagamento de contas, de acordo com o padrão estabelecido pela Febraban.

Em suma, o sistema, portanto, possui:
* Padrão de leitura dos código de barras
* Balança para pesagem dos produtos
* Banco de dados para armazenamento de estoque, com seus respectivos valores de venda
