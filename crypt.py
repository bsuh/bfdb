import base64
from Crypto.Cipher import AES


def pkcs5_pad(s):
    return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)


def pkcs5_unpad(s):
    return s[0:-ord(s[-1])]


def encode(s, key):
    cipher = AES.new(key.ljust(16, '\x00'))
    return base64.b64encode(cipher.encrypt(pkcs5_pad(s)))


def decode(s, key):
    cipher = AES.new(key.ljust(16, '\x00'))
    return pkcs5_unpad(cipher.decrypt(base64.b64decode(s)))
