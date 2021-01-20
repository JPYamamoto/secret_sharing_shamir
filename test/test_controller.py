import os
import mock
import random
import filecmp
import shutil
import pytest
import string
from shamir.controller import Controller
from shamir.io import IO
from shamir.argument_error import ArgumentError

BABY_YODA_ORIGINAL = './test/test_assets/test.jpg'
BABY_YODA_ENCRYPT = './test/test_assets/test_encrypt.jpg'
TEXT_ORIGINAL = './test/test_assets/text_original.txt'
TEXT_ENCRYPT = './test/test_assets/text_encrypt.txt'
BINARY_ORIGINAL = './test/test_assets/binary_original.txt'
BINARY_ENCRYPT = './test/test_assets/binary_encrypt.txt'

class TestController:

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_encrypt_decrypt_image(self):
        self.verify_test(BABY_YODA_ORIGINAL, BABY_YODA_ENCRYPT)

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_encrypt_decrypt_text(self):
        self.verify_test(TEXT_ORIGINAL, TEXT_ENCRYPT)

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_encrypt_decrypt_binary(self):
        with open(BINARY_ORIGINAL, 'wb') as f:
            f.write(os.urandom(8192)) # 8 kiB

        self.verify_test(TEXT_ORIGINAL, TEXT_ENCRYPT)

    def verify_test(self, original, encrypt):
        n = random.randint(15, 256)
        t = random.randint(3, n-10)
        k = random.randint(1, n-t)
        m = n-k-t+1 + random.randint(1, t-1)

        shutil.copy(original, encrypt)

        with mock.patch.object(IO, 'input_secret', lambda _: 'Una vaca vestida de uniforme'):
            Controller.encrypt(encrypt, n, t)

        Controller.decrypt(encrypt + '.frg', encrypt + '.aes')
        filecmp.clear_cache()
        assert filecmp.cmp(original, encrypt)

        self.delete_lines(encrypt + '.frg', k)
        Controller.decrypt(encrypt + '.frg', encrypt + '.aes')
        filecmp.clear_cache()
        assert filecmp.cmp(original, encrypt)

        try:
            self.delete_lines(encrypt + '.frg', m)
            Controller.decrypt(encrypt + '.frg', encrypt + '.aes')
            filecmp.clear_cache()
            assert not filecmp.cmp(original, encrypt)
        except ArgumentError:
            assert True

    @pytest.fixture(autouse=True)
    def remove_temp_files(self):
        yield

        files = [
            BABY_YODA_ENCRYPT,
            BABY_YODA_ENCRYPT + '.aes',
            BABY_YODA_ENCRYPT + '.frg',
            TEXT_ENCRYPT,
            TEXT_ENCRYPT + '.aes',
            TEXT_ENCRYPT + '.frg',
            BINARY_ENCRYPT,
            BINARY_ENCRYPT + '.aes',
            BINARY_ENCRYPT + '.frg',
        ]
        for filename in files:
            if os.path.exists(filename):
                os.remove(filename)

    def delete_lines(self, filename, k):
        lines = []

        with open(filename, 'r') as f:
            lines = f.readlines()

        with open(filename, 'w') as f:
            new_lines = lines[k:]
            f.writelines(new_lines)

