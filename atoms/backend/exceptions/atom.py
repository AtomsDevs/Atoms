from atoms.backend.exceptions.exception import AtomsException


class AtomsWrongAtomData(AtomsException):
    """
    Exception raised when the atom data is wrong.
    """

    def __init__(self, data: dict):
        super().__init__("Wrong atom data: {}".format(str(data)))
