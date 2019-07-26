from packmule.pkg import (
        PackageManager, Package, PackageVer)
from packmule.errors import PackageManagerNotInstalled
from subprocess import run, PIPE
from pint import UnitRegistry


ureg = UnitRegistry()


class XBPS(PackageManager):
    name = "XBPS"
    check_cmd = ["xq"]

    def installed(self):
        cmd = ["xpkg", "-V"]
        size_cmd = ["xhog"]
        installed_dict = {}
        installed = []

        installed_res = run(cmd, stdout=PIPE, check=True, encoding="utf-8")
        installed_list = installed_res.stdout.strip().split("\n")
        for line in installed_list:
            line = [s.strip() for s in line.split(" ", 1)]
            name, ver_str = self._full_name_split(line[0])
            ver = self._parse_version(ver_str)
            desc = line[1]
            installed_dict[name] = {
                "ver": ver,
                "desc": desc
            }

        size_res = run(size_cmd, stdout=PIPE, check=True, encoding="utf-8")
        size_list = size_res.stdout.strip().split("\n")
        for line in size_list:
            line = [s.strip() for s in line.split(" ", 1)]
            name, _ = self._full_name_split(line[0])
            size = ureg(self._format_size_str(line[1]))
            installed_dict[name]["size"] = size

        for name, pkg in installed_dict.items():
            installed.append(
                    Package(name, pkg["ver"], self, pkg["size"], pkg["desc"]))

        return installed

    @staticmethod
    def _parse_version(ver: str) -> PackageVer:
        sections, rev = tuple(ver.split("_"))
        try:
            sections = [int(d) for d in sections.split(".")]
        except ValueError:
            sections = [sections]
        sections.append(int(rev))
        names = ["version_section" if v != sections[-1] else "revision"
                 for v in sections]
        format = ".".join(["%s" for v in sections if v != sections[-1]])
        format += "_%s"
        return PackageVer(sections, names, format)

    @staticmethod
    def _full_name_split(full_name):
        out = tuple(full_name.rsplit("-", 1))
        return out

    @staticmethod
    def _format_size_str(size_str):
        size_str = size_str.replace("K", "k")
        return size_str


