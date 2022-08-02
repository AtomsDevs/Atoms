from atoms.backend.models.distribution import AtomDistribution


class Debian(AtomDistribution):
    def __init__(self):
        super().__init__(
            "debian", "Debian", "debian-symbolic",
            ["21.04", "22.04"],
            # TODO: remote_structure not found
            "http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/buntu-base-{0}-base-{1}.tar.gz",
            ["amd64"]
        )
