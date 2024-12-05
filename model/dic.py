import csv
jugadores = []
players = './BestPlayers.csv'
#funcion para cargar datos del csv
def cargar_datos():
    try:
        #abrir el archivo en modo read
        with open(players, newline='', mode='r') as archivo:
            #en modo diccionario
            dic_read = csv.DictReader(archivo)
            #recorremos las filas
            for fila in dic_read:
                jugador = {
                    "Posicion": fila["Posicion"],
                    "Nombre": fila["Nombre"],
                    "Puntaje": fila["Puntaje"]
                }
                #agregamos el jugador a la lista de jugadores
                jugadores.append(jugador)
    except FileNotFoundError:
        print("El archivo no existe")

#funcion para guardar datos al csv
def guardar_datos(jugadores):
    #abrir el archivo en modo W
    #se abre en modo 'W' y no 'A', pq se modifican las posiciones en 
    #tabla de todos los jugadores, antonces si anexamos el ultimo jugador
    #no se veran modifcadas las posiciones de los jugadores anteriores
    with open('./BestPlayers.csv', mode='w', newline='') as archivo:
        campos = ["Posicion", "Nombre", "Puntaje"]
        #modo diccionario
        dic_write = csv.DictWriter(archivo, fieldnames=campos)
        
        dic_write.writeheader()  # Escribir el encabezado del CSV
        #escribimos los jugadores
        for jugador in jugadores:
            fila = {
                "Posicion": int(jugador["Posicion"]),
                "Nombre": jugador["Nombre"],
                "Puntaje": int(jugador["Puntaje"])
            }
            dic_write.writerow(fila)