from binascii import b2a_hex, a2b_hex
from string import octdigits

from pyDes import des, PAD_PKCS5, ECB


def des_encrypt(data, key=octdigits):
    return b2a_hex(des(key, ECB, key, padmode=PAD_PKCS5).encrypt(data.encode())).decode()


def des_crypt(data, key=octdigits):
    return des(key, ECB, key, padmode=PAD_PKCS5).decrypt(a2b_hex(data.encode()), padmode=PAD_PKCS5).decode()
