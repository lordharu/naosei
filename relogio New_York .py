import pygame
import pytz
from datetime import datetime, timedelta
import calendar

# Inicializar Pygame
pygame.init()

# Configurações da janela
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hora Atual em Nova York e Calendário")

# Configurações de fonte
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
font_calendar = pygame.font.Font(None, 28)

# Configurações de cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Obter o fuso horário de Nova York
ny_tz = pytz.timezone('America/New_York')

# Função para obter a hora atual em Nova York
def get_current_time_ny():
    now_utc = datetime.now(pytz.utc)
    now_ny = now_utc.astimezone(ny_tz)
    return now_ny

# Função para desenhar a hora na janela
def draw_time(window, time_str):
    text = font.render("Hora Atual em Nova York:", True, black)
    time_text = font.render(time_str, True, black)
    instruction_text = font_small.render("Pressione 'A' para adicionar 5 dias", True, black)
    window.blit(text, (20, 20))
    window.blit(time_text, (20, 70))
    window.blit(instruction_text, (20, 150))

# Função para adicionar 5 dias à data atual
def add_five_days(current_time):
    return current_time + timedelta(days=5)

# Função para desenhar o calendário na janela
def draw_calendar(window, current_time, special_days, display_month):
    cal = calendar.Calendar()
    year = display_month.year
    month = display_month.month
    days = cal.monthdayscalendar(year, month)
    month_name = calendar.month_name[month]

    # Título do calendário
    calendar_title = font.render(f"{month_name} {year}", True, black)
    window.blit(calendar_title, (20, 200))

    # Nomes dos dias da semana
    days_of_week = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    for i, day in enumerate(days_of_week):
        day_text = font_calendar.render(day, True, black)
        window.blit(day_text, (20 + i * 100, 250))

    # Dias do mês
    for row, week in enumerate(days):
        for col, day in enumerate(week):
            if day != 0:
                day_color = red if (year, month, day) in special_days else black
                day_text = font_calendar.render(str(day), True, day_color)
                text_rect = day_text.get_rect(topleft=(20 + col * 100, 300 + row * 50))
                window.blit(day_text, text_rect)
                # Destacar o dia atual com um retângulo azul
                if (year, month, day) == (current_time.year, current_time.month, current_time.day):
                    pygame.draw.rect(window, blue, text_rect.inflate(10, 10), 2)

    # Desenhar setas de navegação
    pygame.draw.polygon(window, black, [(380, 200), (400, 220), (380, 240)])  # Próximo mês (direita)
    pygame.draw.polygon(window, black, [(420, 200), (400, 220), (420, 240)])  # Mês anterior (esquerda)

# Função para verificar se há uma data especial hoje e retornar o nome do evento
def check_special_day(current_time, special_days):
    key = (current_time.year, current_time.month, current_time.day)
    return special_days.get(key, None)

# Definir dias especiais (ano, mês, dia) com nomes dos eventos
special_days = {
    (2024, 6, 10): "Aniversário do João",
    (2024, 6, 15): "Festa Junina",
    (2024, 6, 20): "Reunião de Trabalho"
}

# Loop principal
running = True
current_time = get_current_time_ny()  # Inicializar current_time fora do loop
display_month = current_time.replace(day=1)  # Começar exibindo o mês atual
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                current_time = add_five_days(current_time)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Verificar clique nas setas de navegação
            if 380 <= mouse_x <= 400 and 200 <= mouse_y <= 240:
                # Próximo mês
                next_month = display_month + timedelta(days=calendar.monthrange(display_month.year, display_month.month)[1])
                display_month = next_month.replace(day=1)
            elif 400 <= mouse_x <= 420 and 200 <= mouse_y <= 240:
                # Mês anterior
                previous_month = display_month - timedelta(days=1)
                display_month = previous_month.replace(day=1)

    # Desenhar a janela
    window.fill(white)
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    draw_time(window, time_str)
    draw_calendar(window, current_time, special_days, display_month)

    # Checar se hoje é um dia especial
    special_event = check_special_day(current_time, special_days)
    if special_event:
        notification_text = font.render(f"Hoje é um dia especial: {special_event}", True, red)
        window.blit(notification_text, (20, 500))

    pygame.display.flip()

    # Atualizar a cada segundo
    pygame.time.delay(1000)
    # Atualizar current_time com o tempo real em Nova York se não foi adicionado 5 dias
    if not pygame.key.get_pressed()[pygame.K_a]:
        current_time = get_current_time_ny()

pygame.quit()
