from users.cliente import Caixa


def main():
    db = Caixa()
    print("Bem vindo ao sistema!\n")

    comandos = {1: ["Entrada", db.entrada],
                2: ["Atualização de Produto", db.atualizar_produto],
                3: ["Vendas", db.vendas],
                4: ["Relatório de Itens", db.relatorio_estoque],
                5: ["Relatório de Itens em Falta", db.relatorio_baixo_estoque],
                6: ["Sair", db.fechar]}

    print("Operações disponíveis:")
    for item in comandos.keys():
        print(f"{item}) {comandos[item][0]}")

    operacao = int(input("\nDigite o ID da operação desejada: "))

    while operacao in comandos.keys():
        comandos[operacao][1]()

        if operacao == 6:
            print("Até mais!")
            break

        operacao = int(input("\nDigite a operação desejada: "))


if __name__ == "__main__":
    main()
