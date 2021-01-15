import random
from .io import IO
from .crypto import Crypto
from .polynomial import Polynomial

MODSZ = 208351617316091241234326746312124448251235562226470491514186331217050270460481
BITS = 256

class Controller:

    @staticmethod
    def encrypt(entry_file, n, t):
        password = IO.input_secret("Input a password: ")
        sha_pass = Crypto.sha_256(password)

        file_content = IO.read_file(entry_file, binary=True)
        aes_result = Crypto.to_aes(file_content, sha_pass)

        coefficients = Controller._sample_random_bits(BITS, t-1)
        coefficients.insert(0, int.from_bytes(sha_pass, byteorder='little'))

        polynomial = Polynomial(coefficients)
        domain = Controller._sample_random_bits(BITS, n)
        evaluations = [(x, polynomial.evaluate(x, MODSZ)) for x in domain]

        out_frg = '\n'.join(['({},{})'.format(p[0], p[1]) for p in evaluations])

        IO.write_file(entry_file + '.aes', aes_result, binary=True)
        print("The file {}.aes was successfully generated.".format(entry_file))
        IO.write_file(entry_file + '.frg', out_frg)
        print("The file {}.frg was successfully generated.".format(entry_file))


    @staticmethod
    def decrypt(points_file, cyphered_file):
        cyphered_content = IO.read_file(cyphered_file, binary=True)

        points_content = IO.read_file(points_file)
        points = Controller._parse_points(points_content)
        password = Polynomial.lagrange(points, 0, MODSZ)
        password_bytes = password.to_bytes(BITS // 8, byteorder='little')

        clear_content = Crypto.from_aes(cyphered_content, password_bytes)
        clear_filename = cyphered_file.replace('.aes', '')
        IO.write_file(clear_filename, clear_content, binary=True)
        print("The file {} was successfully generated.".format(clear_filename))


    @staticmethod
    def _parse_points(points_text):
        lines = points_text.strip().split('\n')
        points = []

        for line in lines:
            line = line[1:-1].split(',')
            points.append((int(line[0]), int(line[1])))

        return points


    @staticmethod
    def _sample_random_bits(bits, k):
        sample = set()

        while len(sample) < k:
            sample.add(int(random.getrandbits(bits)))

        return list(sample)

