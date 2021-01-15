import hashlib
from Crypto.Cipher import AES

class Crypto:
    @staticmethod
    def sha_256(text):
        password = hashlib.sha256(text.encode('utf8')).digest()
        return password

    @staticmethod
    def to_aes(text, password):
        aes = AES.new(password, AES.MODE_CFB, 16 * b'\0')
        encrypted = aes.encrypt(text)
        return encrypted

    @staticmethod
    def from_aes(text, password):
        aes = AES.new(password, AES.MODE_CFB, 16 * b'\0')
        desencrypted = aes.decrypt(text)
        return desencrypted

