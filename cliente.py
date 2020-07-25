import sqlite3
import socket

class Caixa():

    def __init__ (self):
        cnx = sqlite3.connect ('caixa.db')
        cursor = cnx.cursor()

        self.cnx = cnx
        self.cursor = cursor
        cursor.execute ("CREATE TABLE if not exists estoque (produto text, qtdade real, valor real, codigo real)")
        cnx.commit()
    
    def entrada (self):
        comando_entrada = "S"
        while comando_entrada == "S":
            input_material = input ("Digite o material que está chegando: ")
            input_qtdade = float (input ("Digite a quantidade deste material a entrar (em kg): "))

            self.cursor.execute ("SELECT produto,qtdade FROM estoque where produto = ?", (input_material,))
            conteudo = self.cursor.fetchone()

            if conteudo is not None:
                novo_estoque = conteudo [1] + input_qtdade
                self.cursor.execute ("UPDATE estoque SET qtdade = ? WHERE produto = ?", (novo_estoque, input_material))
                self.cnx.commit()

            else:
                input_codigo = input ("Insira um código para este material: ")
                input_valor = input ("Insira o valor de venda deste material: R$")
                self.cursor.execute ("INSERT INTO estoque VALUES (?, ?, ?, ?)", (input_material, input_qtdade, input_valor, input_codigo))
                self.cnx.commit()

            comando_entrada = input ("Deseja adicionar outro produto no sistema? Responda com S ou N: ")
    
    def atualizarProduto (self):
        comando_atualizar = "S"
        while comando_atualizar == "S":
            produto_atualizado = input ("Digite o produto a ter o valor de venda alterado: ")

            self.cursor.execute("SELECT produto FROM estoque WHERE produto = ?", (produto_atualizado,))
            conteudo = self.cursor.fetchone()

            if conteudo is not None:
                atualizar_venda = input ("Digite o valor de venda a ser atualizado: R$")
                self.cursor.execute ("UPDATE estoque SET valor = ? WHERE produto = ?", (atualizar_venda, produto_atualizado))
                self.cnx.commit()

            else:
                print ("Produto inexistente")
            
            comando_atualizar = input ("Deseja atualizar outro produto no sistema? Responda com S ou N: ")
            
    def vendaBarras (self, output_codigo):
        contas = {"1": "Prefeitura", "2": "Saneamento", "3": "Energia Elétrica e Gás", "4": "Telecomunicações",
                  "5": "Órgãos Governamentais", "6": "Carnes e Assemelhados ou demais", "7": "Multas de trânsito",
                  "9": "Uso exclusivo do banco"}

        if output_codigo [1] in contas:
            compra = (f"Código de barras: {contas [output_codigo [1]]}")
            valor = float (output_codigo [5:11] + output_codigo [12:16]) / 100

            print (compra)
            print (f"Valor a pagar: R$ {valor}")

        else:
            print ("Código não reconhecido")
            compra = ""
            valor = 0

        return (compra, valor)
    
    def vendaMateriais (self, output_codigo):
        self.cursor.execute ("SELECT * FROM estoque WHERE codigo = ?", (output_codigo,))
        conteudo = self.cursor.fetchone()

        if conteudo is not None:
            peso = float (self.balanca())

            if conteudo [1] >= peso:
                valor_produto = conteudo [2] * peso
                produto_comprado = conteudo [0]
                print (f"O valor do(a) {produto_comprado} é R$ {valor_produto:.2f}")

                novo_estoque = float (conteudo [1]) - peso
                self.cursor.execute ("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, output_codigo))
                self.cnx.commit()

            else:
                print ("Produto insuficiente")
                produto_comprado = ""
                valor_produto = 0

        return (produto_comprado, valor_produto)
    
    def balanca(self):
        host = 'localhost';
        port = 8888;
        s = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
        s.connect ((host, port))

        print ("Conexão estabelecida com a balança")

        reply = s.recv(4096)
        print (f"Peso: {reply.decode()} kg")
        return (reply.decode())
        s.close()
    
    def vendas (self):
        lista_compras = []
        valor_carrinho = 0

        comando_vendas = "S"
        while comando_vendas == "S":
            output_codigo = input ("Digite o código desejado: ")

            if output_codigo [0] == "7":
                produto_comprado, valor_produto = self.vendaMateriais (output_codigo)

            elif output_codigo [0] == "8":
                produto_comprado, valor_produto = self.vendaBarras (output_codigo)

            else:
                produto_comprado = ""
                valor_produto = 0

            lista_compras.append (produto_comprado)
            valor_carrinho += valor_produto

            comando_vendas = input ("Deseja adicionar outro produto no carrinho? Responda com S ou N: ")

        print ("\nLista de produtos comprados")
        for produto in lista_compras:
            if produto != "":
                print (produto)

        if valor_carrinho != 0:
            print (f"O valor total da compra foi R$ {valor_carrinho:.2f}")
            
    def resumoItens (self):
        self.cursor.execute ("SELECT produto,qtdade,valor FROM estoque")

        print ("\nRelatório Gerencial")
        print ("Produtos cadastrados no sistema")
        print ("\nProduto \t Qtdade (kg) \t Valor (R$)")

        for produto, qtdade, valor in self.cursor.fetchall():
            print (f"{produto} \t {qtdade:.2f} \t {valor}")
            
    def resumoBaixoEst (self):
        self.cursor.execute ("SELECT produto,qtdade FROM estoque WHERE qtdade < 5")

        print ("\nRelatório Gerencial")
        print ("Produtos com baixo estoque (menos que 5 kg)")
        print ("\nProduto \t Qtdade (kg)")

        for produto, qtdade in cursor.fetchall():
            print (f"{produto} \t {qtdade:.2f}")

    def fechar (self):
        self.cnx.close()

db = Caixa()
print ("Bem vindo ao sistema!\n\nQue operação deseja realizar? Digite:")
operacao = int (input ("1 para Entrada \n2 para Atualização do Valor de Venda \
                       \n3 para Vendas \n4 para Relatório \n5 para Sair\n"))

while operacao < 5:
    if operacao == 1:
        db.entrada()

    elif operacao == 2:
        db.atualizarProduto()

    elif operacao == 3:
        db.vendas()

    elif operacao == 4:
        tipo = int (input ("Digite 1 para resumo de todos os itens ou 2 para um resumo de itens com baixo estoque\n"))
        if tipo == 1:
            db.resumoItens()
        elif tipo == 2:
            db.resumoBaixoEst()

    operacao = int (input ("Deseja fazer outra operação? Digite: \n1 para Entrada \n2 para Atualização do Valor de Venda \
                            \n3 para Vendas \n4 para Relatório \n5 para Sair\n"))

print ("Até mais!")
