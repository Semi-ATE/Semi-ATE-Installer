from typing import List
from mamba import repoquery as repoquery_api
from conda.base.context import context
from json import loads
from utils.packages import AvailablePackageInfo

class Repository:

    channel: str

    def __init__(self, channel: str = 'conda-forge'):
        self.channel = channel


    def get_available_versions(self, package_query: str) -> List[AvailablePackageInfo]:
        package_set = set([])
        pool = repoquery_api.create_pool([self.channel], context.platform, False)
        query_result: dict = loads(repoquery_api._repoquery('search', package_query, pool)).get('result')

        if query_result['status'] != 'OK':
            return []
    
        for p in query_result['pkgs']:
            info = AvailablePackageInfo(p.get('name'), [p.get('version')])
            found = False
            for p_info in package_set:
                if p_info == info:
                    p_info.versions.add(p.get('version'))
                    found = True
                    break
            if found == False:
                package_set.add(info)

        return list(package_set)