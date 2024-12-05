import pygame
from model.button import Button
from model.constants import *
from model.dic import *


def game_logic(game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if game.game_state == "playing": 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q and game.current_player is None:
                        game.current_player = 1
                        game.show_turn_announcement = True
                        game.announcement_timer = 2 * FPS
                    
                    elif event.key == pygame.K_p and game.current_player is None:
                        game.current_player = 2
                        game.show_turn_announcement = True
                        game.announcement_timer = 2 * FPS    
                    game.click_time = game.current_time 
                if event.type == pygame.MOUSEBUTTONDOWN and game.current_player is not None:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in game.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if game.tries==0:
                                correct = check_answer(game,button.text,game.click_time)
                            else:
                                correct = check_answer(game,button.text,(game.timer)*.40)
                            if not correct:
                                game.tries+=1
                                
                                if game.tries < 2:
                                    
                                    game.current_time = (game.timer)*.75
                                    if game.current_player == 1:
                                        
                                        game.current_player = 2
                                        game.show_turn_announcement = True
                                        game.announcement_timer = 2 * FPS
                                        
                                    else:
                                        game.current_player = 1
                                        game.show_turn_announcement = True
                                        game.announcement_timer = 2 * FPS
                                    break
                            #Verificar si alguien ganó
                            if game.player1_score >= 100 or game.player2_score >= 100 or game.question_cont >= 10:
                                game.game_state = "game_over"
                                if game.player1_score > game.player2_score:
                                    game.winner = 1
                                    game.winnerName = game.player1_name
                                    game.winnerScore = game.player1_score
                                elif game.player2_score > game.player1_score:
                                    game.winner = 2
                                    game.winnerName = game.player2_name
                                    game.winnerScore = game.player2_score
                                else:
                                    game.winner = None
                                    game.winnerName = "EMPATE"
                                    game.winnerScore = 0
                            else:
                                game.select_random_question()
        
def check_answer(self, answer: str,click_time) -> bool:
        """Verifica si la respuesta es correcta"""
        print("comprobando respuesta")
        if self.current_question and answer == self.current_question.correct_answer:
            
            if self.current_player == 1:
                
                if click_time >= (self.timer)*.75:
                    self.player1_score += 14
                elif click_time>(self.timer)*.50 and click_time<(self.timer)*.75:
                    self.player1_score += 12
                else:
                    self.player1_score += 10
            else:
                if click_time >=(self.timer)*.75:
                    self.player2_score += 14
                elif click_time>(self.timer)*.50 and click_time<(self.timer)*.75:
                    self.player2_score += 12
                else:
                    self.player2_score += 10
            show_feedback(self,True)
            return True
        else:
            if click_time >= (self.timer)*.75:
                if self.current_player==1: 
                    self.player1_score-=5 
                else: 
                    self.player2_score-=5
            
        show_feedback(self,False)
        return False

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
        self.selected_questions = []
        self.select_random_question()
                
def draw_turn_announcement(game):
    """Dibuja el anuncio del turno del jugador"""
    info = pygame.display.Info()
    if game.show_turn_announcement and game.current_player:
        font = pygame.font.Font("font/font.ttf", 22)
        player_color = RED if game.current_player == 1 else BLUE
        player_name = game.player1_name if game.current_player == 1 else game.player2_name
        
        text_player = font.render(f"TURNO: {player_name}", True, player_color)
        
        if game.current_player == 1:
            text_rect_player = text_player.get_rect(center=((info.current_w // 2) // 2, info.current_h // 2))
        else:
            text_rect_player = text_player.get_rect(center=((info.current_w // 2) + ((info.current_w // 2)/2), info.current_h // 2))
        
        game.screen.blit(text_player, text_rect_player)
            
        
def show_feedback(self, is_correct: bool):
        """Muestra mensaje de retroalimentación"""
        font = pygame.font.Font("font/font.ttf", 22)
        self.feedback_message = "¡Correcto!" if is_correct else "Incorrecto" 
        self.feedback_color = GREEN if is_correct else RED
        self.feedback_timer = 0.5* FPS  # Mostrar por 2 segundos