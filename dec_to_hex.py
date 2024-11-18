__all__ = ["convert_dtoh"]

# Diccionario que permite convertir fácilmente los bloques binarios
DEC_TO_HEX_MAP = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "A",
    11: "B",
    12: "C",
    13: "D",
    14: "E",
    15: "F"
}

# Funcion que convierte de decimal a hexadecimal
def convert_dtoh(number):
    number = int(number)

    print(number)
    if number < 0:
        number *= -1
        aux = ''
        while (number / 10) != 0:
            aux = str(10 - number % 10) + aux
            number = number // 10

        number = int(aux) + 1

    print(number)
    converted = '' 
    while (number / 16) != 0:
        converted = DEC_TO_HEX_MAP[number % 16] + converted
        number = number // 16

    return converted

print(convert_dtoh(-16))