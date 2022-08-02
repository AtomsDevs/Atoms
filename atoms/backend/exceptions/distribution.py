from atoms.backend.exceptions.exception import AtomsException


class AtomsUnknownDistribution(AtomsException):
    """
    Exception raised when the distribution id is unknown.
    """

    def __init__(self, distribution_id: str):
        super().__init__("Unknown distribution id: {}".format(distribution_id))
