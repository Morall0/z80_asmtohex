import argparse

__all__ = ["crear_args_parser"]


def crear_args_parser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("nombre_asm", type=str, help="Nombre del archivo ASM.")
    parser.add_argument("-H", "--HEX", type=str, help="(OPCIONAL) Nombre del archivo HEX. Si no se especifica, el nombre del HEX será el mismo que el ASM, con la extensión '.hex'.")
    parser.add_argument("-L", "--LST", type=str, help="(OPCIONAL) Nombre del archivo LST.")

    return parser
