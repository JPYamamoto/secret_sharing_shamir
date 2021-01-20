import random
from .io import IO
from .crypto import Crypto
from .polynomial import Polynomial
from .argument_error import ArgumentError

MODSZ = 208351617316091241234326746312124448251235562226470491514186331217050270460481
BITS = 256

class Controller:
    """Join the different parts of the code in order to perform the Shamir's
    Secret Code Sharing Scheme.
    """

    @staticmethod
    def encrypt(entry_file, n, t):
        """Performs the ciphering of a given file and uses SSSS to generate
        n evaluations. Out of the n evaluations, only t will be necessary in
        order to decipher the file.

        The user will have to input a password (it will not be displayed on the
        terminal) in order to perform the ciphering.
        A file with the same name but .aes extension will be written, it being
        the ciphered file.
        Another file with the same name but .frg extension will also be written,
        containing n lines each containing a fragment.

        Args:
            entry_file: The name of the file to be ciphered.
            n: The number of fragments to be generated.
            t: The minimum number of needed fragments in order to decipher the file.
        """
        # Generate the password used to cipher the file.
        password = IO.input_secret("Input a password: ")
        sha_pass = Crypto.sha_256(password)

        # Read and cipher the file.
        file_content = IO.read_file(entry_file, binary=True)
        aes_result = Crypto.to_aes(file_content, sha_pass)

        # Generate a random polynomial.
        coefficients = Controller._sample_random_bits(BITS, t-1)
        coefficients.insert(0, int.from_bytes(sha_pass, byteorder='little'))
        polynomial = Polynomial(coefficients)

        # Evaluate the polynomial on n random points.
        domain = Controller._sample_random_bits(BITS, n)
        evaluations = [(x, polynomial.evaluate(x, MODSZ)) for x in domain]

        # Write the output.
        out_frg = '\n'.join(['({},{})'.format(p[0], p[1]) for p in evaluations])
        IO.write_file(entry_file + '.aes', aes_result, binary=True)
        print("The file {}.aes was successfully generated.".format(entry_file))
        IO.write_file(entry_file + '.frg', out_frg)
        print("The file {}.frg was successfully generated.".format(entry_file))


    @staticmethod
    def decrypt(points_file, cyphered_file):
        """Deciphers a file, previously ciphered using the SSSS, by performing
        a polynomial interpolation over a finite field, using the evaluations
        provided in another file.

        If the given evaluations are less than were indicated as required when
        ciphering the file, the result will be a random file, otherwise the
        original file will be restored with the same name as the cyphered_file
        but removing the .aes extension.

        Args:
            points_file: The name of the file containing the fragments.
            cyphered_file: The name of the ciphered file, to be deciphered.
        """
        # Read the ciphered file.
        cyphered_content = IO.read_file(cyphered_file, binary=True)

        # Get the fragments and use them to retrieve the password to decipher
        # the file.
        try:
            points_content = IO.read_file(points_file)
            points = Controller._parse_points(points_content)
            password = Polynomial.lagrange(points, 0, MODSZ)
            password_bytes = password.to_bytes(32, byteorder='little')
        except OverflowError:
            raise ArgumentError("Error when deciphering the file, probably due to a lack of fragments.")
        except ValueError:
            raise ArgumentError("Error when reading the file {}. Invalid format.".format(cyphered_file))

        # Decipher the file.
        clear_content = Crypto.from_aes(cyphered_content, password_bytes)
        clear_filename = cyphered_file.replace('.aes', '')

        # Write the deciphered file.
        IO.write_file(clear_filename, clear_content, binary=True)
        print("The file {} was successfully generated.".format(clear_filename))


    @staticmethod
    def _parse_points(points_text):
        """Given a string containing many lines, each with a tuple containing
        an evaluation, parse it into a list of tuples with the corresponding
        evaluations.

        Args:
            points_text: The string containing the fragments.
        """
        lines = points_text.strip().split('\n')
        points = []

        for line in lines:
            line = line[1:-1].split(',')
            points.append((int(line[0]), int(line[1])))

        return points


    @staticmethod
    def _sample_random_bits(bits, k):
        """Generate a list with k random unique integers in the range of a
        given number of bits.

        Args:
            bits: The number of bits the integers should be.
            k: The number of integers in the returned list.
        """
        sample = set()

        while len(sample) < k:
            sample.add(int(random.getrandbits(bits)))

        return list(sample)

