from atoms.backend.models.distribution import AtomDistribution


class AlpineLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            "alpine", "Alpine Linux", "alpine-linux-symbolic",
            ["3.16.0", "3.16.1"],
            "https://dl-cdn.alpinelinux.org/alpine/v{0}/releases/{1}/alpine-minirootfs-{2}-{1}.tar.gz",
            ["x86_64"]
        )
    
    def get_remote(self, architecture: str, release: str):
        return self.remote_structure.format(
            '.'.join(release.split('.')[:2]), # only take major and minor version
            architecture, 
            release
        )