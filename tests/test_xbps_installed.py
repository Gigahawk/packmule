from packmule.managers.xbps import XBPS
from packmule.pkg import PackageVer
from numbers import Number


def test_xbps_installed():
    xbps = XBPS()
    installed = xbps.installed()
    for pkg in installed:
        assert isinstance(pkg.name, str)
        assert isinstance(pkg.desc, str)
        assert isinstance(float(pkg.size), Number)
        assert isinstance(pkg.version, PackageVer)
        assert isinstance(pkg.manager, XBPS)
