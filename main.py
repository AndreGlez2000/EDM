import os
from Game import Game
from  model.constants import *
from  model.dic import cargar_datos


quit
def main():
    
    # Verificar que existe el archivo de preguntas
    if not os.path.exists('model/questions.JSON'):
        print("No se encuentra el archivo 'questions.json'. 😭")
        return
    
    # Iniciar el juegoq
    
    game = Game()
    game.run()               

if __name__ == "__main__":

    cargar_datos() 
    main()

