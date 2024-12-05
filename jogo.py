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


# Carregar a imagem de fundo
fundo = pygame.image.load("Imagens\Fisica_Quarto.png")  # Substitua por sua imagem de fundo
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))  # Ajusta ao tamanho da tela


# Carregar a imagem da lupa
lupa_Iteracao = pygame.image.load("Imagens\lupa.png")  # Substitua por sua imagem
lupa_Iteracao = pygame.transform.scale(lupa_Iteracao, (25, 25))  # Redimensiona para 25x25 pixels
lupa_Iteracao.set_alpha(0)  # 0 é totalmente transparente inicialmente

# Posições para as lupas usando um dicionário
posicoes_lupas = {
    "gaveta": (246, 295), 
    "porta": (339, 229), 
    "papel": (199, 453), 
    "estante": (560, 240)}

tempos_mensagens = {}

#Mensagens associadas
mensagens = {
    "gaveta": "A gaveta está trancada. Precisa de um código para abrir", 
    "porta": "É preciso resolver o quebra-cabeça para abrir a porta", 
    "papel": "Tem algo no papel 2μC e 3μC, 0.5m", 
    "estante": "Alguns livros com relação a eletriciadade e magnetismo,talvez tenha algo útil. Forças com sinais opostos se atraem e forças com sinais iguais se repelem"
}


#Variaveis do jogo
lupa_x, lupa_y = 0, 0
mensagem_ativa =""
resposta_correta = "0.216"
resposta_usuario = ""
gaveta_aberta = False #Estado inicial da gaveta
mensagem_correta = False #Indica se a mensagem da gaveta aberta esta aberta ou não
contador = 0
mensagem_correta = False  # Indica se a mensagem "Resposta correta!" deve ser exibida
tempo_mensagem = 0        # Temporizador para exibir a mensagem (em milissegundos)
DURACAO_MENSAGEM = 2000   # Tempo de exibição da mensagem (2 segundos)




# FUNÇÕES:

# Função para mostrar mensagem na tela
def mostrar_mensagem(mensagem):
    font = pygame.font.Font(None, 36)
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
def mostrar_pergunta(resposta_usuario):
    font = pygame.font.Font(None, 36)

    texto_resposta = font.render(resposta_usuario, True, (255, 255, 255))
    if mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
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

#Classe de uma Pegunta generico
class Pergunta:
    def __init__(self, pergunta, resposta_correta):
        self.pergunta = pergunta
        self.resposta_correta = resposta_correta

    def verificar_resposta(self, resposta_usuario):
        return resposta_usuario == self.resposta_correta

#Classe para uma fase Generica
class Fase:
    def __init__(self, nome, imagem_fundo, posicoes_lupas, desafios):
        self.nome = nome
        self.imagem_fundo = imagem_fundo
        self.posicoes_lupas = posicoes_lupas
        self.desafios = desafios

    # Função para calcular a distância entre o cursor e o centro da lupa
    def distancia_entre_pontos(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    # Função para verificar se o mouse está dentro do raio de interação
    def esta_no_raio_interacao(mouse_x, mouse_y,alvo_x, alvo_y, raio = 25):
        distancia = Fase.distancia_entre_pontos((mouse_x, mouse_y), (alvo_x, alvo_y))
        return distancia < raio

    # Função para verificar se o clique foi fora de uma área interativa
    def clicou_fora_da_area_interativa(mouse_x, mouse_y):
        # Aqui você pode definir o tamanho da área interativa onde o clique deve ser considerado "fora"
        return not any(Fase.esta_no_raio_interacao(mouse_x, mouse_y, x, y) for x, y in posicoes_lupas.values())

#Criar uma fase
fase1 = Fase("Fase 1", "Imagens\Fisica_Quarto.png", posicoes_lupas, mensagens)

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
            if Fase.clicou_fora_da_area_interativa(mouse_x, mouse_y):
                mensagem_ativa = ""
            else:
                # Verifica se o clique foi dentro da imagem da lupa
                for  local, (alvo_x, alvo_y) in posicoes_lupas.items():
                    if Fase.esta_no_raio_interacao(mouse_x, mouse_y, alvo_x, alvo_y):
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
        #else:

            #if not esta_no_raio_interacao(mouse_x,mouse_y, LARGURA  // 2, ALTURA// 2):
                #mensagem_ativa ="";   

        # Detectar tecla pressionada para digitar a resposta
        if evento.type == pygame.KEYDOWN and  mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
            if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:  # Quando pressionar Enter ou Enter do teclado numérico
                if resposta_usuario == resposta_correta:  # Verifica se a resposta está correta
                    contador += 1  # Incrementa o contador
                    gaveta_aberta = True; #Gaveta é aberta
                    mensagem_correta = True  # Ativa a exibição de resposta certa 
                    tempo_mensagem = pygame.time.get_ticks()  # Armazena o tempo atual
                    print("Resposta correta!")
                    mensagens["gaveta"] = "A gaveta está aberta. Você encontrou uma chave!"
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
        if Fase.esta_no_raio_interacao(mouse_x, mouse_y, alvo_x, alvo_y):
            lupa_Iteracao.set_alpha(255)  # Tornar a lupa mais visível
            lupa_x,lupa_y = alvo_x, alvo_y
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            break

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            lupa_Iteracao.set_alpha(0)  # Manter opacidade baixa

    
    # Verificar se o mouse está dentro do raio de interação da lupa
    #if esta_no_raio_interacao(mouse_x, mouse_y, posicoes_lupas.values()):
     #   TELA.blit(lupa_Iteracao, (mouse_x, mouse_y))  # Desenhar a lupa na posição do mouse))
      #  lupa_Iteracao.set_alpha(255)  # Tornar a lupa mais visível
    #else:
     #   lupa_Iteracao.set_alpha(0)  # Manter opacidade baixa

    # Desenhar o fundo (estático)
    TELA.blit(fundo, (0, 0))

    # Desenhar a lupa visìvel
    TELA.blit(lupa_Iteracao, (lupa_x, lupa_y))


    # Se a janela de pergunta estiver ativa, desenhar a caixa de pergunta
    if mensagem_ativa:
        mostrar_mensagem(mensagem_ativa)

        # Exibe se for a gaveta
        if mensagem_ativa == mensagens["gaveta"] and not gaveta_aberta:
            mostrar_pergunta(resposta_usuario)

        if mensagem_ativa in tempos_mensagens:
            # Verifica se a mensagem ativa NÃO é a da gaveta
            if mensagem_ativa != mensagens["gaveta"]:
                if pygame.time.get_ticks() - tempos_mensagens[mensagem_ativa] > DURACAO_MENSAGEM:
                    if mensagem_ativa in tempos_mensagens:  # Verifica se a mensagem ainda existe no dicionário
                        del tempos_mensagens[mensagem_ativa]  # Remove o tempo da mensagem
                    mensagem_ativa = ""  # Para de exibir a mensagem

        # Exibe a instrução para pressionar Enter
        #texto_instrucoes = font.render("Pressione Enter para responder", True, (255, 255, 255))
        #TELA.blit(texto_instrucoes, (LARGURA // 4, ALTURA // 1.5))
    
    #Exibir a mensagem da gaveta aberta
    if mensagem_correta:
        font = pygame.font.Font(None, 36)
        texto_sucesso = font.render("Gaveta aberta!Boa animal", True, (0, 255, 0))
        TELA.blit(texto_sucesso, (LARGURA // 4, ALTURA // 1.5))

        if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
            mensagem_correta = False  # Para de exibir a mensagem
    
    # Exibir o contador
    font = pygame.font.Font(None, 36)
    texto_contador = font.render(f"Contador: {contador}", True, (255, 255, 255))
    TELA.blit(texto_contador, (10, 10))

    #if mensagem_correta:
     #   font = pygame.font.Font(None, 36)
      #  texto_mensagem = font.render("Resposta correta!", True, (0, 255, 0))  # Texto em verde
       # TELA.blit(texto_mensagem, (10, 50))  # Desenha abaixo do contador

        # Verifica se o tempo de exibição já passou
        #if pygame.time.get_ticks() - tempo_mensagem > DURACAO_MENSAGEM:
         #   mensagem_correta = False  # Para de exibir a mensagem

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()
sys.exit()
