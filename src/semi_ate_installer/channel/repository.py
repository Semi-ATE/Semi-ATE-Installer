import itertools
from typing import List
from mamba import repoquery as repoquery_api
from conda.base.context import context
from json import loads

from packaging import version

from semi_ate_installer.utils.packages import PackageInfo


class Repository:
    @staticmethod
    def get_available_versions(
        package_query: str, channel: str = "conda-forge"
    ) -> List[PackageInfo]:
        pool = repoquery_api.create_pool([channel], context.platform, False)
        query_result: dict = loads(
            repoquery_api._repoquery("search", package_query, pool)
        ).get("result")

        if query_result["status"] != "OK":
            return []

        packages = {}

        for p in query_result["pkgs"]:
            packages.setdefault(p["name"], []).append(p.get("version"))

        package_set = []
        for name, vers in packages.items():
            highest_version = version.parse("0.0.0")
            for ver1, ver2 in itertools.combinations(vers, 2):
                ver1_obj = version.parse(ver1)
                ver2_obj = version.parse(ver2)
                if ver1_obj > ver2_obj and ver1_obj > highest_version:
                    highest_version = ver1_obj
                elif ver1_obj < ver2_obj and ver2_obj > highest_version:
                    highest_version = ver2_obj
                else:
                    continue

            package_set.append(PackageInfo(name, highest_version))

        return list(package_set)
