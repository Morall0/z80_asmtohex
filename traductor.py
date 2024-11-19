from lut import lut
from dec_to_hex import convert_dtoh
import re

TABLA_DE_SIMBOLOS = {}
CL=0


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


# TODO: Funcion que añada ceros

# Lectura del archivo
with open("reloc.asm", "r") as archivo:
    linea = archivo.readline()
    while linea:
        if hay_instruccion(linea):  # Verif no linea vacía o coment
            if linea.find(":") != -1:  # Verifica si hay eti
                linea = re.split(r":", linea)
                eti = linea[0]

                if eti in TABLA_DE_SIMBOLOS is not None:
                    TABLA_DE_SIMBOLOS[eti] = CL
                else:
                    print("Etiqueta definida múltiplemente")
                    break

                instruccion = ""
                if linea[1][0] != "\n":  # Verif si hay instr después de la eti
                    instruccion = linea[1]
                    instruccion = limpa_instruccion(instruccion)

            else:
                instruccion = limpa_instruccion(linea)

            if instruccion != "":
                # Reemplaza los numeros en decimal, por hexa
                numero = re.search(r"\b\d+(?!H)\b", instruccion)
                if numero is not None:
                    numero = convert_dtoh(numero.group(0))+"H"
                    instruccion = re.sub(r"\b\d+(?!H)\b", numero, instruccion)

                # Separacion de las instrucciones
                div_inst = instruccion.split(" ")
                instruccion = div_inst[0]
                num_operandos = len(div_inst[1:])

                if num_operandos == 0:
                    print(instruccion)
                    print(lut[instruccion])

                elif num_operandos == 1:
                    op1 = div_inst[1]

                    # Etiquetas
                    if re.match(r"", op1):
                        if op1 in TABLA_DE_SIMBOLOS:
                            op1 = TABLA_DE_SIMBOLOS

                    # Registros
                    elif re.match(r"[A-EHL]$", op1):
                        print(instruccion+" "+op1)
                        print(lut[instruccion+" "+op1])

                    # Registros pares
                    elif re.match(r"(AF|BC|DE|HL|SP|IX|IY)$", op1):
                        print(instruccion+" "+op1)
                        print(lut[instruccion+" "+op1])

                    # (HL) | (IX) | (IY)
                    elif re.match(r"\((HL|IX|IY)\)", op1):
                        print(instruccion+" "+op1)
                        print(lut[instruccion+" "+op1])

                    # N o NN
                    elif re.match(r"[0-9A-F]{1,4}H", op1):
                        if re.match(r"(JP|CALL)", instruccion):
                            print(instruccion+" "+op1)
                            print(lut[instruccion+" NN"])
                        elif re.match(r"[0-9A-F]{1,2}H", op1):
                            print(instruccion+" "+op1)
                            print(lut[instruccion+" N"])

                    # (IX+D) | (IY+D)
                    elif re.match(r"\((IX|IY)\+[0-9AF]{1,2}H\)", op1):
                        print(instruccion+" "+op1)
                        print(lut[instruccion+" D"])

                    else:
                        print(f"La instruccion '{instruccion} {op1}' no fue encontrada")
                        break

                elif num_operandos == 2:
                    op1 = div_inst[1]
                    op2 = div_inst[2]
                    # print(instruccion, op1, op2)

        linea = archivo.readline()
