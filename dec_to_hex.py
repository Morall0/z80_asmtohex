import re

__all__ = ["convert_dtoh", "comp_a16_HexNumNeg"]

# Diccionario que permite convertir de decimal a hexadecimal
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

# Diccionario que permite convertir fácilmente de hexadecimal a decimal
HEX_TO_DEC_MAP = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15
}


# Funcion que convierte de decimal a hexadecimal
def convert_dtoh(number):
    number = int(number)

    if number == 0:
        return str(0)

    sign = 1
    neg = 0

    if number < 0:
        sign = -1
        number *= sign
        number -= 1
        neg = 15

    converted = ''
    while (number / 16) != 0:
        converted = DEC_TO_HEX_MAP[neg + sign * (number % 16)] + converted
        number = number // 16

    if sign == -1:
        converted = '-' + converted

    return converted


# Funcion que convierte -numHex a comp_a16(-numHex)
def comp_a16_HexNumNeg(number):
    number = re.sub(r"-", "", number)
    length = len(number)

    converted = 0
    for i, c in enumerate(number):
        converted += HEX_TO_DEC_MAP[c]*16**(length - i - 1)

    return convert_dtoh("-" + str(converted))
