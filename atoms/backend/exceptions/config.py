from atoms.backend.exceptions.exception import AtomsException


class AtomsCantMakeAtomsPath(AtomsException):
    """
    Exception raised when it is not possible to create the atoms path
    due to a permission error.
    """

    def __init__(self, path: str):
        super().__init__("Atoms can't make the atoms path due to missing permissions: {}".format(path))
