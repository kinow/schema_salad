import subprocess
import time

import pkg_resources
from setuptools.command.egg_info import egg_info

SETUPTOOLS_VER = pkg_resources.get_distribution(
    "setuptools").version.split('.')

RECENT_SETUPTOOLS = int(SETUPTOOLS_VER[0]) > 40 or (
    int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) > 0) or (
        int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) == 0 and
        int(SETUPTOOLS_VER[2]) > 0)

print('##### BRUNO')
print(RECENT_SETUPTOOLS)

class EggInfoFromGit(egg_info):
    """Tag the build with git commit timestamp.

    If a build tag has already been set (e.g., "egg_info -b", building
    from source package), leave it alone.
    """

    def git_timestamp_tag(self):
        print('--- git_timestamp_tag')
        gitinfo = subprocess.check_output(
            ['git', 'log', '--first-parent', '--max-count=1',
             '--format=format:%ct', '.']).strip()
        return time.strftime('.%Y%m%d%H%M%S', time.gmtime(int(gitinfo)))

    def tags(self):
        print('--- tags')
        print('##### BRUNO')
        print(self.tag_build)
        if self.tag_build is None:
            try:
                self.tag_build = self.git_timestamp_tag()
            except subprocess.CalledProcessError as e:
                print('##### BRUNO')
                print(e)
                pass
        return egg_info.tags(self)

    if RECENT_SETUPTOOLS:
        print('--- RECENT_SETUPTOOLS')
        vtags = property(tags)
