from shamir.crypto import Crypto
from secrets import choice
import pytest
from string import ascii_letters, ascii_uppercase, digits


class TestCrypto:
    CHARS = ascii_letters + ascii_uppercase + digits
    TEST_PASSWORD = "nombre_de_mi_perro"
    TEST_PASSWORD_2 = "contraseña chafa"

    def random_string(self):
        string = ''.join(choice(self.CHARS) for char in range(150))
        return string

    def test_sha256(self):
        dispersion = Crypto.sha_256(self.TEST_PASSWORD)
        dispersion2 = Crypto.sha_256(self.TEST_PASSWORD_2)
        assert dispersion == b'\xc2;\xbd\xean\xe8\xc5-\xd851\xa1\xc6\xd1H\x85\x03\xf8\x045a=\x003\xad\xb6\x19\x8a{\xce$\x1b'
        assert dispersion2 == b'\xd2\xa9L\x99\xa2\x87T\xd3\x9a(\x8b\x1ae\x14\x02\x83\xb9\x84\x0f\xfe7\x9a4\xff>Y\xb2M\xe8y|\x12'

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_encryp_desencrypt(self):
        for i in range(0, 20):
            message = self.random_string()
            password = self.random_string()
            sha256 = Crypto.sha_256(password)
            encrypted = Crypto.to_aes(message, sha256)
            desencrypted  = Crypto.from_aes(encrypted, sha256)
            inf = message.encode('utf8')
            assert desencrypted == inf

