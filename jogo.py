#teste
import pygame
import sys
import math
import os
import sys
from time import sleep


# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 634, 634  # Tamanho da tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Escape Room de Física")  # Título da janela


# Carregar a imagem da lupa
if getattr(sys, 'frozen', False):
    basepath = sys._MEIPASS
else:
    basepath = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(basepath, 'Imagens\\lupa.png')
lupa_Iteracao = pygame.image.load(file_path)  # Substitua por sua imagem
#lupa_Iteracao = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\lupa.png")  # Substitua por sua imagem
lupa_Iteracao = pygame.transform.scale(lupa_Iteracao, (25, 25))  # Redimensiona para 25x25 pixels
lupa_Iteracao.set_alpha(0)  # 0 é totalmente transparente inicialmente

# Posições para as lupas usando um dicionário


tempos_mensagens = {}

#Mensagens associadas

#Carrega a musica
if getattr(sys, 'frozen', False):
    basepath = sys._MEIPASS
else:
    basepath = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(basepath, 'Musica\\Musica_jogo.mp3')
pygame.mixer.music.load(file_path)
#pygame.mixer.music.load("D:\Cursos\Projetos\Jogo-de-F-sica\Musica\Musica_jogo.mp3")
pygame.mixer.music.play(-1)  # Toca a música em loop infinito

#Variaveis do jogo

cursor_ativo = False
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
def mostrar_mensagem(mensagem, menu_largura=None, menu_altura=None ,menu_x=None, menu_y=None, cor_borda=(255, 255, 255), cor_fundo=(0, 0, 0), cor_texto=(255, 255, 255), x_onset = 10, y_onset = 0):
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
    if menu_largura is None or menu_altura is None:
        menu_largura, menu_altura = LARGURA - 40, len(linhas) * font.get_linesize() + 20
    if menu_x is None or menu_y is None:
        menu_x, menu_y = 20, ALTURA - menu_altura - 100
    pygame.draw.rect(TELA, cor_fundo, (menu_x, menu_y, menu_largura, menu_altura))
    pygame.draw.rect(TELA, cor_borda, (menu_x, menu_y, menu_largura, menu_altura), 2)
    y_offset = menu_y + 10
    for linha in linhas:
        texto_mensagem = font.render(linha, True, cor_texto)
        TELA.blit(texto_mensagem, (menu_x + x_onset, y_offset + y_onset))
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

# Função exclusiva do circuito
def resolver_Circuito():
    # Configuração inicial do minigame
    resistores_disponiveis = [2, 6, 8]
    resistores_escolhidos = []
    configuracao = None
    resultado = ""
    fase = 1
    sucesso = False
    # Salvar a tela atual em uma variável
    tela_atual = TELA.copy()
    # Loop principal do minigame
    while True:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Pressione R para sair
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                return False

            # Lógica para fase 1: Seleção de resistores
            if fase == 1:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    print("Clique do mouse:", evento.pos)
                    btts_resistores = [(165, 225), (315, 225), (465, 223)]
                    mouse_x, mouse_y = evento.pos
                    # botões dos resistores (140, 225) (288, 226) (445, 224)
                    for x, y in btts_resistores:
                        if processar_interecao(mouse_x, mouse_y, alvo_x=x, alvo_y=y, modo="raio", raio=38):
                            if len(resistores_escolhidos) < 4:
                                r = resistores_disponiveis[btts_resistores.index((x, y))]
                                resistores_escolhidos.append(r)

            # Avançar para a próxima fase
            if len(resistores_escolhidos) == 4 and fase == 1:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    fase = 2

            # Escolher configuração
            elif fase == 2:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    print("Clique do mouse:", evento.pos)
                    btts_configuracao = [(245, 245), (415, 224)]
                    mouse_x, mouse_y = evento.pos
                    if processar_interecao(mouse_x, mouse_y, alvo_x=250, alvo_y=245, modo="raio", raio=50):
                        configuracao = "série"
                        fase = 3
                    elif processar_interecao(mouse_x, mouse_y, alvo_x=416, alvo_y=245, modo="raio", raio=50):
                        configuracao = "paralelo"
                        fase = 3

        # Fase 1: Seleção de resistores
        if fase == 1:
            TELA.fill((255, 255, 255))  # Preenche a tela com a cor branca
            TELA.blit(tela_atual, (0, 0))  # Restaura a tela anterior
            mostrar_mensagem("Escolha 4 resistores:", menu_largura=250, menu_altura=50, menu_x=(LARGURA - 250) // 2, menu_y=50)
            for i, r in enumerate(resistores_disponiveis):
                mostrar_mensagem(f"{r} Ω", menu_largura=75, menu_altura=50, menu_x=(LARGURA - 75) // 2 + (i - len(resistores_disponiveis) // 2) * 150, menu_y=200)
            mostrar_mensagem(f"Escolhidos: {resistores_escolhidos}", menu_largura=300, menu_altura=50, menu_x=(LARGURA - 300) // 2, menu_y=350, cor_borda=(0, 0, 0), cor_fundo=(255, 255, 255), cor_texto=(0, 0, 0))
            mostrar_mensagem("Pressione Enter para continuar", menu_largura=400, menu_altura=50, menu_x=(LARGURA - 400) // 2, menu_y=400, cor_borda=(0, 0, 0), cor_fundo=(255, 255, 255), cor_texto=(0, 0, 0))
        # Fase 2: Escolha de configuração
        elif fase == 2:
            TELA.fill((255, 255, 255))  # Preenche a tela com a cor branca
            TELA.blit(tela_atual, (0, 0))  # Restaura a tela anterior
            mostrar_mensagem("Escolha a configuração dos resistores:", menu_largura=400, menu_altura=50, menu_x=(LARGURA - 400) // 2, menu_y=50)
            mostrar_mensagem("Série", menu_largura=100, menu_altura=100, menu_x=200, menu_y=200, x_onset=23, y_onset= 28)
            mostrar_mensagem("Paralelo", menu_largura=100, menu_altura=100, menu_x=(LARGURA // 2) + 50, menu_y=200, x_onset=8, y_onset= 28)

        # Fase 3: Resultado
        elif fase == 3:
            TELA.fill((255, 255, 255))  # Preenche a tela com a cor branca
            TELA.blit(tela_atual, (0, 0))  # Restaura a tela anterior
            if configuracao == "série":
                resistencia_total = sum(resistores_escolhidos)
            elif configuracao == "paralelo":
                resistencia_total = 1 / sum(1 / r for r in resistores_escolhidos)
            else:
                raise ValueError("Configuração inválida")

            corrente = 12 / resistencia_total  # Considerando uma tensão de 12V
            if corrente == 8:
                sucesso = True
                resultado = "Parabéns! A corrente é 8A. A porta foi destrancada!"
            else:
                resultado = f"Corrente: {corrente}A. Tente novamente."
            mostrar_mensagem(resultado, menu_largura=550, menu_altura=100, menu_x=(LARGURA - 550) // 2, menu_y=(ALTURA - 100) // 2 - 50, cor_borda=(0, 0, 0), cor_fundo=(255, 255, 255), cor_texto=(0, 0, 0))
            if not sucesso:
                mostrar_mensagem("Pressione R para sair.", menu_largura=550, menu_altura=50, menu_x=(LARGURA - 550) // 2, menu_y=(ALTURA - 50) // 2 + 50, cor_borda=(0, 0, 0), cor_fundo=(255, 255, 255), cor_texto=(0, 0, 0))

            pygame.display.flip()
            pygame.time.delay(5000) # Aguarda 5 segundos
            print("Fim do minigame")
            if sucesso:
                return sucesso

        pygame.display.flip()

#Menu do jogo
def menu_principal():
    #Carregar a imagem de fundo
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Menu.png")  # Substitua por sua imagem de fundo
    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(basepath, 'Imagens\\Menu.png')
    
    fundo = pygame.image.load(file_path)  # Substitua por sua imagem de fundo
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela
    TELA.blit(fundo, (0, 0)) # Desenha a imagem de fundo na tela

    global cursor_ativo

    rodando = True
    while rodando:
        font = pygame.font.Font(None, 74)
        titulo = font.render("Escape Room de Física", True, (255, 255, 255))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 4))


        #botao_jogar_rect = botao_jogar.get_rect(center=(LARGURA // 2, (ALTURA // 2) -50))
        #botao_sair_rect = botao_sair.get_rect(center=(LARGURA // 2, (ALTURA // 2) + 10))


        # Verificar o clique do mouse
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                print(f'Clique do mouse: {evento.pos}')
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if processar_interecao(mouse_x, mouse_y, alvo_x=328, alvo_y=285, modo="raio", raio=45):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    fase_1()
                    pygame.quit()
                    sys.exit()
       

        pygame.display.flip()


#Fase 1 QUARTO
def fase_1():
    #começa a contar o tempo


    # Carregar a imagem de fundo
    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(basepath, 'Imagens\\Fisica_Quarto.png')

    fundo = pygame.image.load(file_path)
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Fisica_Quarto.png")  # Substitua por sua imagem de fundo
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
    "papel": "Tem algumas anotações no papel: 2μC e 3μC, 0.5m", 
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
                if processar_interecao(mouse_x, mouse_y, modo="clique_fora", alvo_x=alvo_x, alvo_y=alvo_y, posicoes_lupas=posicoes_lupas) and mensagem_ativa != mensagens["gaveta"] and not porta_aberta:
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
                        mensagem_ativa = ""
                        resposta_usuario = ""
                    #pergunta_ativa = False  # Fecha a janela de pergunta
                    else:
                        mensagem_ativa = "Código incorreto!"
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
            if mensagem_ativa == mensagens["porta"] and porta_aberta:
                pygame.display.flip()
                sleep(4)
                fase_3()
                pygame.quit()

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
            sucess = fase_2()
            if sucess:
                mensagens["gaveta"] = "O Desafio foi resolvido"
                porta_aberta = True
                mensagens["porta"] = "Agora a porta está aberta"


            if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
                mensagem_correta = False  # Para de exibir a mensagem


        # Atualizar a tela
        pygame.display.flip()

#Fase 2 GAVETA
def fase_2():
    # Carregar a imagem de fundo
    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(basepath, 'Imagens\\Gaveta.png')

    fundo = pygame.image.load(file_path)  # Substitua por sua imagem de fundo
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Gaveta.png")  # Substitua por sua imagem de fundo
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

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                print(f'Clique do mouse: {evento.pos}')
                mouse_x, mouse_y = evento.pos  # Pega a posição do clique
                if processar_interecao(mouse_x, mouse_y, modo="clique_fora", alvo_x=alvo_x, alvo_y=alvo_y, posicoes_lupas=posicoes_lupas) and mensagem_ativa != mensagens["bateria"]:
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
                        contador += 1  # Incrementa o contador
                        gaveta_aberta = True; #Gaveta é aberta
                        mensagem_correta = True  # Ativa a exibição de resposta certa 
                        tempo_mensagem = pygame.time.get_ticks()  # Armazena o tempo atual
                        print("Resposta correta!")
                        mensagens["bateria"] = "Já foi resolvido"
                        mensagem_ativa = ""
                        resposta_usuario = ""
                    #pergunta_ativa = False  # Fecha a janela de pergunta
                    else:
                        mensagem_ativa = "Código incorreto!"
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
            mostrar_mensagem("O circuito esta emitindo um campo magnetico que abre a porta do quarto")
            pygame.display.flip()
            sleep(4)
            return True


            if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
                mensagem_correta = False  # Para de exibir a mensagem
        


        # Atualizar a tela
        pygame.display.flip()  

#Fase 3 SALA
def fase_3():

    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(basepath, 'Imagens\\Sala3.png')


    # Carregar a imagem de fundo
    fundo = pygame.image.load(file_path)  # Substitua por sua imagem de fundo
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Sala3.png")  # Substitua por sua imagem de fundo
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
    porta_aberta = False #Estado inicial da gaveta
    mensagem_correta = False  # Estado inicial da mensagem de resposta correta
    maleta = False
    
    posicoes_lupas = {"porta": (322, 308),
                      "maleta": (499, 491),
                      "papel":(200, 485),
                      "mesa":(320, 368)}
    
    mensagens = {"porta": "A porta está trancada,e parece estar ligada a um circuito sobre a mesa.",
                "maleta": "A maleta possui uma grande quantidade de resistores, eles são de 4 , 6 e 8 Ohms",
                "papel": "Uma anotação: maior que 7 e menor que 9",
                "mesa": "Um circuito e uma bateria de 12V,mas parece que não temos todos os resistores"}



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
                                

                            if local == "papel" :
                                mensagem_ativa = mensagens["papel"]
                            elif local == "porta":
                                mensagem_ativa = mensagens["porta"]
                            elif local == "mesa":
                                maleta = True
                                mensagem_ativa = mensagens["mesa"]
                            elif local == "maleta" and maleta:
                                mensagem_ativa = mensagens["maleta"]
                                mensagens["mesa"] = "Agora podemos analisar o circuito"


            # Obter a posição do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Verificar se o mouse está dentro do raio de interação da lupa
            if not mensagem_ativa:
                for local, (alvo_x, alvo_y) in posicoes_lupas.items():
                    if processar_interecao(mouse_x, mouse_y, alvo_x=alvo_x, alvo_y=alvo_y, modo="raio"):
                        lupa_Iteracao.set_alpha(255)  # Tornar a lupa mais visível
                        lupa_x, lupa_y = alvo_x, alvo_y
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        break
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                        lupa_Iteracao.set_alpha(0)  # Manter opacidade baixa
            else:
                lupa_Iteracao.set_alpha(0)  # Torna a lupa invisível

        # Desenhar a lupa visìvel
        TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))

        # Se a janela de pergunta estiver ativa, desenhar a caixa de pergunta
        if mensagem_ativa:
            TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
            mostrar_mensagem(mensagem_ativa)
            pygame.display.flip() 

            if maleta and mensagem_ativa == "Agora podemos analisar o circuito" and not porta_aberta:
                sleep(4)
                sucess = fase_4()
                if sucess:
                    porta_aberta = True
                    mensagens["porta"] = "Agora a porta está aberta"
            if porta_aberta and mensagem_ativa == "Agora a porta está aberta":
                sleep(4)
                tela_final()
                pygame.quit()

            if mensagem_ativa in tempos_mensagens:
                # Verifica se a mensagem ativa NÃO é a da gaveta
                if pygame.time.get_ticks() - tempos_mensagens[mensagem_ativa] > DURACAO_MENSAGEM:
                    if mensagem_ativa in tempos_mensagens:  # Verifica se a mensagem ainda existe no dicionário
                        del tempos_mensagens[mensagem_ativa]  # Remove o tempo da mensagem
                    mensagem_ativa = ""  # Para de exibir a mensagem
                    TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela

        # Atualizar a tela
        pygame.display.flip()  

#Fase 4 CIRCUITO
def fase_4():
    # Carregar a imagem de fundo
    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(basepath, 'Imagens\\Circuito.png')

    fundo = pygame.image.load(file_path)  # Substitua por sua imagem de fundo
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Circuito.png")  # Substitua por sua imagem de fundo
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
    
    mensagem_correta = False  # Estado inicial da mensagem de resposta correta
    porta_aberta = False  # Estado inicial da porta aberta


    posicoes_lupas = {
    "circuito": (313, 296),  
    "bateria": (211, 140), 
    "nota": (433, 421)}

    mensagens = {
    "circuito": "O circuito está aberto. Precisa ser fechado para funcionar",
    "bateria": "Uma bateria com um DDP de 12V", 
    "nota": "Devo ligar em paralelo ou em série?"
    }

     # Loop Principal da Fase 1

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            # Detectar clique do mouse direito
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
                return False
      
            
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
                                

                            if local == "nota" :
                                mensagem_ativa = mensagens["nota"]
                            elif local == "bateria":
                                mensagem_ativa = mensagens["bateria"]
                            elif local == "cirtuito":
                                mensagem_ativa = mensagens["circuito"]
                                resolver_Circuito()


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

            # Exibe se for o circuito
            if mensagem_ativa == mensagens["circuito"]:
                sucess = resolver_Circuito()
                mensagem_ativa = ""
                if sucess:
                    return True


            if mensagem_ativa in tempos_mensagens:
                # Verifica se a mensagem ativa NÃO é a da gaveta
                if mensagem_ativa != mensagens["circuito"]:
                    if pygame.time.get_ticks() - tempos_mensagens[mensagem_ativa] > DURACAO_MENSAGEM:
                        if mensagem_ativa in tempos_mensagens:  # Verifica se a mensagem ainda existe no dicionário
                            del tempos_mensagens[mensagem_ativa]  # Remove o tempo da mensagem
                        mensagem_ativa = ""  # Para de exibir a mensagem
                        TELA.blit(fundo, (0, 0))  # Desenha a imagem de fundo na tela
                        
        #Exibir a mensagem da gaveta aberta
        if mensagem_correta:
            mostrar_mensagem("Circuito resolvido!!")
            mensagem_ativa = ""
            pygame.display.flip()
            sleep(4)
            rodando = False

            if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
                mensagem_correta = False  # Para de exibir a mensagem


        # Atualizar a tela
        pygame.display.flip()

# Tela Final
def tela_final():
    # Carregar a imagem de fundo
        # Carregar a imagem de fundo
    if getattr(sys, 'frozen', False):
        basepath = sys._MEIPASS
    else:
        basepath = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(basepath, 'Imagens\\Final.png')

    fundo = pygame.image.load(file_path)  # Substitua por sua imagem de fundo
    #fundo = pygame.image.load("D:\Cursos\Projetos\Jogo-de-F-sica\Imagens\Final.png")  # Substitua por sua imagem de fundo
    fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela
    TELA.blit(fundo, (0, 0)) # Desenha a imagem de fundo na tela

    # Variaveis
    global contador
    global texto_contador

    # Atualizar a tela
    pygame.display.flip()

    # Aguardar 5 segundos
    pygame.time.delay(10000)
    pygame.quit()
    sys.exit()

#inicalizar o Jogo
menu_principal()

# Finalizar o Pygame
pygame.quit()
sys.exit()


