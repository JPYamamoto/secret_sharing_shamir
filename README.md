# Shamir's Secret Sharing Scheme

Cipher and decipher files using Shamir's Secret Sharing Scheme.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package.

```bash
pip install -r requirements.txt
```

## Tests

The project runs with Python 3. If the default version is Python 2, use the command `python3` instead. Tests can take from 2 seconds up to 70 seconds, depending on the random number of generated fragments.

```bash
pytest
```

## Usage

### Cipher

Provide the name of the file, followed by the total amount of evaluations to generate and the minimum number of evaluations required to decrypt the file. A password will be required as well, without being printed on the terminal.

```bash
# ./main.py c <file> <n> <t>
./main.py c ./test/test_assets/test.jpg 10 7
```

### Decipher

Provide the name of the file with the evaluations and the name of the encrypted file.

```bash
# Decipher
# ./main.py d <fragments file> <ciphered file>
./main.py d ./test/test_assets/test.jpg.frg ./test/test_assets/test.jpg.aes
```

## Documentation

After having the requirements installed, execute the following command:

```bash
cd docs/

# To generate the documentation in HTML format
make html

# To generate the documentation in LaTeX format
make latex
```

Generated docs will be located in `docs/build/`.

## License
[MIT](LICENSE)
