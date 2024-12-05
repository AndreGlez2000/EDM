import pygame
from model.button import Button
from model.constants import *
from model.dic import *
from logic import draw_turn_announcement, reset_game

def draw_background(game):
    background_image = pygame.image.load("BG_IMAGES/BG-SP.jpeg")
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    game.screen.blit(background_image, (0, 0))

def draw_menu(game):
    info = pygame.display.Info()

    PLAY_BUTTON = Button((info.current_w / 2) - 50, (info.current_h / 2) - (info.current_h / 5), 100, 150, "JUGAR", base_color="#d7fcd4", hovering_color="GREEN", font=get_font(30), image=None)
    PUNTAJE_BUTTON = Button((info.current_w / 2) - 50, (info.current_h / 2) - (info.current_h / 7), 100, 150, text="PUNTAJES", font=get_font(30), base_color="#d7fcd4", hovering_color="GREEN", image=None)
    QUIT_BUTTON = Button((info.current_w / 2) - 50, (info.current_h / 2) - (info.current_h / 12), 100, 150, text="SALIR", font=get_font(30), base_color="#d7fcd4", hovering_color="GREEN", image=None)
    
    
    draw_background(game)
    
    pygame.display.set_caption("Menu - Exploradores del mundo")
    dibujar_texto(game,"Exploradores del mundo", (info.current_w // 30), (info.current_w / 2), 200)

    if PLAY_BUTTON.checkForInput(game.screen):
        game.game_state = "playing_input"
        game.select_random_question()
    if PUNTAJE_BUTTON.checkForInput(game.screen):
        game.screen.fill(BLACK)
        pygame.display.flip()
        game.game_state = "puntaje"
    if QUIT_BUTTON.checkForInput(game.screen):
        pygame.quit()

def draw_puntaje(game):
    info = pygame.display.Info()

    BACK_BUTTON = Button(100, info.current_h - 100, 50, 100, text="ATRAS", font=get_font(30), base_color="White", hovering_color="Black", image=None)
    draw_background(game)
    pygame.display.set_caption("Puntaje - Exploradores del mundo")
    
    altura = 150
    jugadores_imprimidos = set()
    
    dibujar_texto(game, "PUNTAJE", 30, (info.current_w / 2), 50)
    
    # Convertir puntajes a enteros y ordenar jugadores por puntaje en orden descendente
    jugadores_ordenados = sorted(jugadores, key=lambda x: int(x["Puntaje"]), reverse=True)
    
    for jugador in jugadores_ordenados:
        posicion = jugador["Posicion"]
        nombre = jugador["Nombre"]
        puntaje = jugador["Puntaje"]

        if nombre not in jugadores_imprimidos:
            dibujar_texto(game, "POSICION", 15, (info.current_w / 2) - 200, 100, color="WHITE")
            dibujar_texto(game, "NOMBRE", 15, (info.current_w / 2), 100, color="WHITE")
            dibujar_texto(game, "PUNTOS", 15, (info.current_w / 2) + 200, 100, color="WHITE")
            dibujar_texto(game, f"{posicion}", 15, (info.current_w / 2) - 200, altura)
            dibujar_texto(game, f"{nombre}", 15, info.current_w / 2, altura)
            dibujar_texto(game, f"{puntaje}", 15, (info.current_w / 2) + 200, altura)
            altura += 50
            jugadores_imprimidos.add(nombre)

    if not jugadores_imprimidos:
        dibujar_texto(game, "No hay jugadores", 20, 400, altura, color=RED)

    if BACK_BUTTON.checkForInput(game.screen):
        game.game_state = "menu"

def draw_game_over(game):
    info = pygame.display.Info()

   

    while game.game_state == "game_over":
        draw_background(game)
        dibujar_texto(game,"Partida terminada!", 30, info.current_w /2 , 50)
        if game.winner is not None:
            dibujar_texto(game,f"{game.winnerName} es el GANADOR!!!", 50, info.current_w / 2, 300, color=GREEN)
        else:
            dibujar_texto(game,f"QUEDO EMPATE", 30, info.current_w / 2, 250, color=YELLOW)
        dibujar_texto(game,"tecla SPACIO para volver a menu", 18, info.current_w / 2, 700)


        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    reset_game(game)
                    game.game_state = "menu"
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()

def get_players_name(game):
    info = pygame.display.Info

    player1_name = ""
    player2_name = ""
    input_active = True
    current_player = 1

    while input_active:
        info = pygame.display.Info()
        draw_background(game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if current_player == 1 and player1_name != "":
                        current_player = 2
                    elif current_player == 2 and player2_name != "":
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    if current_player == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                else:
                    if current_player == 1:
                        if len(player1_name) < 10:
                            player1_name += event.unicode
                    else:
                        if len(player2_name) < 10:
                            player2_name += event.unicode

        if current_player == 1:
            dibujar_texto(game,"Nombre de Jugador 1", 30, (info.current_w / 2), 50, color="#C12626")
            dibujar_texto(game,"Ingrese su nombre:", 20, (info.current_w / 2), 200, color=WHITE)
            text_surface = get_font(25).render(player1_name, True, RED)
        else:
            dibujar_texto(game,"Nombre de Jugador 2", 30, (info.current_w / 2), 50, color="#26ADC1")
            dibujar_texto(game,"Ingrese su nombre:", 20, (info.current_w / 2), 200, color=WHITE)
            text_surface = get_font(25).render(player2_name, True, BLUE)

        text_rect = text_surface.get_rect(center=(400, 250))
        game.screen.blit(text_surface, ((info.current_w / 2) - 70, 250))
        pygame.display.flip()

    return player1_name, player2_name

def draw(game):
        """Dibuja todos los elementos en pantalla"""
        info = pygame.display.Info()
        # Fondo
        draw_background(game)
        pygame.display.set_caption("Exploradores del mundo")
        # Barra superior
        pygame.draw.rect(game.screen, "ORANGE", (0, 0, info.current_w, 60))
        #game.dibujar_texto(game,f"{game.current_time}!!!", 30, 420, 100, color =BROWN)
        # Timer bar
        timer_width = (game.current_time / game.timer) * info.current_w
        pygame.draw.rect(game.screen, PURPLE2, (0, 70, timer_width, 10))
        
        
        
        # Puntuaciones
        font = get_font(20)
        
        dibujar_texto(game,f"Jugador 1:", 17, 120, 30, color=player_color_score)
        dibujar_texto(game,f"Jugador 2:", 17, info.current_w - 140, 30, color=player_color_score)
        dibujar_texto(game,f"{game.player1_score}", 17, 220, 30, color=RED)
        dibujar_texto(game,f"{game.player2_score}", 17, info.current_w - 40, 30, color=BLUE)
        #score1 = font.render(f"Jugador 1: {game.player1_score}", True, BLACK)
        #score2 = font.render(f"Jugador 2: {game.player2_score}", True, BLACK)
        #game.screen.blit(score1, (50, 20))
        #game.screen.blit(score2, (WINDOW_WIDTH - 200, 20))
        
        if game.current_question:
            # Pregunta (size, color, posicion)
            question_font = get_font(30)
            question_text = question_font.render(game.current_question.question, True, YELLOW)
            question_rect = question_text.get_rect(center=(info.current_w//2, 120))
            game.screen.blit(question_text, question_rect)
            
            # Imagen
            image_rect = game.current_question.image.get_rect(center=(info.current_w//2, 280))
            game.screen.blit(game.current_question.image, image_rect)
        
        # Botones
        mouse_pos = pygame.mouse.get_pos()
        for button in game.buttons:
            button.update_hover(mouse_pos)
            button.draw(game.screen)
        
        # Mensaje de retroalimentación
        if game.feedback_timer > 0:
            feedback_font = pygame.font.Font(None, 48)
            feedback_text = feedback_font.render(game.feedback_message, True, game.feedback_color)
            feedback_rect = feedback_text.get_rect(center=(info.current_w//2, 400))
            game.screen.blit(feedback_text, feedback_rect)
        
        # Anuncio de turno
        if game.show_turn_announcement:
            draw_turn_announcement(game)
            
    
        
        pygame.display.flip()

def dibujar_texto(game, text, size, x, y, color="#28B1F6"):
    draw = get_font(size).render(str(text), True, color)
    MENU_RECT = draw.get_rect(center=(x,y))
    game.screen.blit(draw, MENU_RECT)

def get_font(size):  # Returns Press-Start-2P in the desired size
    pygame.init()
    return pygame.font.Font("font/font.ttf", size)