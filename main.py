from users.cliente import Caixa


def main():
    db = Caixa()
    print("Bem vindo ao sistema!\n")

    comandos = {1: ["Entrada", db.entrada],
                2: ["Atualização de Produto", db.atualizar_produto],
                3: ["Vendas", db.vendas],
                4: ["Relatório de Itens", db.relatorio_estoque],
                5: ["Sair", db.fechar]}

    print("Operações disponíveis:")
    for item in comandos.keys():
        print(f"{item}) {comandos[item][0]}")

    while True:
        operacao = int(input("\nDigite o ID da operação desejada: "))

        if operacao in comandos.keys():
            comandos[operacao][1]()


if __name__ == "__main__":
    main()
