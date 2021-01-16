import getpass

class IO:
    """Input/Output related utilities.
    """

    @staticmethod
    def input_secret(msg):
        """Prompt the user for an input using a given message. The input will
        not be visible on the terminal.

        Args:
            msg: The message to display to the user prompting for an input.
        """
        return getpass.getpass(msg)

    @staticmethod
    def read_file(filename, *, binary = False):
        """Read a file whose name was supplied as a parameter. By default
        reads its content as a text, unless specified, in which case it will
        be read as a byte array.

        Args:
            filename: The name of the file to be read.
            binary: Whether to read the file as binary or not.
        """
        mode = 'r'
        if binary:
            mode += 'b'

        with open(filename, mode) as f:
            return f.read()

    @staticmethod
    def write_file(filename, content, *, binary = False):
        """Write a given content to a file. The content can be supplied as
        a byte array or as plain text.

        Args:
            filename: The name of the file to be written.
            content: The content to write to the specified file.
            binary: Whether to read the file as binary or not.
        """
        mode = 'w'
        if binary:
            mode += 'b'

        with open(filename, mode) as f:
            f.write(content)

