import pygame
import math
import random
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulador de Olas y Burbujas")

# Definir colores para diferentes momentos del día
SKY_DAY = (135, 206, 235)
SKY_SUNSET = (250, 128, 114)
SKY_NIGHT = (25, 25, 112)
OCEAN_DAY = (0, 105, 148)
OCEAN_SUNSET = (72, 61, 139)
OCEAN_NIGHT = (0, 0, 139)
BUTTON_COLOR = (100, 100, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
BLACK = (0, 0, 0)

# Elegir colores iniciales
sky_color = SKY_DAY
ocean_color = OCEAN_DAY

# Parámetros de la onda
wave_amplitude = 20
wave_length = 100
wave_speed = 0.05

# Crear la fuente para el texto del botón
font = pygame.font.Font(None, 36)

# Función para dibujar las olas
def draw_waves(surface, color, amplitude, length, speed, time):
    for y in range(screen_height // 2, screen_height, 10):
        points = []
        for x in range(0, screen_width, 5):
            offset = int(amplitude * math.sin((x / length) + (time * speed)))
            points.append((x, y + offset))
        pygame.draw.lines(surface, color, False, points, 2)

# Función para dibujar el botón
def draw_button(surface, rect, color, hover_color, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect)
    else:
        pygame.draw.rect(surface, color, rect)
    
    # Dibujar el texto en el botón
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Función para la simulación de partículas flotantes
def particles_simulation():
    # Configurar la pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Partículas Flotantes')

    # Colores
    colors = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) for _ in range(100)]

    # Configuración de partículas
    particles = [{'x': random.randint(0, screen_width),
                  'y': random.randint(0, screen_height),
                  'dx': random.uniform(-1, 1),
                  'dy': random.uniform(-1, 1),
                  'color': random.choice(colors)} for _ in range(100)]

    # Reloj para controlar la velocidad de actualización
    clock = pygame.time.Clock()

    # Definir el rectángulo del botón en la pantalla de partículas
    button_rect = pygame.Rect(0, screen_height - 50, screen_width, 50)

    # Bucle principal de la simulación de partículas
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Detectar clics en el botón
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Regresa al estado de las olas

        screen.fill(BLACK)

        for particle in particles:
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), 3)
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']

            # Mantener las partículas dentro de la pantalla
            if particle['x'] < 0 or particle['x'] > screen_width:
                particle['dx'] *= -1
            if particle['y'] < 0 or particle['y'] > screen_height:
                particle['dy'] *= -1

        # Dibujar el botón
        draw_button(screen, button_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "Siguiente")

        pygame.display.flip()
        clock.tick(60)

# Función para la simulación de burbujas flotantes
def bubbles_simulation():
    # Configurar la pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Burbujas Flotantes')

    # Colores
    colors = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)) for _ in range(100)]

    # Configuración de burbujas
    bubbles = [{'x': random.randint(0, screen_width),
                'y': random.randint(0, screen_height),
                'dx': random.uniform(-1, 1),
                'dy': random.uniform(-1, 1),
                'size': random.uniform(10, 30),
                'color': random.choice(colors)} for _ in range(50)]

    # Reloj para controlar la velocidad de actualización
    clock = pygame.time.Clock()

    # Bucle principal de la simulación de burbujas
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        for bubble in bubbles:
            pygame.draw.circle(screen, bubble['color'], (int(bubble['x']), int(bubble['y'])), int(bubble['size']))
            bubble['x'] += bubble['dx']
            bubble['y'] += bubble['dy']
            bubble['size'] += 0.1 * math.sin(pygame.time.get_ticks() / 1000.0)

            # Mantener las burbujas dentro de la pantalla
            if bubble['x'] < 0 or bubble['x'] > screen_width:
                bubble['dx'] *= -1
            if bubble['y'] < 0 or bubble['y'] > screen_height:
                bubble['dy'] *= -1

        pygame.display.flip()
        clock.tick(60)

# Estado actual del programa
current_state = 'waves'
time = 0

# Definir el rectángulo del botón en la pantalla de olas
button_rect = pygame.Rect(0, screen_height - 50, screen_width, 50)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Cambiar colores con las teclas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:  # Día
                sky_color = SKY_DAY
                ocean_color = OCEAN_DAY
            elif event.key == pygame.K_2:  # Atardecer
                sky_color = SKY_SUNSET
                ocean_color = OCEAN_SUNSET
            elif event.key == pygame.K_3:  # Noche
                sky_color = SKY_NIGHT
                ocean_color = OCEAN_NIGHT
        
        # Detectar clics en el botón
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                if current_state == 'waves':
                    current_state = 'particles'
                    particles_simulation()
                elif current_state == 'particles':
                    current_state = 'bubbles'
                    bubbles_simulation()

    if current_state == 'waves':
        # Llenar la pantalla con el color del cielo
        screen.fill(sky_color)
        
        # Dibujar las olas
        draw_waves(screen, ocean_color, wave_amplitude, wave_length, wave_speed, time)
        
        # Dibujar el botón
        draw_button(screen, button_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "Siguiente")
        
        # Actualizar la pantalla
        pygame.display.flip()
        
        # Incrementar el tiempo para animar las olas
        time += 1
        
        # Limitar la velocidad del bucle
        clock.tick(60)
