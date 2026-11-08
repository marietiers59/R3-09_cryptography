from base64 import b64encode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def main():
    key = b"ALL THEM WITCHES"
    aad = None
    nonce = b"KNOWER 4EVER"

    # fichier de données en clair non partagées
    with open("aesgcm-data.txt", "rb") as f:
        data = f.read()

    aesgcm = AESGCM(key)
    ciphertxt = aesgcm.encrypt(nonce, data, aad)

    corrupting_mask = int.to_bytes(1, len(ciphertxt), "big")
    corrupt_ciphertxt = bytes(bk ^ mk for bk, mk in zip(ciphertxt, corrupting_mask))

    print(b64encode(ciphertxt).decode())
    print(b64encode(corrupt_ciphertxt).decode())


if __name__ == "__main__":
    main()
