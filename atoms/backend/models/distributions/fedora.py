from atoms.backend.models.distribution import AtomDistribution


class Fedora(AtomDistribution):
    def __init__(self):
        super().__init__(
            "fedora", "Fedora", "fedora-symbolic",
            ["36.20220723.2.2"],
            # TODO: remote_structure may be incorrect
            "https://builds.coreos.fedoraproject.org/prod/streams/testing/builds/{0}/{1}/fedora-coreos-{0}-live-rootfs.{1}.img",
            ["amd64"]
        )
