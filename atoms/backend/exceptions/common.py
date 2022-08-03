from atoms.backend.exceptions.exception import AtomsException


class AtomsNoBinaryFound(AtomsException):
    """
    Exception raised when no binary is found.
    """

    def __init__(self, binary_name: str):
        super().__init__("No binary found, ensure it is installed: {}".format(binary_name))
