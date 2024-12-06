import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Minigame de Resistores")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 102, 204)
VERMELHO = (204, 0, 0)
VERDE = (0, 204, 0)

# Fonte
fonte = pygame.font.Font(None, 36)

# Funções auxiliares
def calcular_corrente(resistores, configuracao):
    if len(resistores) != 4:
        return None  # O jogador deve escolher exatamente 4 resistores

    # Calcula a resistência equivalente
    if configuracao == "paralelo":
        try:
            r_eq = 1 / sum(1 / r for r in resistores)
        except ZeroDivisionError:
            return None
    elif configuracao == "série":
        r_eq = sum(resistores)
    else:
        return None

    # Calcula a corrente
    V = 12  # Tensão da bateria
    corrente = V / r_eq
    return round(corrente, 2)

def desenhar_texto(texto, x, y, cor=PRETO):
    texto_renderizado = fonte.render(texto, True, cor)
    TELA.blit(texto_renderizado, (x, y))

# Função para reiniciar o jogo
def reiniciar_jogo():
    global fase, resistores_escolhidos, configuracao, resultado
    fase = 1
    resistores_escolhidos = []
    configuracao = None
    resultado = ""

# Variáveis do jogo
resistores_disponiveis = [2, 6, 8]
resistores_escolhidos = []
configuracao = None
resultado = ""
fase = 1

# Loop principal do jogo
rodando = True
while rodando:
    TELA.fill(BRANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Lógica para reinício
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
            reiniciar_jogo()

        # Lógica para a fase 1: Seleção de resistores
        if fase == 1:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos

                # Detecta clique nos botões de resistores
                for i, r in enumerate(resistores_disponiveis):
                    if 50 + i * 150 < mouse_x < 150 + i * 150 and 200 < mouse_y < 250:
                        if len(resistores_escolhidos) < 4:
                            resistores_escolhidos.append(r)

        # Lógica para a fase 2: Escolha de configuração
        elif fase == 2:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos

                # Detecta clique nos botões de configuração
                if 200 < mouse_x < 300 and 200 < mouse_y < 250:
                    configuracao = "série"
                    fase = 3
                elif 500 < mouse_x < 600 and 200 < mouse_y < 250:
                    configuracao = "paralelo"
                    fase = 3

    # Fase 1: Seleção de resistores
    if fase == 1:
        desenhar_texto("Escolha 4 resistores:", 50, 50)
        for i, r in enumerate(resistores_disponiveis):
            pygame.draw.rect(TELA, AZUL, (50 + i * 150, 200, 100, 50))
            desenhar_texto(f"{r} Ω", 70 + i * 150, 215, BRANCO)

        desenhar_texto(f"Escolhidos: {resistores_escolhidos}", 50, 350)

        if len(resistores_escolhidos) == 4:
            desenhar_texto("Pressione Enter para avançar!", 50, 400, VERDE)
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                fase = 2

    # Fase 2: Escolha da configuração
    elif fase == 2:
        desenhar_texto("Escolha a configuração dos resistores:", 50, 50)

        # Botões para configuração
        pygame.draw.rect(TELA, AZUL, (200, 200, 100, 50))
        desenhar_texto("Série", 220, 215, BRANCO)
        pygame.draw.rect(TELA, AZUL, (500, 200, 100, 50))
        desenhar_texto("Paralelo", 520, 215, BRANCO)

    # Fase 3: Resultado
    elif fase == 3:
        corrente = calcular_corrente(resistores_escolhidos, configuracao)
        if corrente is None:
            resultado = "Configuração inválida!"
        elif corrente == 8:
            resultado = "Parabéns! A corrente é 8A. A porta foi destrancada!"
        else:
            resultado = f"Corrente calculada: {corrente}A. Tente novamente!"

        desenhar_texto(resultado, 50, 50)
        desenhar_texto("Pressione R para reiniciar.", 50, 100)

    pygame.display.flip()

# Finalização do Pygame
pygame.quit()
sys.exit()
