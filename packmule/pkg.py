from subprocess import run
from packmule.errors import PackageManagerNotInstalled


class Package(object):
    def __init__(
            self,
            name: str,
            version,
            manager,
            size: None,
            desc: str = None):
        self.name = name
        self.version = version
        self.manager = manager
        self.size = size
        self.desc = desc


class PackageManager(object):
    name = None
    check_cmd = ["not_a_real_command"]

    def __init__(self):
        self._check_installed()

    def install(self, package: Package):
        raise NotImplementedError

    def uninstall(self, package: Package):
        raise NotImplementedError

    def search(self, package: Package):
        raise NotImplementedError

    def installed(self):
        raise NotImplementedError

    def _check_installed(self):
        res = run(self.check_cmd)
        if res.returncode != 0:
            raise PackageManagerNotInstalled(self.name)


class PackageVer(object):
    def __init__(self, sections, names=None, format=None):
        self.sections = sections
        self.names = names
        self.format = format

    def __eq__(self, other):
        if len(self.sections) != len(other.sections):
            raise ValueError("Version length mismatch")
        return self.sections == other.sections

    def __ne__(self, other):
        return not self.__eq__()

    def __lt__(self, other):
        if len(self.sections) != len(other.sections):
            raise ValueError("Version length mismatch")
        for a, b in zip(self.sections, other.sections):
            if a > b:
                return False
            if a < b:
                return True
        return False

    def __le__(self, other):
        return self.__eq__(self, other) or self.__lt__(self, other)

    def __gt__(self, other):
        if len(self.sections) != len(other.sections):
            raise ValueError("Version length mismatch")
        for a, b in zip(self.sections, other.sections):
            if a < b:
                return False
            if a > b:
                return True
        return False

    def __ge__(self, other):
        return self.__eq__(self, other) or self.__gt__(self, other)

    def __str__(self):
        if self.format is None:
            return ".".join(self.sections)

        return self.format % tuple(self.sections)

    def __repr__(self, other):
        return f"<PackageVer ({str(self)})>"
