import pygame
import sys
import math
from time import sleep

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 634, 634  # Tamanho da tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Escape Room de Física")  # Título da janela


# Carregar a imagem da lupa
lupa_Iteracao = pygame.image.load("Imagens\\lupa.png")  # Substitua por sua imagem
lupa_Iteracao = pygame.transform.scale(lupa_Iteracao, (25, 25))  # Redimensiona para 25x25 pixels
lupa_Iteracao.set_alpha(0)  # 0 é totalmente transparente inicialmente

# Posições para as lupas usando um dicionário


tempos_mensagens = {}

#Mensagens associadas



#Variaveis do jogo
lupa_x, lupa_y = 0, 0
posicoes_lupas = {}
mensagens = {}
mensagem_ativa =""
resposta_usuario = ""
contador = 0
tempo_mensagem = 0        # Temporizador para exibir a mensagem (em milissegundos)
DURACAO_MENSAGEM = 2000   # Tempo de exibição da mensagem (2 segundos)




# FUNÇÕES:

# Função para processar as interações do maouse
def processar_interecao(mouse_x, mouse_y, modo = "distancia", alvo_x = None, alvo_y=None, raio = 25, posicoes_lupas=None):
        
    if modo == "distancia":
        if alvo_x is None or alvo_y is None:
            raise ValueError("alvo_x e alvo_y são necesssários no modo 'distancia'")
        return math.sqrt((alvo_x - mouse_x) ** 2 + (alvo_y - mouse_y) ** 2)
    
    elif modo == "raio":
        if alvo_x is None or alvo_y is None:
            raise ValueError("alvo_x e alvo_y são necesssários no modo 'raio'")
        distancia = math.sqrt((alvo_x - mouse_x) ** 2 + (alvo_y - mouse_y) ** 2)
        return distancia < raio

    elif modo == "clique_fora":
        if alvo_x is None or alvo_y is None:
            raise ValueError("alvo_x e alvo_y são necesssários no modo 'clique_fora'")
        return not any(
            processar_interecao(mouse_x, mouse_y, modo = "raio", alvo_x = x, alvo_y = y, raio = raio)
            for x, y in posicoes_lupas.values()
        )

    else:
        raise ValueError

# Função para mostrar mensagem na tela
def mostrar_mensagem(mensagem):
    font = pygame.font.Font(None, 30)
    palavras = mensagem.split(' ')
    linhas = []
    linha_atual = ""
    for palavra in palavras:
        if font.size(linha_atual + palavra)[0] < LARGURA - 40:
            linha_atual += palavra + " "
        else:
            linhas.append(linha_atual)
            linha_atual = palavra + " "
    linhas.append(linha_atual)
    
    menu_largura, menu_altura = LARGURA - 40, len(linhas) * font.get_linesize() + 20
    menu_x, menu_y = 20, ALTURA - menu_altura - 100
    pygame.draw.rect(TELA, (0, 0, 0, 100), (menu_x, menu_y, menu_largura, menu_altura))
    pygame.draw.rect(TELA, (255, 255, 255), (menu_x, menu_y, menu_largura, menu_altura), 2)
    y_offset = menu_y + 10
    for linha in linhas:
        texto_mensagem = font.render(linha, True, (255, 255, 255))
        TELA.blit(texto_mensagem, (menu_x + 10, y_offset))
        y_offset += font.get_linesize()

# Função para mostrar pergunta na tela
def mostrar_pergunta():
    global resposta_usuario
    font = pygame.font.Font(None, 36)

    texto_resposta = font.render(resposta_usuario, True, (255, 255, 255))
    resposta_largura, resposta_altura = LARGURA - 40, 50
    resposta_x, resposta_y = 20, ALTURA - resposta_altura - 30
    pygame.draw.rect(TELA, (0, 0, 0), (resposta_x, resposta_y, resposta_largura, resposta_altura))
    pygame.draw.rect(TELA, (255, 255, 255), (resposta_x, resposta_y, resposta_largura, resposta_altura), 2)

    # Exibir a resposta digitada
    texto_resposta = font.render(resposta_usuario, True, (255, 255, 255))
    TELA.blit(texto_resposta, (resposta_x + 10, resposta_y + 10))

    # Exibir a instrução para pressionar Enter
    texto_instrucoes = font.render("Pressione Enter para responder", True, (255, 255, 255))
    TELA.blit(texto_instrucoes, (resposta_x + 10, resposta_y + 50))
    # Desenhar o fundo do menu de resposta

#Menu do jogo
def menu_principal():
    rodando = True
    while rodando:
        TELA.fill((0, 0, 0))  # Preencher a tela com preto

        font = pygame.font.Font(None, 74)
        titulo = font.render("Escape Room de Física", True, (255, 255, 255))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 4))

        font = pygame.font.Font(None, 56)
        botao_jogar = font.render("Jogar", True, (255, 255, 255))
        botao_sair = font.render("Sair", True, (255, 255, 255))

        botao_jogar_rect = botao_jogar.get_rect(center=(LARGURA // 2, ALTURA // 2))
        botao_sair_rect = botao_sair.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))

        TELA.blit(botao_jogar, botao_jogar_rect)
        TELA.blit(botao_sair, botao_sair_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar_rect.collidepoint(evento.pos):
                    rodando = False
                elif botao_sair_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()


#Fase 1
def fase_1():
    # Carregar a imagem de fundo
    fundo = pygame.image.load("Imagens\Fisica_Quarto.png")  # Substitua por sua imagem de fundo
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela
    TELA.blit(fundo, (0, 0)) # Desenha a imagem de fundo na tela
    
    # Variaveis
    global contador
    global posicoes_lupas
    global mensagens
    global mensagem_ativa
    global lupa_x, lupa_y
    global texto_contador
    global DURACAO_MENSAGEM
    global resposta_usuario
    global lupa_Iteracao
    gaveta_aberta = False #Estado inicial da gaveta
    mensagem_correta = False  # Estado inicial da mensagem de resposta correta
    porta_aberta = False  # Estado inicial da porta aberta

    posicoes_lupas = {
    "gaveta": (246, 295), 
    "porta": (339, 229), 
    "papel": (199, 453), 
    "estante": (560, 240)}
    mensagens = {
    "gaveta": "A gaveta está trancada. Precisa de um código para abrir", 
    "porta": "É preciso resolver o quebra-cabeça para abrir a porta", 
    "papel": "Tem algo no papel 2μC e 3μC, 0.5m", 
    "estante": "Alguns livros com relação a eletriciadade e magnetismo,talvez tenha algo útil. Forças com sinais opostos se atraem e forças com sinais iguais se repelem"
    }

    # Loop Principal da Fase 1

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            
            # Detectar clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                print(f'Clique do mouse: {evento.pos}')
                mouse_x, mouse_y = evento.pos  # Pega a posição do clique
                if processar_interecao(mouse_x, mouse_y, modo="clique_fora", alvo_x=alvo_x, alvo_y=alvo_y, posicoes_lupas=posicoes_lupas):
                    print("Clique fora da lupa")
                    mensagem_ativa = ""
                    lupa_Iteracao.set_alpha(0)  # Torna a lupa invisível
                    TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                else:
                    # Verifica se o clique foi dentro da imagem da lupa
                    for  local, (alvo_x, alvo_y) in posicoes_lupas.items():
                        if processar_interecao(mouse_x, mouse_y, alvo_x=alvo_x, alvo_y=alvo_y, modo="raio"):
                            #pergunta_ativa = True  # Exibe a pergunta
                            #resposta_usuario = ""  # Limpa a resposta
                            if local in mensagens:
                                mensagem_ativa = mensagens[local]
                                tempos_mensagens[mensagem_ativa] = pygame.time.get_ticks()  # REGISTRA O TEMPO DA MENSAGEM
                                

                            if local == "gaveta" and not gaveta_aberta:
                                print(gaveta_aberta)
                                mensagem_ativa = mensagens["gaveta"]
                            elif local == "porta":
                                mensagem_ativa = mensagens["porta"]
                            elif local == "papel":
                                mensagem_ativa = mensagens["papel"]
                            elif local == "estante":
                                mensagem_ativa = mensagens["estante"]  

            if evento.type == pygame.KEYDOWN and mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
                global resposta_usuario
            if evento.type == pygame.KEYDOWN and  mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:  # Quando pressionar Enter ou Enter do teclado numérico
                    if resposta_usuario == "0.216":  # Verifica se a resposta está correta
                        contador += 1  # Incrementa o contador
                        gaveta_aberta = True; #Gaveta é aberta
                        mensagem_correta = True  # Ativa a exibição de resposta certa 
                        tempo_mensagem = pygame.time.get_ticks()  # Armazena o tempo atual
                        print("Resposta correta!")
                        mensagens["gaveta"] = "O Desafio foi resolvido"
                        mensagem_ativa = ""
                        resposta_usuario = ""
                    #pergunta_ativa = False  # Fecha a janela de pergunta
                    else:
                        mensagem_ativa = "Código incorreto!Você é burro"
                elif evento.key == pygame.K_BACKSPACE:
                    resposta_usuario = resposta_usuario[:-1]  # Apaga um caractere
                elif evento.unicode.isnumeric() or evento.unicode == ".":  # Apenas números e ponto
                    resposta_usuario += evento.unicode  # Adiciona a letra pressionada

            # Obter a posição do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Verificar se o mouse está dentro do raio de interação da lupa
            for alvo_x, alvo_y in posicoes_lupas.values():
                if processar_interecao(mouse_x, mouse_y, alvo_x=alvo_x, alvo_y=alvo_y, modo="raio"):
                    lupa_Iteracao.set_alpha(255)  # Tornar a lupa mais visível
                    lupa_x,lupa_y = alvo_x, alvo_y
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                    lupa_Iteracao.set_alpha(0)  # Manter opacidade baixa
        
        # Desenhar a lupa visìvel
        TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))


        # Se a janela de pergunta estiver ativa, desenhar a caixa de pergunta
        if mensagem_ativa:
            TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
            mostrar_mensagem(mensagem_ativa)
            TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))  # Desenha a lupa visível

            # Exibe se for a gaveta
            if mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
                mostrar_pergunta()

            if mensagem_ativa in tempos_mensagens:
                # Verifica se a mensagem ativa NÃO é a da gaveta
                if mensagem_ativa != mensagens["gaveta"]:
                    if pygame.time.get_ticks() - tempos_mensagens[mensagem_ativa] > DURACAO_MENSAGEM:
                        if mensagem_ativa in tempos_mensagens:  # Verifica se a mensagem ainda existe no dicionário
                            del tempos_mensagens[mensagem_ativa]  # Remove o tempo da mensagem
                        mensagem_ativa = ""  # Para de exibir a mensagem
                        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                        
        #Exibir a mensagem da gaveta aberta
        if mensagem_correta:
            mostrar_mensagem("Gaveta aberta!!")
            mensagem_ativa = ""
            pygame.display.flip()
            sleep(4)
            fase_2()
            mensagens["porta"] = "Agora a porta está aberta"


            if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
                mensagem_correta = False  # Para de exibir a mensagem
        
        # Exibir o contador
        font = pygame.font.Font(None, 36)
        texto_contador = font.render(f"Contador: {contador}", True, (255, 255, 255))
        TELA.blit(texto_contador, (10, 10))


        # Atualizar a tela
        pygame.display.flip()

#Fase 2
def fase_2():
    # Carregar a imagem de fundo
    fundo = pygame.image.load("Imagens\Gaveta.png")  # Substitua por sua imagem de fundo
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela
    TELA.blit(fundo, (0, 0)) # Desenha a imagem de fundo na tela
    
    # Variaveis
    global contador
    global mensagem_ativa
    global lupa_x, lupa_y
    global texto_contador
    global DURACAO_MENSAGEM
    global resposta_usuario
    global lupa_Iteracao
    gaveta_aberta = False #Estado inicial da gaveta
    mensagem_correta = False  # Estado inicial da mensagem de resposta correta

    posicoes_lupas = {"papel": (199, 453),
                      "fio": (542, 260),
                      "bateria":(391, 403)}

    mensagens = {"papel": "Tem algo no papel: r = 0.2m ,I = 10A, u0 = 4pi * 10^-7T*m/A",
                 "fio": "Isso parece ser um circuito improvisado capaz de gerar um campo magnetico",
                 "bateria" : "Qual o campo magnetico?:"}

    # Loop Principal da Fase 2

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                print(f'Clique do mouse: {evento.pos}')
                mouse_x, mouse_y = evento.pos  # Pega a posição do clique
                if processar_interecao(mouse_x, mouse_y, modo="clique_fora", alvo_x=alvo_x, alvo_y=alvo_y, posicoes_lupas=posicoes_lupas):
                    print("Clique fora da lupa")
                    mensagem_ativa = ""
                    lupa_Iteracao.set_alpha(0)  # Torna a lupa invisível
                    TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                else:
                    # Verifica se o clique foi dentro da imagem da lupa
                    for  local, (alvo_x, alvo_y) in posicoes_lupas.items():
                        if processar_interecao(mouse_x, mouse_y, alvo_x=alvo_x, alvo_y=alvo_y, modo="raio"):
                            #pergunta_ativa = True  # Exibe a pergunta
                            #resposta_usuario = ""  # Limpa a resposta
                            if local in mensagens:
                                mensagem_ativa = mensagens[local]
                                tempos_mensagens[mensagem_ativa] = pygame.time.get_ticks()  # REGISTRA O TEMPO DA MENSAGEM
                                

                            if local == "papel" :
                                print(gaveta_aberta)
                                mensagem_ativa = mensagens["papel"]
                            elif local == "fio":
                                mensagem_ativa = mensagens["fio"]
                            elif local == "bateria":
                                mensagem_ativa = mensagens["bateria"]

            if evento.type == pygame.KEYDOWN and mensagem_ativa == mensagens["bateria"]:
                global resposta_usuario
            if evento.type == pygame.KEYDOWN and  mensagem_ativa == mensagens["bateria"] and not gaveta_aberta:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:  # Quando pressionar Enter ou Enter do teclado numérico
                    if resposta_usuario == "0.00001":  # Verifica se a resposta está correta
                        global porta_aberta
                        contador += 1  # Incrementa o contador
                        gaveta_aberta = True; #Gaveta é aberta
                        mensagem_correta = True  # Ativa a exibição de resposta certa 
                        tempo_mensagem = pygame.time.get_ticks()  # Armazena o tempo atual
                        print("Resposta correta!")
                        porta_aberta = True
                        mensagens["bateria"] = "Já foi resolvido"
                        mensagem_ativa = ""
                        resposta_usuario = ""
                    #pergunta_ativa = False  # Fecha a janela de pergunta
                    else:
                        mensagem_ativa = "Código incorreto!Você é burro"
                elif evento.key == pygame.K_BACKSPACE:
                    resposta_usuario = resposta_usuario[:-1]  # Apaga um caractere
                elif evento.unicode.isnumeric() or evento.unicode == ".":  # Apenas números e ponto
                    resposta_usuario += evento.unicode  # Adiciona a letra pressionada
        
           # Obter a posição do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Verificar se o mouse está dentro do raio de interação da lupa
            for alvo_x, alvo_y in posicoes_lupas.values():
                if processar_interecao(mouse_x, mouse_y, alvo_x=alvo_x, alvo_y=alvo_y, modo="raio"):
                    lupa_Iteracao.set_alpha(255)  # Tornar a lupa mais visível
                    lupa_x,lupa_y = alvo_x, alvo_y
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    break
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                    lupa_Iteracao.set_alpha(0)  # Manter opacidade baixa
        
        # Desenhar a lupa visìvel
        TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))

        
        # Se a janela de pergunta estiver ativa, desenhar a caixa de pergunta
        if mensagem_ativa:
            TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
            mostrar_mensagem(mensagem_ativa)
            TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))  # Desenha a lupa visível

            # Exibe se for a gaveta
            if mensagem_ativa == mensagens["bateria"]:
                mostrar_pergunta()

            if mensagem_ativa in tempos_mensagens:
                # Verifica se a mensagem ativa NÃO é a da gaveta
                if mensagem_ativa != mensagens["bateria"]:
                    if pygame.time.get_ticks() - tempos_mensagens[mensagem_ativa] > DURACAO_MENSAGEM:
                        if mensagem_ativa in tempos_mensagens:  # Verifica se a mensagem ainda existe no dicionário
                            del tempos_mensagens[mensagem_ativa]  # Remove o tempo da mensagem
                        mensagem_ativa = ""  # Para de exibir a mensagem
                        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                        
        #Exibir a mensagem da gaveta aberta
        if mensagem_correta:
            mostrar_mensagem("O circuito esta emanando um campo magnetico que abre a porta do quarto")
            pygame.display.flip()
            sleep(4)
            rodando = False


            if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
                mensagem_correta = False  # Para de exibir a mensagem
        
        # Exibir o contador
        font = pygame.font.Font(None, 36)
        texto_contador = font.render(f"Contador: {contador}", True, (255, 255, 255))
        TELA.blit(texto_contador, (10, 10))

        # Atualizar a tela
        pygame.display.flip()  
menu_principal()
fase_1()
#Fase 3

# Finalizar o Pygame
pygame.quit()
sys.exit()
