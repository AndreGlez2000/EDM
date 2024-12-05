import pygame
import random
import json

from typing import List
from model.constants import *
from model.Question import Question
from ui import *
from model.button import Button
from model.dic import *
from logic import *

class Game:
    
    def __init__(self):
        self.used_questions = []
        pygame.init()
        info = pygame.display.Info()
        music = pygame.mixer.music.load('youtube_viejo.mp3')
        pygame.mixer.music.play(-1)
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w - 80, info.current_h - 80), pygame.FULLSCREEN)
        pygame.display.set_caption("EDM")
        self.clock = pygame.time.Clock()
        
        # Timer
        self.timer = 10 * FPS  
        self.current_time = self.timer
        self.timer_active = False
        
        # Jugadores
        self.player1_name = ""
        self.player2_name = ""
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = None
        self.show_turn_announcement = False
        self.announcement_timer = 0
        
        # Mensaje de retroalimentación
        self.feedback_message = ""
        self.feedback_color = WHITE
        self.feedback_timer = 0
        
        # Cargar preguntas
        self.questions = self.load_questions()
        self.selected_questions = []
        self.current_question = None
        self.question_cont = 0
        self.tries = 0
        self.click_time = 0
        
        # Botones
        self.buttons = []
        
        # Estado del juego
        self.game_state = "menu"
        self.winner = None
        self.winnerName = ""
        self.winnerScore = 0

    def update_buttons(self, options: List[str]):
            """Actualiza los botones con nuevas opciones"""
            info = pygame.display.Info()
            self.buttons = []
            
            button_width = info.current_w / 2
            button_height = 150
            
            respuestas = []
            for i, option in enumerate(options):
                respuestas.append(option)
            
            self.buttons.append(Button(0, info.current_h/2 + 200, button_width, button_height,text=respuestas[0],base_color=PURPLE, hovering_color=RED, font = get_font(13), image = None))
            self.buttons.append(Button(button_width + 5, info.current_h/2 + 200, button_width, button_height,text=respuestas[1],base_color=AQUA, hovering_color=RED, font = get_font(13), image = None))
            self.buttons.append(Button(0, (info.current_h/2 + button_height) + 205, button_width, button_height,text=respuestas[2],base_color=PINK, hovering_color=RED, font = get_font(13), image = None))
            self.buttons.append(Button(button_width + 5, (info.current_h/2 + button_height) + 205, button_width, button_height,text=respuestas[3],base_color=GREEN, hovering_color=RED, font = get_font(13), image = None))
    def visual_update(self):
        self.current_time -= 1
        if self.current_time <= 0:
            if self.question_cont == 10:
                self.game_state = "game_over"
            else:
                self.select_random_question()
        
        # Actualizar tiempo de anuncio
        if self.show_turn_announcement:
            self.announcement_timer -= 1
            if self.announcement_timer <= 0:
                self.show_turn_announcement = False
        
        # Actualizar timer de feedback
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        #print(self.current_player)
    def load_questions(self) -> List[Question]:
        """Carga las preguntas desde un archivo JSON"""
        questions = []
        try:
            with open('model/questions.JSON', 'r', encoding='utf-8') as file:
                data = json.load(file)
                for q in data['questions']:
                    questions.append(Question(
                        q['question'],
                        q['image_path'],
                        q['options'],
                        q['correct_answer'],
                        q['category']
                    ))
        except FileNotFoundError:
            print("Archivo de preguntas no encontrado")
        return questions

    def select_random_question(self):
        """Selecciona una pregunta aleatoria"""
        self.tries = 0
        self.question_cont += 1
        if self.questions:
            available_questions = [q for q in self.questions if q not in self.used_questions]
            if not available_questions:
                print("No hay más preguntas disponibles")
                return
            self.current_question = random.choice(available_questions)
            self.used_questions.append(self.current_question)
            self.update_buttons(self.current_question.options)
            self.current_time = self.timer
            self.current_player = None
            self.show_turn_announcement = False
            self.timer_active = False

            # Redimensionar la imagen de la pregunta
            screen_width, screen_height = self.screen.get_size()
            image_path = self.current_question.image_path
            question_image = pygame.image.load(image_path)
            question_image = pygame.transform.scale(question_image, (screen_width // 4, screen_height // 3))
            self.current_question.image = question_image

    def reset_game(self):
        """Reinicia el juego"""
        global jugadores
        if self.winner != None:
            datos_jugador = {"Posicion": len(jugadores), "Nombre": self.winnerName, "Puntaje": self.winnerScore}
            jugadores.append(datos_jugador)
            
            # Reordenar la lista de jugadores basada en el puntaje en orden descendente
            jugadores = sorted(jugadores, key=lambda x: int(x["Puntaje"]), reverse=True)
            
            #Actualizar posiciones de los jugadores ya ordenados del 1 a ...
            for pos, jugador in enumerate(jugadores,start=1):
                jugador["Posicion"] = pos 

            # Guardar los datos del jugador
            print("guardando")
            print(jugadores) 
            guardar_datos(jugadores)
        
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = None
        self.game_state = "playing"
        self.winner = None
        self.question_cont = 0
        self.current_question = None
        self.selected_questions = []  # Reiniciar la lista de preguntas seleccionadas

    def run(self):
        """Loop principal del juego"""
        
        while True:
            
            if self.game_state == "menu":
                draw_menu(self)
            elif self.game_state == "puntaje":
                draw_puntaje(self)
            elif self.game_state == "playing_input":
                self.player1_name, self.player2_name = get_players_name(self)
                self.game_state="playing"           
            elif self.game_state == "playing":
                while self.game_state == "playing":
                    self.clock.tick(FPS)
                    draw(self)
                    self.visual_update()
                    game_logic(self)
            elif self.game_state == "game_over":
                draw_game_over(self)

            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

def draw(game):
    """Dibuja todos los elementos en pantalla"""
    info = pygame.display.Info()
    # Fondo
    draw_background(game)
    pygame.display.set_caption("Exploradores del mundo")
    # Barra superior
    pygame.draw.rect(game.screen, ORANGE, (0, 0, info.current_w, 60))
    # Timer bar
    timer_width = (game.current_time / game.timer) * info.current_w
    pygame.draw.rect(game.screen, PURPLE2, (0, 70, timer_width, 10))
    
    # Puntuaciones
    font = get_font(20)
    
    dibujar_texto(game, f"Jugador 1:", 17, 120, 30, color=player_color_score)
    dibujar_texto(game, f"Jugador 2:", 17, info.current_w - 140, 30, color=player_color_score)
    dibujar_texto(game, f"{game.player1_score}", 17, 220, 30, color=RED)
    dibujar_texto(game, f"{game.player2_score}", 17, info.current_w - 40, 30, color=BLUE)
    
    if game.current_question:
        # Pregunta (size, color, posicion)
        question_font = get_font(30)
        question_text = question_font.render(game.current_question.question, True, YELLOW)
        question_rect = question_text.get_rect(center=(info.current_w // 2, 120))
        game.screen.blit(question_text, question_rect)
        
        # Imagen
        image_rect = game.current_question.image.get_rect(center=(info.current_w // 2, 400))
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
        feedback_rect = feedback_text.get_rect(center=(info.current_w // 2, 400))
        game.screen.blit(feedback_text, feedback_rect)
    
    # Anuncio de turno
    if game.show_turn_announcement:
        draw_turn_announcement(game)
    
    pygame.display.flip()