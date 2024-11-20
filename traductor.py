from lut import lut
from dec_to_hex import convert_dtoh
import re

# TODO: CONFIGURAR ARGUMENTOS

TABLA_DE_SIMBOLOS = {}
#LST=[]
CL = 0


# Funcion que quita los espacios en blanco y cometarios de la instruccion
def limpa_instruccion(string: str) -> str:
    string = re.sub(r"^\s+", "", string)
    string = re.sub(r"\s+$", "", string)
    string = re.sub(r";.*", "", string)

    while re.search(r"(?<=\S)\s{2,}(?=\S)", string) is not None:
        string = re.sub(r"(?<=\S)\s{2,}(?=\S)", " ", string)

    string = re.sub(r"\s,", ",", string)
    string = re.sub(r"(?<=\S),(?=\S)", ", ", string)
    return string


# Funcion que retorna si la linea es vacia o es un comentario
def hay_instruccion(linea: str) -> bool:
    no_linea_vacia = re.search(r"^\s+$", linea) is None
    no_linea_coment = re.search(r"^\s*;.*$", linea) is None
    return no_linea_vacia and no_linea_coment


# Función que retorna un numero HEX rellenado por la izquierda por n ceros
def rellena_ceros(num: str, tam_bytes: int) -> str:
    while len(num)-1 < tam_bytes: # Se resta 1 por la 'H'
        num="0"+num
    return num


# Lectura del archivo
def traduce():
    try:
        archivoASM = open("reloc.asm", "r")
    except FileNotFoundError:
        print("El archivo [ARCHIVO] no fue encontrado")  # TODO: PONER EL NOMBRE DEL ARCHIVO
        return
    linea = archivoASM.readline()
    i=0
    while linea:

        #LST[0]=i
        #LST[3]=linea     

        if hay_instruccion(linea):  # Verif no linea vacía o coment
            if linea.find(":") != -1:  # Verifica si hay eti
                linea = re.split(r":", linea)
                eti = linea[0]

                if eti not in TABLA_DE_SIMBOLOS:
                    TABLA_DE_SIMBOLOS[eti] = convert_dtoh(str(CL))
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
                    numero = convert_dtoh(numero.group(0)) + "H"
                    instruccion = re.sub(r"\b\d+(?!H)\b", numero, instruccion)

                # Separacion de las instrucciones
                div_inst = instruccion.split(" ")
                instruccion = div_inst[0]
                num_operandos = len(div_inst[1:])

                div_inst.pop(0)
                valores_op = []
                for index, op in enumerate(div_inst):
                    op = re.sub(r",", "", op)
                    div_inst[index] = op
                    # Etiquetas
                    if not re.match(r"\S*\W\S*|\b([A-FHL]|d+\S*|(AF|BC|DE|SP|HL|IX|IY)|[A-F]+H)\b", op):
                        if op in TABLA_DE_SIMBOLOS:
                            op = TABLA_DE_SIMBOLOS[op] + "H"

                    # Registros
                    # (HL) | (IX) | (IY) | (SP)
                    if re.match(r"([A-EHL]|(\((HL|IX|IY|SP)\)))$", op):
                        extendido = False

                    # Registros pares
                    elif re.match(r"(AF|BC|DE|HL|SP|IX|IY)$", op):
                        extendido = True

                    elif re.match(r"\([0-9A-F]{1,4}H\)$", op):
                        valores_op.append(op)
                        div_inst[index] = "(NN)"
                        #str(lut[instruccion][2]) 0F nn_
                        #LST[2]=+valores_op

                    #Saltos
                    elif re.match(r"NZ|Z|NC|C|PO|PE|P|M", op): 
                        if re.match(r"JP|CALL|RET", instruccion):
                            extendido = True
                        elif re.match(r"JR", instruccion) and re.match(r"NZ|Z|NC|C", op):
                            extendido = False
                        

                    # N o NN
                    elif re.match(r"-?[0-9A-F]{1,4}H$", op):
                        if (re.match(r"(JP|CALL)", instruccion) and re.match(r"[0-9A-F]{1,4}H$", op)) or extendido:
                            valores_op.append(op)
                            div_inst[index] = "NN"
                        elif re.match(r"-?[0-9A-F]{1,2}H$", op):
                            if re.match(r"JR", instruccion):
                                div_inst[index] = "D"
                            else:
                                valores_op.append(op)
                                div_inst[index] = "N"

                    # (IX+D) | (IY+D)
                    elif re.match(r"\((IX|IY)(\+|\-)[0-9AF]{1,2}H\)$", op):
                        valores_op.append(op)
                        div_inst[index] = "D"

                if num_operandos >= 1:
                    instruccion = instruccion + " " + div_inst[0]
                if num_operandos == 2:
                    instruccion = instruccion + ", " + div_inst[1]

                #ideas chema
                #base=pop de valores_op para recuperar el valor sustituido
                #obtener hex de instruccion con 
                #str(lut[instruccion][1])

                print(lut[instruccion])
                # CL += int(lut[instruccion][1])
                # LST[1]=CL

                #print LST 1, LST2, LST3

                i+=1


                

        linea = archivoASM.readline()

    archivoASM.close()

traduce()