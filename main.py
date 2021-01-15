#!/usr/bin/env python3
"""
Shamir's Secret Sharing Scheme.
"""

__author__ = "Juan Pablo Yamamoto Zazueta, Luis Edgar Flores Ayala and Fausto David Hernández Jasso"
__version__ = "1.0.0"
__license__ = "MIT"

import argparse
from shamir.controller import Controller
from shamir.argument_error import ArgumentError

USAGE = "%(prog)s [c input n t output|d fragments cyphered]"
DESCRIPTION = "Cyphers and decyphers files using Shamir's Secret Sharing Scheme."
ARGS = {
    "input": "The file to be ciphered.",
    "n": "The number of evaluations to be generated.",
    "t": "The minimum number of fragments required to successfully decipher the file.",
    "fragments": "The file with at least t out of n needed evaluations.",
    "cyphered": "The file to be deciphered.",
    "c": "Ciphering mode.",
    "d": "Deciphering mode.",
    "mode": "Execution mode: [c]ipher or [d]ecipher.",
}


def main(**kwargs):
    """ Main entry point of the app """
    if kwargs['[c|d]'] == 'c':
        if kwargs['n'] <= 2:
            raise ArgumentError("n should be higher than 2.")
        if kwargs['t'] < 2 or kwargs['t'] > kwargs['n']:
            raise ArgumentError("t should be between 2 and n (inclusive).")

        Controller.encrypt(args.input, args.n, args.t)
    elif kwargs['[c|d]'] == 'd':
        if not kwargs['cyphered'].endswith('.aes'):
            raise ArgumentError("The name of the cyphered file should have the extension .aes")

        if not kwargs['fragments'].endswith('.frg'):
            raise ArgumentError("The name of the fragments file should have the extension .frg")

        Controller.decrypt(args.fragments, args.cyphered)
    else:
        raise ArgumentError("Invalid command.")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(prog='main.py', usage=USAGE, description=DESCRIPTION)

    # Positional arguments
    suparsers = parser.add_subparsers(required=True, dest='[c|d]', help=ARGS['mode'])
    parser_encrypt = suparsers.add_parser('c', help=ARGS['c'])
    parser_decrypt = suparsers.add_parser('d', help=ARGS['d'])

    # Encrypt Mode
    parser_encrypt.add_argument('input', help=ARGS['input'])
    parser_encrypt.add_argument('n', help=ARGS['n'], type=int)
    parser_encrypt.add_argument('t', help=ARGS['t'], type=int)

    # Decrypt Mode
    parser_decrypt.add_argument('fragments', help=ARGS['fragments'])
    parser_decrypt.add_argument('cyphered', help=ARGS['cyphered'])

    args = parser.parse_args()

    try:
        main(**vars(args))
    except ArgumentError as a:
        parser.error(str(a))
    except ValueError as v:
        print(str(v))
    except IOError as io:
        print("Error when opening the file: {}".format(io.filename))

