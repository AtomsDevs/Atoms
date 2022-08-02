from atoms.backend.models.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            "ubuntu", "Ubuntu", "ubuntu-symbolic",
            ["21.04", "22.04"],
            "http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/buntu-base-{0}-base-{1}.tar.gz",
            ["amd64"]
        )
