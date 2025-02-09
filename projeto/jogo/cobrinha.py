import pygame
import serial
import random

# Inicializa o pygame
pygame.init()

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define o tamanho da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480

# Define o tamanho do bloco
BLOCK_SIZE = 20

# Inicializa a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

# Inicializa a serial
ser = serial.Serial("/dev/ttyACM0", 115200)

# Inicializa as variáveis do jogo
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
snake_direction = "RIGHT"
food = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)


# Função para desenhar a cobrinha
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))


# Função para desenhar a comida
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))


# Função para mover a cobrinha
def move_snake(snake, direction):
    head = snake[-1]

    if direction == "RIGHT":
        new_head = (head[0] + BLOCK_SIZE, head[1])
    elif direction == "LEFT":
        new_head = (head[0] - BLOCK_SIZE, head[1])
    elif direction == "UP":
        new_head = (head[0], head[1] - BLOCK_SIZE)
    elif direction == "DOWN":
        new_head = (head[0], head[1] + BLOCK_SIZE)
    snake.append(new_head)
    snake.pop(0)


# Função para verificar se a cobrinha bateu na parede ou em si mesma
def check_collision(snake):
    head = snake[-1]
    if (
        head[0] < 0
        or head[0] >= SCREEN_WIDTH
        or head[1] < 0
        or head[1] >= SCREEN_HEIGHT
    ):
        return True
    if head in snake[:-1]:
        return True
    return False


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lê os dados da serial
    line = ser.readline().decode("utf-8").rstrip()
    vry, vrx = map(int, line.split(","))

    # Define a direção da cobrinha
    if vrx > 3000:
        snake_direction = "RIGHT"
    elif vrx < 1000:
        snake_direction = "LEFT"
    elif vry > 3000:
        snake_direction = "UP"
    elif vry < 1000:
        snake_direction = "DOWN"

    # Move a cobrinha
    move_snake(snake, snake_direction)

    # Verifica se a cobrinha bateu na parede ou em si mesma
    if check_collision(snake):
        print("bateu")
        running = False

    # Verifica se a cobrinha comeu a comida
    head = snake[-1]
    food_rect = pygame.Rect(
        food[0], food[1], BLOCK_SIZE, BLOCK_SIZE
    )  # Cria um rect para a comida
    head_rect = pygame.Rect(
        head[0], head[1], BLOCK_SIZE, BLOCK_SIZE
    )  # Cria um rect para a cabeça da cobra

    if head_rect.colliderect(food_rect):  # Usa colliderect para verificar a colisão
        food = (
            random.randrange(0, SCREEN_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, SCREEN_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE,
        )
        snake.insert(0, snake[0])  # Aumenta a cobra

    # Desenha o fundo
    screen.fill(BLACK)

    # Desenha a cobrinha
    draw_snake(snake)

    # Desenha a comida
    draw_food(food)

    # Atualiza a tela
    pygame.display.flip()

# Finaliza o pygame
pygame.quit()

# Fecha a serial
ser.close()
