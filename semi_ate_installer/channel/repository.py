import itertools
from typing import List
from mamba import repoquery as repoquery_api
from conda.base.context import context
from json import loads
from semi_ate_installer.utils.packages import PackageInfo

from packaging import version


class Repository:
    @staticmethod
    def get_available_versions(package_query: str, channel: str = 'conda-forge') -> List[PackageInfo]:
        pool = repoquery_api.create_pool([channel], context.platform, False)
        query_result: dict = loads(repoquery_api._repoquery('search', package_query, pool)).get('result')

        if query_result['status'] != 'OK':
            return []

        packages = {}

        for p in query_result['pkgs']:
            packages.setdefault(p['name'], []).append(p.get('version'))
        
        package_set = []
        for name, vers in packages.items():
            highest_version = version.parse('0.0.0')
            for ver1, ver2 in itertools.combinations(vers, 2):
                version_item1 = version.parse(ver1)
                version_item2 = version.parse(ver2)
                if version_item1 > version_item2 and version_item1 > highest_version:
                    highest_version = version_item1
                elif version_item1 < version_item2 and version_item2 > highest_version:
                    highest_version = version_item2
                else:
                    continue

            package_set.append(PackageInfo(name, highest_version))

        return list(package_set)
