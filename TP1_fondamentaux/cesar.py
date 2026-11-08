def encrypt(text: bytes, shift: int):
    """Chiffre des données représentant un texte avec le chiffre de César."""
    shift = shift % 26
    return bytes(_ascii_letter_shift(letter, shift) for letter in text)


def decrypt(ciph: bytes, shift: int):
    """Déchiffre des données représentant un texte avec le chiffre de César."""
    return encrypt(ciph, -shift)


def key_to_char(shift: int):
    """Convertit une clé numérique (0-25) en lettre (A-Z)."""
    return chr(ord("A") + (shift % 26))


def char_to_key(shift: str):
    """Convertit une lettre (A-Z) en clé numérique (0-25)."""
    return ord(shift.upper()) - ord("A")


def _ascii_letter_shift(letter: int, shift: int):
    """Décale une lettre ASCII en conservant sa casse. 
    Les autres caractères ne sont pas modifiés."""
    upr_a, upr_z = 0x41, 0x5A  # ord("A"), ord("Z")
    lwr_a, lwr_z = 0x61, 0x7A  # ord("a"), ord("z")
    if upr_a <= letter <= upr_z:
        return (letter - upr_a + shift) % 26 + upr_a
    if lwr_a <= letter <= lwr_z:
        return (letter - lwr_a + shift) % 26 + lwr_a
    return letter
