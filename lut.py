import csv

lut = {}  # Look Up Table con las instrucciones y sus codigos en hexadecimal

# Lectura del archivo con las instrucciones
with open("TablaZ80.csv", "r") as archivo_csv:
    lector = csv.reader(archivo_csv, delimiter=";")
    for fila in lector:  # Llenado de la LUT con el contenido de cada fila
        key = fila[0]
        values = fila[1:]
        lut[key] = values
