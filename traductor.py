from lut import lut
from dec_to_hex import convert_dtoh, comp_a16_HexNumNeg
import re
from args_config import crear_args_parser

TABLA_DE_SIMBOLOS = {}


# Funcion que realiza el checksum de un renglon hex
def checksum(linea_hex):
    bytes_hex = [int(linea_hex[i: i + 2], 16)
                 for i in range(0, len(linea_hex), 2)]
    suma = sum(bytes_hex)
    checksum = (256 - (suma % 256)) % 256
    return f"{checksum:02X}"


# Devuelve una lista con elementos de 16 bytes de las instrucciones traducidas
def split_hex_16Bytes(linea_hex):
    lista_hex = []
    for i in range(0, len(linea_hex), 32):
        lista_hex.append(linea_hex[i: i + 32])

    return lista_hex


# Funcion que genera el archivo.hex con base a la traducción
def genera_hex(linea_hex, nombre_hex, ORG):
    archivoHEX = open(nombre_hex, "w")
    lista_hex = split_hex_16Bytes(linea_hex)
    CL = ORG

    # For que genera el renglon hex de cada 16 bytes de datos
    for datos_hex in lista_hex:
        CL_HEX = rellena(convert_dtoh(CL), 2)
        CL_CODIGOS_HEX = CL_HEX + "00" + datos_hex
        renglon = rellena(convert_dtoh(len(datos_hex) / 2), 1) + CL_CODIGOS_HEX
        CL += len(datos_hex) / 2
        archivoHEX.write(":" + renglon + checksum(renglon) + "\n")

    archivoHEX.write(":00000001FF")  # Escribe el final del archivo
    archivoHEX.close()
    return


# Funcion que quita los espacios en blanco y cometarios de la instruccion
def limpia_instruccion(string: str) -> str:
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
def rellena(num: str, tam_bytes: int) -> str:
    if num.find("-") != -1:
        num = re.sub(r"-", "", num)
        char = "F"
    else:
        char = "0"

    while len(num) < tam_bytes * 2:  # Se resta 1 por la 'H'
        num = char + num
    return num


# Verifica que el valor de un número se encuentre dentro de los rangos válidos
def verif_num(num, n_bytes, con_signo=False):
    num = re.sub(r"H", "", num)
    if num.find("-") != -1:
        num = re.sub(r"-", "", num)
        num = int(num, 16)
        if num > (16 ** (2 * n_bytes)) / 2:
            raise ValueError(
                f"Valor fuera del rango permitido (<-{(16**(2*n_bytes)) / 2})"
            )
    else:
        aux = 1
        num = int(num, 16)
        if con_signo:
            aux *= 2

        if num > (16 ** (2 * n_bytes) / aux) - 1:
            raise ValueError(
                f"Valor fuera del rango permitido (>{(
                    16**(2*n_bytes) / aux) - 1})"
            )


# Retorna la clave de la inst. para acceder a su codigo y tamaño en la lut
def obtener_clave(instruccion: str, primeraPasada: bool):
    # Separacion de las instrucciones
    div_inst = instruccion.split(" ")
    instruccion = div_inst[0]
    num_operandos = len(div_inst[1:])
    extendido = False

    div_inst.pop(0)
    valores_op = []
    for index, op in enumerate(div_inst):
        op = re.sub(r",", "", op)
        div_inst[index] = op

        # DIRECTIVA ORG
        if re.match(r"ORG", instruccion):
            div_inst[index] = "NN"

        # Registros
        # (HL) | (IX) | (IY) | (SP)
        elif re.match(r"([A-EHL]|(\((HL|IX|IY|SP)\)))$", op):
            extendido = False

        # Registros pares
        elif re.match(r"(AF|BC|DE|HL|SP|IX|IY)$", op):
            extendido = True

        elif re.match(r"\([0-9A-F]{1,4}H\)$", op):
            valores_op.append(op)
            div_inst[index] = "(NN)"

        # Saltos
        elif re.match(r"NZ|Z|NC|C|PO|PE|P|M", op):
            if re.match(r"JP|CALL|RET", instruccion):
                extendido = True
            elif re.match(r"JR", instruccion) and re.match(r"NZ|Z|NC|C", op):
                extendido = False

        # N o NN
        elif re.match(r"-?0*[0-9A-F]{1,4}H$", op):
            op = re.sub(r"0+(?=[1-9A-F]([0-9A-F]{3}|[0-9A-F]{1}))", "", op)
            if (
                re.match(r"JP|CALL|RET", instruccion) and op.find("-") == -1
            ) or extendido:
                valores_op.append(op)
                verif_num(op, 2)
                div_inst[index] = "NN"
            elif re.match(r"-?[0-9A-F]{1,2}H$", op):
                valores_op.append(op)
                if re.match(r"JR", instruccion):
                    verif_num(op, 1, True)
                    div_inst[index] = "D"
                elif re.match(r"RST", instruccion):
                    div_inst[index] = re.sub(r"8H", "08H", op)
                else:
                    verif_num(op, 1)
                    div_inst[index] = "N"

        # (IX+D) | (IY+D)
        elif re.match(r"\((IX|IY)(\+|\-)[0-9A-F]{1,2}H\)$", op):
            if op.find("IX") != -1:
                div_inst[index] = "(IX+D)"
            else:
                div_inst[index] = "(IY+D)"
            op = re.sub(r"\((IX|IY)(\+|\-)", "", op)
            op = re.sub(r"\)", "", op)
            valores_op.append(op)

        # Etiquetas
        elif re.match(r"\S*\W+\S*|\b\d+\S*\b", op) is None:
            if op in TABLA_DE_SIMBOLOS:
                verif_num(convert_dtoh(TABLA_DE_SIMBOLOS[op]) + "H", 2)
                valores_op.append(op)

            if op in TABLA_DE_SIMBOLOS or primeraPasada:
                if re.match(r"JP|CALL|RET", instruccion):
                    div_inst[index] = "NN"
                elif re.match(r"JR", instruccion):
                    div_inst[index] = "D"

    if num_operandos >= 1:
        instruccion = instruccion + " " + div_inst[0]
    if num_operandos == 2:
        instruccion = instruccion + ", " + div_inst[1]

    return instruccion, valores_op


# Primera pasada (llena la tabla de simbolos)
def primera_pasada(archivoASM, nombre_lst, nombre_hex):
    linea = archivoASM.readline()

    CL = 0
    ORG = 0
    while linea:
        if hay_instruccion(linea):  # Verif no linea vacía o coment
            if linea.find(":") != -1:  # Verifica si hay eti
                linea = re.split(r":", linea)
                eti = limpia_instruccion(linea[0])

                if eti not in TABLA_DE_SIMBOLOS:
                    TABLA_DE_SIMBOLOS[eti] = CL
                else:
                    print("ERROR: Etiqueta definida múltiplemente")
                    return
                instruccion = ""
                if linea[1][0] != "\n":  # Verif si hay instr después de la eti
                    instruccion = linea[1]
                    instruccion = limpia_instruccion(instruccion)

            else:
                instruccion = limpia_instruccion(linea)

            if instruccion != "":
                # Reemplaza los numeros en decimal, por hexa
                numero_dec = re.search(r"\b\d+(?!H)\b", instruccion)
                if numero_dec is not None:
                    numero_hex = convert_dtoh(numero_dec.group(0)) + "H"
                    instruccion = re.sub(
                        r"\b\d+(?!H)\b", numero_hex, instruccion)

                try:
                    clave, _ = obtener_clave(instruccion, True)
                except ValueError as e:
                    print(f"ERROR: {e}")
                    return

                if clave == "ORG NN":
                    ORG = re.search(
                        r"\b[0-9A-F]{1,4}(?=H)", instruccion).group()
                    CL = int(ORG, 16)
                    ORG = CL  # Obteniendo el ORG en decimal

                try:
                    CL = CL + int(lut[clave][1])
                except KeyError:
                    print(f"ERROR: La instrucción '{instruccion}' NO EXISTE")
                    return

        linea = archivoASM.readline()
    archivoASM.seek(0)
    try:
        segunda_pasada(archivoASM, nombre_lst, nombre_hex)
    except ValueError as e:
        print(f"ERROR: {e}")
        return


# Segunda pasada (genera el lst y el hex)
def segunda_pasada(archivoASM, nombre_lst, nombre_hex):
    linea = archivoASM.readline()
    if nombre_lst != "":
        archivoLST = open(nombre_lst, "w")
    CL = 0
    ORG = 0
    linea_hex = ""
    while linea:
        if hay_instruccion(linea):  # Verif no linea vacía o coment
            if linea.find(":") != -1:  # Verifica si hay eti
                instruccion = ""
                # Verif si hay instr después de la eti
                if re.split(r":", linea)[1][0] != "\n":
                    instruccion = re.split(r":", linea)[1]
                    instruccion = limpia_instruccion(instruccion)
                else:
                    linea = "\t\t\t\t" + linea

            else:
                instruccion = limpia_instruccion(linea)

            if instruccion != "":
                # Reemplaza los numeros en decimal, por hexa
                numero_dec = re.search(r"\b\d+(?!H)\b", instruccion)
                if numero_dec is not None:
                    numero_hex = convert_dtoh(numero_dec.group(0)) + "H"
                    instruccion = re.sub(
                        r"\b\d+(?!H)\b", numero_hex, instruccion)

                clave, valores_op = obtener_clave(instruccion, False)

                if clave == "ORG NN":
                    ORG = re.search(
                        r"\b[0-9A-F]{1,4}(?=H)", instruccion).group()
                    CL = int(ORG, 16)
                    ORG = CL  # Obteniendo el ORG en decimal

                # Reemplaza los numeros HEXA negativos por su complemento
                numero_neg = re.search(r"-[0-9A-F]{1,4}(?=H)", instruccion)
                if numero_neg is not None:
                    numero_hex = comp_a16_HexNumNeg(numero_neg.group(0))
                    instruccion = re.sub(
                        r"-[0-9A-F]{1,4}(?=H)", numero_hex, instruccion
                    )

                try:
                    codigo_inst = lut[clave][0]
                    tamano_inst = lut[clave][1]
                except KeyError:
                    print(f"ERROR: La instrucción '{instruccion}' NO EXISTE")
                    return
                for valor in valores_op:
                    if codigo_inst.find("d") != -1:
                        if re.match(r"-?[0-9A-F]{1,2}H", valor) is None:
                            valor = convert_dtoh(
                                str(TABLA_DE_SIMBOLOS[valor] -
                                    CL - int(tamano_inst))
                            )
                            if valor.find("-") != -1:
                                complemento = comp_a16_HexNumNeg(valor)
                                verif_num(complemento, 1, True)
                            else:
                                verif_num(valor, 1, True)
                        else:
                            valor = re.sub(r"H", "", valor)
                        valor = rellena(valor, 1)
                        valor = " " + valor
                        codigo_inst = re.sub(r" d ?", valor, codigo_inst)
                    elif codigo_inst.find("nn") != -1:
                        if (
                            re.match(
                                r"-?[0-9A-F]{1,4}H|\([0-9A-F]{1,4}H\)", valor)
                            is None
                        ):
                            valor = convert_dtoh(TABLA_DE_SIMBOLOS[valor])
                        else:
                            valor = re.sub(r"\(", "", valor)
                            valor = re.sub(r"\)", "", valor)
                            valor = re.sub(r"H", "", valor)
                        valor = rellena(valor, 2)
                        valor = valor[2:4] + " " + valor[0:2]
                        valor = " " + valor
                        codigo_inst = re.sub(r" nn ?", valor, codigo_inst)
                    elif codigo_inst.find("n") != -1:
                        valor = re.sub(r"H", "", valor)
                        valor = rellena(valor, 1)
                        valor = " " + valor
                        codigo_inst = re.sub(r" n ?", valor, codigo_inst)

                codigo_inst = re.sub(
                    r"\s+", "", codigo_inst
                )  # Se eliminan espacios en blanco
                CL_HEX = rellena(convert_dtoh(str(CL)), 2)

                if nombre_lst != "":
                    archivoLST.write(CL_HEX+"\t"+f"{codigo_inst:<8}")

                linea_hex += codigo_inst  # Concatena HEX de las instrucciones

                CL = CL + int(tamano_inst)
        else:
            if nombre_lst != "":
                archivoLST.write("\t\t\t\t")

        if nombre_lst != "":
            archivoLST.write("\t\t"+linea)
        linea = archivoASM.readline()

    if nombre_lst != "":
        archivoLST.close()
    genera_hex(linea_hex, nombre_hex, ORG)


def traduce():
    # Inicializando el parser de los argumentos
    parser = crear_args_parser()

    # Variable que contiene los argumentos dados en terminal
    args = parser.parse_args()
    if args.HEX is not None:
        nombre_hex = args.HEX
    else:
        nombre_lst = re.sub("asm", "lst", args.nombre_asm)
        nombre_hex = re.sub("asm", "hex", args.nombre_asm)

    if args.LST is not None:
        nombre_lst = args.LST
    else:
        nombre_lst = ""

    # Validando la existencia del archivo
    try:
        archivoASM = open(args.nombre_asm, "r")
    except FileNotFoundError:
        print(f"ERROR: El archivo {args.nombre_asm} no fue encontrado")
        return

    primera_pasada(archivoASM, nombre_lst, nombre_hex)
    archivoASM.close()


traduce()  # Traduce :D
