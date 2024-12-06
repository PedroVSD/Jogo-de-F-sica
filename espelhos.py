import pygame
import math

# Configurações da tela
LARGURA, ALTURA = 800, 600
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Classe para representar espelhos
class Espelho:
    def __init__(self, x, y, angulo=0):
        self.x = x
        self.y = y
        self.angulo = angulo  # Ângulo do espelho em graus

    def girar(self, delta):
        self.angulo += delta
        self.angulo %= 360

    def desenhar(self, tela):
        comprimento = 100  # Comprimento do espelho
        angulo_rad = math.radians(self.angulo)
        x2 = self.x + comprimento * math.cos(angulo_rad)
        y2 = self.y - comprimento * math.sin(angulo_rad)
        pygame.draw.line(tela, AZUL, (self.x, self.y), (x2, y2), 3)

    def calcular_reflexao(self, dx, dy):
        # Calcula a normal do espelho (ângulo perpendicular à superfície)
        angulo_espelho = math.radians(self.angulo)
        normal_x = math.cos(angulo_espelho)
        normal_y = -math.sin(angulo_espelho)

        # Produto escalar para projetar o vetor do raio na normal
        dot = dx * normal_x + dy * normal_y

        # Calcula o vetor refletido
        refletido_x = dx - 2 * dot * normal_x
        refletido_y = dy - 2 * dot * normal_y

        return refletido_x, refletido_y

    def intersecao_com_raio(self, raio_x, raio_y, dx, dy):
        # Verifica onde o raio intersecta com o espelho
        comprimento = 100  # Comprimento do espelho
        angulo_rad = math.radians(self.angulo)
        x2 = self.x + comprimento * math.cos(angulo_rad)
        y2 = self.y - comprimento * math.sin(angulo_rad)
        
        # Cálculo para verificar a interseção do raio com o espelho
        denom = (dy * (x2 - self.x) - dx * (y2 - self.y))
        if denom == 0:
            return False  # Raio paralelo ao espelho, sem interseção
        
        # Fórmulas de interseção
        t = ((raio_x - self.x) * (y2 - self.y) - (raio_y - self.y) * (x2 - self.x)) / denom
        u = ((raio_x - self.x) * dy - (raio_y - self.y) * dx) / denom
        
        if 0 <= t <= 1 and u >= 0:
            return True  # Interseção dentro do espelho
        return False

# Configuração inicial
fonte_luz = (400, 100)  # Posição inicial da fonte de luz
alvo = (400, 500)  # Posição do alvo
espelhos = [
    Espelho(300, 300, 45),  # Primeiro espelho
    Espelho(500, 400, -45)  # Segundo espelho
]

# Função principal
def main():
    rodando = True
    angulo_raio = -math.pi / 1.5  # Ângulo inicial do raio de luz (em radianos, para a direita)

    while rodando:
        tela.fill(PRETO)  # Limpa a tela

        # Processa eventos do jogador
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    espelhos[0].girar(-5)  # Gira o primeiro espelho
                elif evento.key == pygame.K_RIGHT:
                    espelhos[0].girar(5)
                elif evento.key == pygame.K_a:
                    espelhos[1].girar(-5)  # Gira o segundo espelho
                elif evento.key == pygame.K_d:
                    espelhos[1].girar(5)

        # Desenha os elementos na tela
        pygame.draw.circle(tela, VERMELHO, fonte_luz, 5)  # Fonte de luz
        pygame.draw.circle(tela, BRANCO, alvo, 10)  # Alvo
        for espelho in espelhos:
            espelho.desenhar(tela)

        # Simulação do raio de luz
        raio_x, raio_y = fonte_luz  # Ponto inicial do raio
        dx = math.cos(angulo_raio) * 1000  # Direção horizontal do raio
        dy = -math.sin(angulo_raio) * 1000  # Direção vertical do raio
        raio_atingiu_alvo = False

        while True:
            atingiu_espelho = False
            for espelho in espelhos:
                if espelho.intersecao_com_raio(raio_x, raio_y, dx, dy):  # Se o raio atinge o espelho
                    pygame.draw.line(tela, BRANCO, (raio_x, raio_y), (espelho.x, espelho.y), 2)
                    dx, dy = espelho.calcular_reflexao(dx, dy)  # Calcula o novo vetor direção
                    raio_x, raio_y = espelho.x, espelho.y  # Atualiza o ponto inicial do próximo raio
                    atingiu_espelho = True
                    break
            
            # Verifica se atingiu um espelho; caso contrário, desenha até o limite
            if not atingiu_espelho:
                fim_x = raio_x + dx
                fim_y = raio_y + dy
                pygame.draw.line(tela, BRANCO, (raio_x, raio_y), (fim_x, fim_y), 2)
                break

        # Verifica se o raio atingiu o alvo
        if math.sqrt((raio_x - alvo[0]) ** 2 + (raio_y - alvo[1]) ** 2) < 10:
            raio_atingiu_alvo = True
            pygame.draw.line(tela, BRANCO, (raio_x, raio_y), alvo, 2)  # Último segmento até o alvo

        # Exibe mensagem de vitória
        if raio_atingiu_alvo:
            fonte = pygame.font.Font(None, 36)
            texto = fonte.render("Você venceu!", True, BRANCO)
            tela.blit(texto, (LARGURA // 2 - 100, ALTURA // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()