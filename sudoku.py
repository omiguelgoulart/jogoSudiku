import random
import time
import csv
import os

# Fácil: 62 quadrados preenchidos / 19 quadrados vazios

# Médio: 53 quadrados preenchidos / 28 quadrados vazios

# Difícil: 44 quadrados preenchidos / 37 quadrados vazios

# Muito difícil: 35 quadrados preenchidos / 46 quadrados vazios

# Extremamente difícil: 26 quadrados preenchidos / 55 quadrados vazios
def gerar_tabuleiro_inicial(preenchidos=40):
    tabuleiro = [[0 for _ in range(9)] for _ in range(9)]

        # Verifica se o número pode ser inserido na posição especificada.
    def is_valid(board, row, col, num):
        if num in board[row]:  # Linha
            return False
        if num in [board[i][col] for i in range(9)]:  # Coluna
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)  # Subgrade
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    preenchidos_atual = 0
    while preenchidos_atual < preenchidos:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if tabuleiro[row][col] == 0 and is_valid(tabuleiro, row, col, num):
            tabuleiro[row][col] = num
            preenchidos_atual += 1

    return tabuleiro

def print_sudoku(board):
    for row in board:
        linha_formatada = ""
        for cell in row:
            if cell == 0:  # Célula vazia
                linha_formatada += "⬜️ "  # Quadrado branco como emoji
            else:
                linha_formatada += f"{cell} "
        print(linha_formatada)
    print()

def is_valid(board, row, col, num):
    if num in board[row]:  # Linha
        return False
    if num in [board[i][col] for i in range(9)]:  # Coluna
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)  # Subgrade
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Encontrar célula vazia
                for num in range(1, 10):  # Testar números de 1 a 9
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):  # Recursão
                            return True
                        board[row][col] = 0  # Retroceder
                return False
    return True

def salvar_ranking_csv(nome, tempo):
    arquivo_csv = "ranking_sudoku.csv"
    existe = os.path.exists(arquivo_csv)
    with open(arquivo_csv, mode="a", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        # Adicionar cabeçalho se o arquivo é novo
        if not existe:  
            escritor.writerow(["Nome", "Tempo (segundos)"])
        escritor.writerow([nome, f"{tempo:.2f}"])

def exibir_ranking_csv():
    arquivo_csv = "ranking.csv"
    if not os.path.exists(arquivo_csv):
        print("\nNenhum ranking disponível.")
        return

    print("\nRanking dos Jogadores:")
    with open(arquivo_csv, mode="r") as arquivo:
        leitor = csv.reader(arquivo)
        ranking = list(leitor)
        if len(ranking) > 1:
            ranking = sorted(ranking[1:], key=lambda x: float(x[1]))
        for i, (nome, tempo) in enumerate(ranking, 1):
            print(f"{i}. {nome} - {tempo} segundos")

def jogar_sudoku():
    tabuleiro = gerar_tabuleiro_inicial(preenchidos=25)
    print("\nTabuleiro inicial:")
    print_sudoku(tabuleiro)

    nome_jogador = input("Digite seu nome: ")
    inicio = time.time()

    if solve_sudoku(tabuleiro):
        fim = time.time()
        duracao = fim - inicio
        print("\nTabuleiro resolvido:")
        print_sudoku(tabuleiro)
        print(f"Parabéns, {nome_jogador}! Você resolveu o Sudoku em {duracao:.2f} segundos.")
        salvar_ranking_csv(nome_jogador, duracao)
    else:
        print("Não foi possível resolver o Sudoku.")

def menu():
    
    while True:
        print("\n=== Menu Principal ===")
        print("1. Jogar Sudoku")
        print("2. Exibir Ranking")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            jogar_sudoku()
        elif opcao == "2":
            exibir_ranking_csv()
        elif opcao == "3":
            print("Saindo do jogo. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Iniciar o menu principal
menu()
