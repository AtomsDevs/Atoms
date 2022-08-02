class AtomsException(Exception):
    """
    Base class for all Atoms exceptions.
    """

    def __init__(self, message: str = "An unknown error occurred."):
        super().__init__(message)