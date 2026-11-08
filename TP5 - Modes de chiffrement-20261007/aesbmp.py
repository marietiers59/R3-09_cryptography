"""Gestion de fichiers BMP et chiffrement AES en modes ECB."""

import warnings

from PIL import Image
from PIL.BmpImagePlugin import BmpImageFile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import numpy as np


class CipherFriendlyBmpImage:
    """
    Sépare le contenu binaire d'un fichier BMP en deux parties :
    l'en-tête, les pixels.

    On suppose que le fichier BMP est au format BITMAPV5HEADER.
    Les données des pixels peuvent « déborder » et donc contenir plus que les pixels.

    Plus d'informations :
    https://en.wikipedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)

    Attributes:
        data (bytes): en-tête du fichier BMP
        pixel_data (bytes): données des pixels (overflow potentiellement)
    """

    def __init__(self, img: Image, bmp_data: bytes):
        self.img = img
        self.data = bmp_data
        self.offset = int.from_bytes(bmp_data[10:14], "little")

    @classmethod
    def open(self, fname: str):
        with open(fname, "rb") as f:
            data = f.read()
        img = Image.open(fname)
        if not isinstance(img, BmpImageFile):
            raise ValueError("The loaded image is not a Bitmap.")
        return CipherFriendlyBmpImage(img, data)

    def has_extra_data(self):
        return len(self.img.tobytes()) < len(self.tobytes())

    def _get_header(self):
        return self.data[: self.offset]

    def tobytes(self):
        return self.data[self.offset :]

    def copy(self):
        return CipherFriendlyBmpImage(self.img.copy(), bytes(self.data))

    def frombytes(self, pixel_data: bytes, remove_end=True):
        header = self._get_header()
        pixel_data_current = self.tobytes()

        self.data = header + pixel_data

        if remove_end and len(pixel_data) < len(pixel_data_current):
            warnings.warn(
                "Input data is shorter than the image pixel data. Some bytes have been deleted.",
                UserWarning,
                stacklevel=2,
            )
        else:
            self.data = self.data + pixel_data_current[len(pixel_data) :]

        self.img = bmpdata_to_img_like(pixel_data, self.img)

    def save(self, fname):
        with open(fname, "wb") as f:
            f.write(self.data)


def bmpdata_to_img_like(data: bytes, img: BmpImageFile):
    img_w, h = img.size
    bpp = len(img.getbands())

    rgb_w = img_w * bpp
    raw_w = rgb_w + (-rgb_w) % 4  # padding in raw file data
    raw_bmp_len = h * raw_w
    data_vec = np.array(list(data), dtype=np.uint8)[:raw_bmp_len]

    if raw_bmp_len < len(data):
        warnings.warn(
            "Not all pixels are stored in the `img` attribute, there might be a padding only available in the raw data.",
            UserWarning,
        )

    data_mat = data_vec.reshape(h, raw_w)
    data_mat = data_mat[:, :rgb_w]  # truncate padding
    rgba_mat = data_mat.reshape(h, img_w, bpp)  # separate channels
    a_mat = rgba_mat[:, :, 3:]
    rgb_mat = rgba_mat[:, :, :3][:, :, ::-1]
    img_mat = np.concat((rgb_mat, a_mat), axis=2)[::-1]

    new_img = img.copy()
    new_img.frombytes(img_mat.flatten())
    return new_img


def encrypt_aes_ecb(data: bytes, key: bytes) -> bytes:
    """
    Chiffre les données avec l'algorithme AES en mode ECB,
    après avoir ajouté un padding standard PKCS#7.

    Args:
        data (bytes): données à chiffrer
        key (bytes): clé de chiffrement (16, 24 ou 32 bytes)
    Returns:
        bytes: données chiffrées
    """
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data)
    encrypted_data += encryptor.finalize()
    return encrypted_data


def main():
    bmp = CipherFriendlyBmpImage("clear.bmp")

    key = b"ALL THEM WITCHES"
    cipher_data = encrypt_aes_ecb(bmp.tobytes(), key)

    cipher_bmp = bmp.copy()
    cipher_bmp.frombytes(cipher_data)
    cipher_bmp.save("cipher-ecb.bmp")


if __name__ == "__main__":
    main()
