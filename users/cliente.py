import sqlite3
import socket


class Caixa:
    def __init__(self):
        cnx = sqlite3.connect('caixa.db')
        cursor = cnx.cursor()

        self.cnx = cnx
        self.cursor = cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS estoque(codigo INTEGER PRIMARY KEY NOT NULL,"
                       "produto VARCHAR NOT NULL, qtdade NUMERIC, valor NUMERIC)")
        cnx.commit()

    def entrada(self):
        comando_entrada = "S"
        while comando_entrada == "S":
            input_codigo = input("Insira um código para este material: ")
            input_qtdade = float(input("Digite a quantidade deste material a entrar (em kg): "))

            self.cursor.execute("SELECT produto, qtdade FROM estoque where codigo = ?", (input_codigo,))
            conteudo = self.cursor.fetchone()

            if conteudo is not None:
                novo_estoque = conteudo[1] + input_qtdade
                self.cursor.execute("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, input_codigo))
                self.cnx.commit()
            else:
                input_material = input("Digite o nome do material que está chegando: ")
                input_valor = input("Insira o valor de venda deste material: R$")
                self.cursor.execute("INSERT INTO estoque VALUES (?, ?, ?, ?)",
                                    (input_codigo, input_material, input_qtdade, input_valor))
                self.cnx.commit()

            comando_entrada = input("Deseja adicionar outro produto no sistema? Responda com S ou N: ")

    def atualizar_produto(self):
        comando_atualizar = "S"
        while comando_atualizar == "S":
            produto_atualizado = input("Digite o código do produto a ter o valor de venda alterado: ")

            self.cursor.execute("SELECT produto FROM estoque WHERE codigo = ?", (produto_atualizado,))
            conteudo = self.cursor.fetchone()

            if conteudo is not None:
                atualizar_venda = input("Digite o valor de venda a ser atualizado: R$")
                self.cursor.execute("UPDATE estoque SET valor = ? WHERE codigo = ?",
                                    (atualizar_venda, produto_atualizado))
                self.cnx.commit()
            else:
                print("Produto inexistente!")

            comando_atualizar = input("Deseja atualizar outro produto no sistema? Responda com S ou N: ")

    @staticmethod
    def _ler_codigo_de_barras(output_codigo):
        contas = {"1": "Prefeitura", "2": "Saneamento", "3": "Energia Elétrica e Gás", "4": "Telecomunicações",
                  "5": "Órgãos Governamentais", "6": "Carnes e Assemelhados ou demais", "7": "Multas de trânsito",
                  "9": "Uso exclusivo do banco"}

        if output_codigo[1] in contas:
            compra = f"Código de barras: {contas[output_codigo[1]]}"
            valor = float(output_codigo[5:11] + output_codigo[12:16]) / 100
            print(compra)
            print(f"Valor a pagar: R$ {valor}")
        else:
            print("Código não reconhecido")
            compra = ""
            valor = 0

        return compra, valor

    def _adicionar_produto_no_carrinho(self, output_codigo):
        produto_comprado = ""
        valor_produto = 0

        self.cursor.execute("SELECT * FROM estoque WHERE codigo = ?", (output_codigo,))
        conteudo = self.cursor.fetchone()

        if conteudo is not None:
            peso = float(self._balanca())

            if conteudo[2] >= peso:
                valor_produto = conteudo[3] * peso
                produto_comprado = conteudo[1]
                print(f"O valor do(a) {produto_comprado} é R$ {valor_produto:.2f}")

                novo_estoque = float(conteudo[2]) - peso
                self.cursor.execute("UPDATE estoque SET qtdade = ? WHERE codigo = ?", (novo_estoque, output_codigo))
                self.cnx.commit()
            else:
                print("Produto insuficiente")
        else:
            print("Código não reconhecido")

        return produto_comprado, valor_produto

    @staticmethod
    def _balanca():
        host = 'localhost'
        port = 8888
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        print("Conexão estabelecida com a balança")
        reply = s.recv(4096)
        peso = round(float(reply.decode()), 3)
        s.close()

        print(f"Peso: {peso} kg")
        return peso

    def vendas(self):
        lista_compras = []
        valor_carrinho = 0

        comando_vendas = "S"
        while comando_vendas == "S":
            valor_produto = 0
            produto_comprado = ""
            output_codigo = input("Digite o código desejado: ")

            if output_codigo[0] == "7":
                produto_comprado, valor_produto = self._adicionar_produto_no_carrinho(output_codigo)
            elif output_codigo[0] == "8":
                produto_comprado, valor_produto = self._ler_codigo_de_barras(output_codigo)

            if valor_produto > 0:
                lista_compras.append(produto_comprado)
                valor_carrinho += valor_produto

            comando_vendas = input("Deseja adicionar outro produto no carrinho? Responda com S ou N: ")

        if valor_carrinho > 0:
            print("\nLista de produtos comprados:")
            for produto in lista_compras:
                print(produto)

            print(f"O valor total da compra foi R$ {valor_carrinho:.2f}")

    def relatorio_estoque(self):
        self.cursor.execute("SELECT * FROM estoque")
        conteudo = self.cursor.fetchall()

        print("Produtos cadastrados no sistema")

        if len(conteudo) > 0:
            print("\nCódigo \t Produto \t Qtdade (kg) \t Valor (R$)")

            for codigo, produto, qtdade, valor in conteudo:
                print(f"{codigo} \t {produto} \t {qtdade:.2f} \t {valor}")
        else:
            print("Não há produtos no sistema!")

    def relatorio_baixo_estoque(self):
        self.cursor.execute("SELECT produto,qtdade FROM estoque WHERE qtdade < 5")
        conteudo = self.cursor.fetchall()

        print("Produtos com baixo estoque (menos que 5 kg)")

        if len(conteudo) > 0:
            print("\nProduto \t Qtdade (kg)")

            for produto, qtdade in conteudo:
                print(f"{produto} \t {qtdade:.2f}")
        else:
            print("Não há itens em falta!")

    def fechar(self):
        self.cnx.close()
        print("Até mais!")

        exit()
