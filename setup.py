from setuptools import setup
from setuptools.command.build_py import build_py
from chromedriver_binary.utils import get_chromedriver_filename, get_chromedriver_url, find_binary_in_path, \
    check_version, get_chrome_major_version, get_latest_release_for_version, open_url

import os
import zipfile

try:
    from io import BytesIO
    from urllib.request import urlopen, URLError, Request
except ImportError:
    from StringIO import StringIO as BytesIO
    from urllib2 import urlopen, URLError

__author__ = 'Iman Azari <azari@mahsan.co>'


with open('README.md') as readme_file:
    long_description = readme_file.read()


class DownloadChromedriver(build_py):
    def run(self):
        """
        Downloads, unzips and installs chromedriver.
        If a chromedriver binary is found in PATH it will be copied, otherwise downloaded.
        """
        chrome_major = get_chrome_major_version()
        print('TTTTTTTTTTTTTTTTTTTTT')
        print(chrome_major)
        chromedriver_version = get_latest_release_for_version(chrome_major)
        chromedriver_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chromedriver_binary')
        chromedriver_filename = find_binary_in_path(get_chromedriver_filename())
        if chromedriver_filename and check_version(chromedriver_filename, chromedriver_version):
            print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            new_filename = os.path.join(chromedriver_dir, get_chromedriver_filename())
            self.copy_file(chromedriver_filename, new_filename)
        else:
            chromedriver_bin = get_chromedriver_filename()
            chromedriver_filename = os.path.join(chromedriver_dir, chromedriver_bin)
            if not os.path.isfile(chromedriver_filename) or not check_version(chromedriver_filename, chromedriver_version):
                print("\nDownloading Chromedriver...\n")
                if not os.path.isdir(chromedriver_dir):
                    os.mkdir(chromedriver_dir)
                url = get_chromedriver_url(version=chromedriver_version)
                try:
                    response = open_url(url)
                    if response.getcode() != 200:
                        raise URLError('Not Found')
                except URLError:
                    raise RuntimeError('Failed to download chromedriver archive: {}'.format(url))
                archive = BytesIO(response.read())
                with zipfile.ZipFile(archive) as zip_file:
                    zip_file.extract(chromedriver_bin, chromedriver_dir)
            else:
                print("\nChromedriver already installed at {}...\n".format(chromedriver_filename))
            if not os.access(chromedriver_filename, os.X_OK):
                os.chmod(chromedriver_filename, 0o744)
        build_py.run(self)


setup(
    name="proxied-chromedriver-binary-auto",
    version="0.3",
    author="Iman Azari",
    author_email="azari@mahsan.co",
    description="Installer for chromedriver.",
    license="MIT",
    keywords="chromedriver chrome browser selenium splinter",
    url="https://github.com/imanazari70/proxied-chromedriver-binary-auto",
    packages=['chromedriver_binary'],
    setup_requires=[
          'PySocks',
      ],
    package_data={
        'chromedriver_binary': ['chromedriver*']
    },
    entry_points={
        'console_scripts': ['chromedriver-path=chromedriver_binary.utils:print_chromedriver_path'],
    },
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Installation/Setup",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
    cmdclass={'build_py': DownloadChromedriver}
)
