from shamir.io import IO
import os
import string
import random

TEST_FILE = './test/test_assets/io_test.txt'

class TestIO:

    def test_read_write_text(self):
        length = random.getrandbits(8)
        content = ''.join(random.choice(string.ascii_letters) for _ in range(length))

        IO.write_file(TEST_FILE, content)
        written = IO.read_file(TEST_FILE)

        print(content)
        print(written)
        assert (content == written)

    def test_read_write_binary(self):
        content = os.urandom(2**16)

        IO.write_file(TEST_FILE, content, binary=True)
        written = IO.read_file(TEST_FILE, binary=True)

        assert (content == written)

