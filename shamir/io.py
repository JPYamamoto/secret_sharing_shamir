import getpass

class IO:
    @staticmethod
    def input_secret(msg):
        return getpass.getpass(msg)

    @staticmethod
    def read_file(filename, *, binary = False):
        mode = 'r'
        if binary:
            mode += 'b'

        with open(filename, mode) as f:
            return f.read()

    @staticmethod
    def write_file(filename, content, *, binary = False):
        mode = 'w'
        if binary:
            mode += 'b'

        with open(filename, mode) as f:
            f.write(content)

