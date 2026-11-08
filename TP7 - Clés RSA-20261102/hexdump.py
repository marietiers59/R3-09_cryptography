"""Affichage "propre" de données dans une liste d'octets."""


def hexdump(data: bytes) -> str:
    """Affichage "propre" des données dans une liste d'octets."""
    hexes = [f"{b:02x}" for b in data]
    hexes += ["  "] * (15 - (len(data) + 15) % 16)  # padding pour faire des lignes de 16

    # groupe par 5, puis par 2 pour faire des lignes de 10
    hexes = [" ".join(hexes[i : i + 8]).ljust(3 * 8 - 1) for i in range(0, len(hexes), 8)]
    hexes = ["  ".join(hexes[i : i + 2]) for i in range(0, len(hexes), 2)]

    # caractères ASCII (imprimables ou .)
    chars = [chr(b) if len(str(bytes([b]))) == 4 else "." for b in data]
    chars += [" "] * (15 - (len(data) + 15) % 16)
    chars = ["".join(chars[i : i + 16]) for i in range(0, len(data), 16)]

    # numéros de ligne
    len_count = max(4, len(str(len(hexes))))
    line_counts = [str(i * 10).rjust(len_count, "0") for i in range(len(hexes))]

    # dump final
    lines = [f"{lc} - {h}   {c}" for lc, h, c in zip(line_counts, hexes, chars)]
    print("\n".join(lines))
    # return lines
