import pygame
import random
import csv
import os
import time

pygame.init()

TAMANHO_CELULA = 60
TAMANHO_GRADE = 9
LARGURA = TAMANHO_CELULA * TAMANHO_GRADE
ALTURA = TAMANHO_CELULA * TAMANHO_GRADE
TELA = pygame.display.set_mode((LARGURA, ALTURA + 100))
pygame.display.set_caption("Sudoku")
FONT_MEDIA = pygame.font.Font(None, 40)
FONT_GRANDE = pygame.font.Font(None, 50)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
CINZA = (200, 200, 200)

ARQUIVO_RANKING = "ranking_sudoku.csv"

def salvar_ranking(nome, tempo):
    existe = os.path.exists(ARQUIVO_RANKING)
    with open(ARQUIVO_RANKING, "a", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        if not existe:
            escritor.writerow(["Nome", "Tempo (segundos)"])
        escritor.writerow([nome, f"{tempo:.2f}"])

def carregar_ranking():
    if not os.path.exists(ARQUIVO_RANKING):
        return ["Nenhum ranking disponível."]
    
    with open(ARQUIVO_RANKING, "r") as arquivo:
        leitor = csv.reader(arquivo)
        ranking = list(leitor)
        if len(ranking) > 1:
            ranking = sorted(ranking[1:], key=lambda x: float(x[1]))
        return [f"{i+1}. {linha[0]} - {linha[1]} segundos" for i, linha in enumerate(ranking)]

def is_valid(board, row, col, num):
    if num in board[row]:
        return False
    if num in [board[i][col] for i in range(TAMANHO_GRADE)]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def gerar_tabuleiro_inicial(preenchidos=40):
    tabuleiro = [[0 for _ in range(TAMANHO_GRADE)] for _ in range(TAMANHO_GRADE)]
    for _ in range(10):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if is_valid(tabuleiro, row, col, num):
            tabuleiro[row][col] = num

    resolver_sudoku(tabuleiro)
    todas_posicoes = [(row, col) for row in range(TAMANHO_GRADE) for col in range(TAMANHO_GRADE)]
    random.shuffle(todas_posicoes)

    preenchidos_atual = 81
    while preenchidos_atual > preenchidos:
        row, col = todas_posicoes.pop()
        valor_original = tabuleiro[row][col]
        tabuleiro[row][col] = 0

        copia_tabuleiro = [linha[:] for linha in tabuleiro]
        if not resolver_sudoku(copia_tabuleiro):
            tabuleiro[row][col] = valor_original
        else:
            preenchidos_atual -= 1

    return tabuleiro

def resolver_sudoku(board):
    for row in range(TAMANHO_GRADE):
        for col in range(TAMANHO_GRADE):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if resolver_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def desenhar_tabuleiro(tabuleiro, selecionada=None, chances=4, mensagem="", mensagem_inicio=None):
    TELA.fill(BRANCO)
    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            x, y = j * TAMANHO_CELULA, i * TAMANHO_CELULA
            if selecionada == (i, j):
                pygame.draw.rect(TELA, CINZA, (x, y, TAMANHO_CELULA, TAMANHO_CELULA))
            pygame.draw.rect(TELA, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)
            if tabuleiro[i][j] != 0:
                texto = FONT_MEDIA.render(str(tabuleiro[i][j]), True, PRETO)
                TELA.blit(texto, (x + 20, y + 15))
    for i in range(0, TAMANHO_GRADE + 1, 3):
        pygame.draw.line(TELA, PRETO, (0, i * TAMANHO_CELULA), (LARGURA, i * TAMANHO_CELULA), 3)
        pygame.draw.line(TELA, PRETO, (i * TAMANHO_CELULA, 0), (i * TAMANHO_CELULA, ALTURA), 3)

    texto_chances = FONT_MEDIA.render(f"Chances restantes: {chances}", True, VERMELHO)
    TELA.blit(texto_chances, (10, ALTURA + 10))

    if mensagem and mensagem_inicio:
        if time.time() - mensagem_inicio < 2:
            texto_mensagem = FONT_MEDIA.render(mensagem, True, PRETO)
            TELA.blit(texto_mensagem, (LARGURA // 2 - texto_mensagem.get_width() // 2, ALTURA + 40))

    pygame.display.flip()

def obter_nome_do_jogador():
    rodando = True
    nome = ""
    while rodando:
        TELA.fill(BRANCO)
        titulo = FONT_GRANDE.render("Digite seu nome para começar:", True, PRETO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 50))
        nome_texto = FONT_GRANDE.render(nome, True, PRETO)
        TELA.blit(nome_texto, (LARGURA // 2 - nome_texto.get_width() // 2, ALTURA // 2 + 10))
        instrucoes = FONT_MEDIA.render("Pressione Enter para confirmar.", True, PRETO)
        TELA.blit(instrucoes, (LARGURA // 2 - instrucoes.get_width() // 2, ALTURA // 2 + 60))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome:
                    rodando = False
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif evento.unicode.isalnum() or evento.unicode == " ":
                    nome += evento.unicode
    return nome

def mostrar_ranking():
    ranking = carregar_ranking()
    rodando = True
    while rodando:
        TELA.fill(BRANCO)
        titulo = FONT_GRANDE.render("Ranking", True, PRETO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 20))

        for i, linha in enumerate(ranking):
            texto = FONT_MEDIA.render(linha, True, PRETO)
            TELA.blit(texto, (50, 80 + i * 30))

        voltar = FONT_MEDIA.render("Pressione ESC para voltar", True, PRETO)
        TELA.blit(voltar, (50, ALTURA - 30))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

def jogar_sudoku():
    nome = obter_nome_do_jogador()
    tabuleiro = gerar_tabuleiro_inicial(preenchidos=40)
    tabuleiro_resolvido = [linha[:] for linha in tabuleiro]
    resolver_sudoku(tabuleiro_resolvido)
    selecionada = [0, 0]
    chances = 4
    rodando = True
    inicio = time.time()
    mensagem = ""
    mensagem_inicio = None

    while rodando:
        desenhar_tabuleiro(tabuleiro, tuple(selecionada), chances, mensagem, mensagem_inicio)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif evento.key == pygame.K_UP:
                    selecionada[0] = (selecionada[0] - 1) % TAMANHO_GRADE
                elif evento.key == pygame.K_DOWN:
                    selecionada[0] = (selecionada[0] + 1) % TAMANHO_GRADE
                elif evento.key == pygame.K_LEFT:
                    selecionada[1] = (selecionada[1] - 1) % TAMANHO_GRADE
                elif evento.key == pygame.K_RIGHT:
                    selecionada[1] = (selecionada[1] + 1) % TAMANHO_GRADE
                elif pygame.K_1 <= evento.key <= pygame.K_9:
                    i, j = selecionada
                    num = evento.key - pygame.K_0
                    if tabuleiro_resolvido[i][j] == num:
                        tabuleiro[i][j] = num
                        mensagem = "Acertou!"
                        mensagem_inicio = time.time()
                        if all(
                            tabuleiro[row][col] == tabuleiro_resolvido[row][col]
                            for row in range(TAMANHO_GRADE)
                            for col in range(TAMANHO_GRADE)
                        ):
                            fim = time.time()
                            duracao = fim - inicio
                            mensagem = f"Você ganhou! Tempo final: {duracao:.2f} segundos."
                            mensagem_inicio = time.time()
                            desenhar_tabuleiro(tabuleiro, selecionada, chances, mensagem, mensagem_inicio)
                            pygame.time.delay(3000)
                            salvar_ranking(nome, duracao)
                            rodando = False
                    else:
                        chances -= 1
                        mensagem = f"Errou! Não era esse o número."
                        mensagem_inicio = time.time()
                        if chances == 0:
                            mensagem = "Você perdeu! Tente novamente."
                            mensagem_inicio = time.time()
                            desenhar_tabuleiro(tabuleiro, selecionada, chances, mensagem, mensagem_inicio)
                            pygame.time.delay(3000)
                            rodando = False

def menu():
    rodando = True
    while rodando:
        TELA.fill(BRANCO)
        titulo = FONT_GRANDE.render("Sudoku", True, PRETO)
        jogar = FONT_MEDIA.render("1. Jogar Sudoku", True, PRETO)
        ranking = FONT_MEDIA.render("2. Ver Ranking", True, PRETO)
        sair = FONT_MEDIA.render("3. Sair", True, PRETO)
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 50))
        TELA.blit(jogar, (50, 150))
        TELA.blit(ranking, (50, 200))
        TELA.blit(sair, (50, 250))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    jogar_sudoku()
                elif evento.key == pygame.K_2:
                    mostrar_ranking()
                elif evento.key == pygame.K_3:
                    rodando = False

    pygame.quit()

menu()
