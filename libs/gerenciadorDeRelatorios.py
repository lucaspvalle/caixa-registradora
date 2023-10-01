from tabulate import tabulate


class GerenciadorDeRelatorios:
    def __init__(self, cnx):
        """
        Inicializa o gerenciador, herdando a conexão com o banco de dados da caixa.

        :param cnx: conexão com o banco de dados da caixa registradora.
        """
        self.cnx = cnx

    @staticmethod
    def _print_tabulate(conteudo, headers):
        print(tabulate(conteudo, headers=headers, tablefmt="rst", floatfmt=".2f"))

    def gerar_relatorio_de_estoque(self, filtro_de_estoque: int = 0):
        """
        Função para exportar relatório de estoque, com a possibilidade de filtrar produtos
        com estoque abaixo de um certo nível. Se nenhum valor for informado, o sistema
        exporta o relatório de estoque inteiro no presente momento.

        :param filtro_de_estoque: valor máximo de estoque no relatório
        :return: nível de estoque da empresa por produto
        """

        print_string = "Relatório Gerencial"

        query = "SELECT * FROM estoque"
        if filtro_de_estoque:
            query += " WHERE qtdade <= " + str(filtro_de_estoque)
            print_string += " (filtro de " + str(filtro_de_estoque) + " kg)"

        print("\n" + print_string + ":")
        conteudo = self.cnx.execute(query).fetchall()

        if len(conteudo) > 0:
            self._print_tabulate(conteudo, headers=["Código", "Produto", "Quantidade (kg)", "Valor (R$)"])
        else:
            print("\nNão há produtos para este relatório!")

    def gerar_relatorio_de_compras(self, carrinho: dict):
        """
        Para todos os produtos adicionados no carrinho, formata e exporta o relatório.

        :param carrinho: contém os produtos comprados e seus respectivos valores
        :return: relatório de compras, se algum produto for comprado
        """
        if len(carrinho) > 0:
            print("\nLista de produtos comprados:")
            self._print_tabulate(carrinho.items(), headers=["Produto", "Valor (R$)"])
            print(f"O valor total da compra foi de R$ {sum(carrinho.values()):.2f}.")
        else:
            print("\nNenhum produto foi comprado.")
