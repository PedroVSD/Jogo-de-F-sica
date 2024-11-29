import pygame
import sys
import math

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mover Imagem com Fundo Estático")

# Carregar a imagem de fundo
fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\imagem.png")  # Substitua por sua imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela

# Carregar a imagem móvel
imagem = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\este.jpg")  # Substitua por sua imagem
imagem = pygame.transform.scale(imagem, (100, 100))  # Redimensiona para 100x100 pixels

# Carregar a imagem da lupa
imagem_lupa = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\lupa.png")  # Substitua por sua imagem
imagem_lupa = pygame.transform.scale(imagem_lupa, (25, 25))  # Redimensiona para 25x25 pixels

# Definir a opacidade inicial da lupa
imagem_lupa.set_alpha(0)  # 0 é totalmente transparente inicialmente

# Posição inicial da imagem móvel
posicao_x, posicao_y = 350, 250

# Variável de controle
movendo = False  # Indica se a imagem está sendo arrastada

# Posição da lupa
lupa_x, lupa_y = 230, 481

# Tamanho da imagem da lupa
lupa_width, lupa_height = imagem_lupa.get_width(), imagem_lupa.get_height()

# Raio de interação da lupa (metade da largura da lupa)
raio_interacao = max(lupa_width, lupa_height)  # Usamos o maior valor como raio para um "círculo de interação"

# Função para calcular a distância entre o cursor e o centro da lupa
def distancia_entre_pontos(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Função para verificar se o mouse está dentro do raio de interação
def esta_no_raio_interacao(mouse_x, mouse_y, lupa_x, lupa_y, raio):
    distancia = distancia_entre_pontos((mouse_x, mouse_y), (lupa_x + lupa_width // 2, lupa_y + lupa_height // 2))
    return distancia < raio

# Variáveis para a janela de pergunta
pergunta_ativa = False
pergunta = "Determine a força elétrica entre duas cargas de q1=2μC q2=-3μC, separadas por uma distância de d=0.5m"
resposta_correta = "0.216"
resposta_usuario = ""
contador = 0
mensagem_correta = False  # Indica se a mensagem "Resposta correta!" deve ser exibida
tempo_mensagem = 0        # Temporizador para exibir a mensagem (em milissegundos)
DURACAO_MENSAGEM = 2000   # Tempo de exibição da mensagem (2 segundos)


# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # Detectar clique do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:
            print(f'Clique do mouse: {evento.pos}')
            mouse_x, mouse_y = evento.pos  # Pega a posição do clique
            # Verifica se o clique foi dentro da imagem da lupa
            if esta_no_raio_interacao(mouse_x, mouse_y, lupa_x, lupa_y, raio_interacao):
                pergunta_ativa = True  # Exibe a pergunta
                resposta_usuario = ""  # Limpa a resposta

        # Detectar quando o botão do mouse é solto
        if evento.type == pygame.MOUSEBUTTONUP:
            movendo = False

        # Detectar movimento do mouse
        if evento.type == pygame.MOUSEMOTION:
            if movendo:
                mouse_x, mouse_y = evento.pos
                # Atualizar posição da imagem móvel com base no movimento do mouse
                posicao_x = mouse_x - offset_x
                posicao_y = mouse_y - offset_y

        # Detectar tecla pressionada para digitar a resposta
        if evento.type == pygame.KEYDOWN and pergunta_ativa:
            if evento.key == pygame.K_RETURN:  # Quando pressionar Enter
                if resposta_usuario.lower() == resposta_correta.lower():  # Verifica se a resposta está correta
                    contador += 1  # Incrementa o contador
                    mensagem_correta = True  # Ativa a exibição da mensagem
                    tempo_mensagem = pygame.time.get_ticks()  # Armazena o tempo atual
                    print("Resposta correta!")
                pergunta_ativa = False  # Fecha a janela de pergunta
            elif evento.key == pygame.K_BACKSPACE:
                resposta_usuario = resposta_usuario[:-1]  # Apaga um caractere
            else:
                resposta_usuario += evento.unicode  # Adiciona a letra pressionada

    # Obter a posição do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Verificar se o mouse está dentro do raio de interação da lupa
    if esta_no_raio_interacao(mouse_x, mouse_y, lupa_x, lupa_y, raio_interacao):
        imagem_lupa.set_alpha(255)  # Tornar a lupa mais visível
    else:
        imagem_lupa.set_alpha(0)  # Manter opacidade baixa

    # Desenhar o fundo (estático)
    TELA.blit(fundo, (0, 0))

    # Desenhar a imagem da lupa
    TELA.blit(imagem_lupa, (lupa_x, lupa_y))

    # Desenhar a imagem móvel
    TELA.blit(imagem, (posicao_x, posicao_y))

    # Se a janela de pergunta estiver ativa, desenhar a caixa de pergunta
    if pergunta_ativa:
        font = pygame.font.Font(None, 36)
        texto_pergunta = font.render(pergunta, True, (255, 255, 255))
        TELA.blit(texto_pergunta, (LARGURA // 4, ALTURA // 4))  # Exibe a pergunta

        texto_resposta = font.render(resposta_usuario, True, (255, 255, 255))
        TELA.blit(texto_resposta, (LARGURA // 4, ALTURA // 2))  # Exibe a resposta digitada

        # Exibe a instrução para pressionar Enter
        texto_instrucoes = font.render("Pressione Enter para responder", True, (255, 255, 255))
        TELA.blit(texto_instrucoes, (LARGURA // 4, ALTURA // 1.5))

    # Exibir o contador
    font = pygame.font.Font(None, 36)
    texto_contador = font.render(f"Contador: {contador}", True, (255, 255, 255))
    TELA.blit(texto_contador, (10, 10))

    if mensagem_correta:
        font = pygame.font.Font(None, 36)
        texto_mensagem = font.render("Resposta correta!", True, (0, 255, 0))  # Texto em verde
        TELA.blit(texto_mensagem, (10, 50))  # Desenha abaixo do contador

        # Verifica se o tempo de exibição já passou
        if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
            mensagem_correta = False  # Para de exibir a mensagem

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
