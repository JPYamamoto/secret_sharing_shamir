import hashlib
from Crypto.Cipher import AES

class Crypto:
    """Crypto related utilities.
    """

    @staticmethod
    def sha_256(text):
        """Returns the 256-byte scatter of the password
        entered by the user.
        Args:
            text: The string with the password entered by the user.
        Returns:
            The 256-byte scatter of the string
        """
        password = hashlib.sha256(text.encode('utf8')).digest()
        return password

    @staticmethod
    def to_aes(text, password):
        """Returns the encrypted message using AES protocol
        Args:
            text: The message to encrypt.
            password: A 256-byte password to use in AES.
        Returns:
            The encrypted information by using AES protocol.
        """
        aes = AES.new(password, AES.MODE_CFB, 16 * b'\0')
        encrypted = aes.encrypt(text)
        return encrypted

    @staticmethod
    def from_aes(text, password):
        """Returns the desencrypted message using AES protocol
        Args:
            text: The encrypted message to desencrypt
            password: the 256-byte password used to encrypt
            the original message.
        Returns:
            The desencrypted information by using AES protocol.
        """
        aes = AES.new(password, AES.MODE_CFB, 16 * b'\0')
        desencrypted = aes.decrypt(text)
        return desencrypted

