# Diccionario que permite convertir fácilmente los bloques binarios
BIN_TO_HEX_MAP = {
    "0000": "0",
    "0001": "1",
    "0010": "2",
    "0011": "3",
    "0100": "4",
    "0101": "5",
    "0110": "6",
    "0111": "7",
    "1000": "8",
    "1001": "9",
    "1010": "A",
    "1011": "B",
    "1100": "C",
    "1101": "D",
    "1110": "E",
    "1111": "F"
}


# Funcion que retorna una lista de bloques de 4 bits del numero original
def div_bin_digits(number: str) -> str:
    binary_blocks_list = []  # Lista de los bloques de 4 bits
    hex_len = len(number) / 4  # Cantidad de digitos hexadecimales
    hex_int_len = int(hex_len)

    # Separación de la cadena en bloques de 4 bits
    for i in range(1, hex_int_len+1):
        slice_index = i*4
        if i == 1:
            binary_blocks_list.insert(0, number[-slice_index:])
        else:
            binary_blocks_list.insert(0, number[-slice_index:-slice_index+4])

    # Agrega los bloques que no son 4 bits completos
    if hex_len != hex_int_len:
        binary_blocks_list.insert(0, number[:-slice_index])

    return binary_blocks_list


# Funcióń que convierte un numero binario a hexadecimal
def bin_to_hex(number: str) -> str:
    binary_digits = div_bin_digits(number)
    hex_digits = [BIN_TO_HEX_MAP[dig] for dig in binary_digits]
    hex_number = "".join(hex_digits)
    return hex_number
