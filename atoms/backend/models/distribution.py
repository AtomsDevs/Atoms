class AtomDistribution:
    distribution_id: str
    name: str
    logo: str

    def __init__(self, distribution_id: str, name: str, logo: str):
        self.distribution_id = distribution_id
        self.name = name
        self.logo = logo

    def __str__(self):
        return f"Distribution {self.name}"


class AlpineLinux(AtomDistribution):
    def __init__(self):
        super().__init__("alpine", "Alpine Linux", "alpine-linux-symbolic")


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__("ubuntu", "Ubuntu", "ubuntu-symbolic")


class Fedora(AtomDistribution):
    def __init__(self):
        super().__init__("fedora", "Fedora", "fedora-symbolic")


class Debian(AtomDistribution):
    def __init__(self):
        super().__init__("debian", "Debian", "debian-symbolic")
