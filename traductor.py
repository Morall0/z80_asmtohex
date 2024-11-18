from lut import lut
from dec_to_hex import convert_dtoh
import re


# Funcion que quita los espacios en blanco y cometarios de la instruccion
def limpa_instruccion(string: str) -> str:
    string = re.sub(r"^\s+", "", string)
    string = re.sub(r"\s+$", "", string)
    string = re.sub(r";.*", "", string)
    return string


# Funcion que retorna si la linea es vacia o es un comentario
def hay_instruccion(linea: str) -> bool:
    no_linea_vacia = re.search(r"^\s+$", linea) is None
    no_linea_coment = re.search(r"^\s*;.*$", linea) is None
    return no_linea_vacia and no_linea_coment


# Lectura del archivo
with open("reloc.asm", "r") as archivo:
    linea = archivo.readline()
    while linea:
        if hay_instruccion(linea):  # Verif no linea vacía o coment
            if linea.find(":") != -1:  # Verifica si hay eti
                linea = re.split(r":", linea)
                eti = linea[0]
                if linea[1][0] != "\n":  # Verif si hay instr después de la eti
                    instruccion = linea[1]
                    instruccion = limpa_instruccion(instruccion)
                    # print(instruccion)
                # TODO: Manejar las referencias (etis)
            else:
                instruccion = limpa_instruccion(linea)

            # Reemplaza los numeros en decimal, por hexa
            numero = re.search(r"\b\d+(?!H)\b", instruccion)
            if numero is not None:
                instruccion = re.sub(r"\b\d+(?!H)\b",  convert_dtoh(numero.group(0))+"H", instruccion)
            print(instruccion)

        linea = archivo.readline()
