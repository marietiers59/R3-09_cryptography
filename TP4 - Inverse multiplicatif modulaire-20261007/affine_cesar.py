class AffineCesarParams:
    def __init__(self, a: int, b: int):
        self.a, self.b = a, b


def encrypt_single_num(clear_num: int, params: AffineCesarParams):
    return (params.a * clear_num + params.b) % 26


def encrypt_single_char(clear_char: str, params: AffineCesarParams):
    if not (clear_char.isalpha() and clear_char.islower()):
        return clear_char
    lwr_a = 0x61  # ord("a")
    clear_num = ord(clear_char) - lwr_a
    ciph_num = encrypt_single_num(clear_num, params)
    ciph_char = chr(ciph_num + lwr_a)
    return ciph_char


def encrypt(clear_str: str, params: AffineCesarParams):
    """Chiffre les lettres `[a-z]` avec un chiffrement affine (pas les symboles spéciaux, les chiffres ou les lettres `[A-Z]`)."""
    return "".join(encrypt_single_char(clear_char, params) for clear_char in clear_str)
