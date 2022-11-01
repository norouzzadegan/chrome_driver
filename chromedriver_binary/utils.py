# coding: utf-8
"""
Helper functions for filename and URL generation.
"""

import sys
import os
import subprocess
import re
import urllib
import socket
import ssl

import urllib.request

try:
    from urllib.request import urlopen, URLError, Request
except ImportError:
    from urllib2 import urlopen, URLError

__author__ = 'Daniel Kaiser <d.kasier@fz-juelich.de>'


def get_chromedriver_filename():
    """
    Returns the filename of the binary for the current platform.
    :return: Binary filename
    """
    if sys.platform.startswith('win'):
        return 'chromedriver.exe'
    return 'chromedriver'


def get_variable_separator():
    """
    Returns the environment variable separator for the current platform.
    :return: Environment variable separator
    """
    if sys.platform.startswith('win'):
        return ';'
    return ':'


def get_chromedriver_url(version):
    """
    Generates the download URL for current platform , architecture and the given version.
    Supports Linux, MacOS and Windows.
    :param version: chromedriver version string
    :return: Download URL for chromedriver
    """
    base_url = 'https://chromedriver.storage.googleapis.com/'
    if sys.platform.startswith('linux') and sys.maxsize > 2 ** 32:
        platform = 'linux'
        architecture = '64'
    elif sys.platform == 'darwin':
        platform = 'mac'
        architecture = '64'
    elif sys.platform.startswith('win'):
        platform = 'win'
        architecture = '32'
    else:
        raise RuntimeError('Could not determine chromedriver download URL for this platform.')
    return base_url + version + '/chromedriver_' + platform + architecture + '.zip'


def find_binary_in_path(filename):
    """
    Searches for a binary named `filename` in the current PATH. If an executable is found, its absolute path is returned
    else None.
    :param filename: Filename of the binary
    :return: Absolute path or None
    """
    if 'PATH' not in os.environ:
        return None
    for directory in os.environ['PATH'].split(get_variable_separator()):
        binary = os.path.abspath(os.path.join(directory, filename))
        if os.path.isfile(binary) and os.access(binary, os.X_OK):
            return binary
    return None


def open_url(url):
    if 'HTTP_PROXY' in os.environ:
        return open_url_with_http_proxy(url, os.environ['HTTP_PROXY'])
    elif 'SOCKS_PROXY' in os.environ:
        proxy_url, proxy_port = os.environ['SOCKS_PROXY'].rsplit(':')[-2:]
        return open_url_with_socks_proxy(url, proxy_url.strip('/'), int(proxy_port))
    else:
        return urllib.request.urlopen(url)


def open_url_with_socks_proxy(url, proxy_url, proxy_port):
    import socks

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    request = Request(url)
    socks.set_default_proxy(socks.SOCKS5, proxy_url, proxy_port)
    socket.socket = socks.socksocket
    return urlopen(request, context=ctx)


def open_url_with_http_proxy(url, proxy):
    proxy_support = urllib.request.ProxyHandler(
        {'http': proxy, 'https': proxy}
    )
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    return urllib.request.urlopen(url)


def get_latest_release_for_version(version=None):
    """
    Searches for the latest release (complete version string) for a given major `version`. If `version` is None
    the latest release is returned.
    :param version: Major version number or None
    :return: Latest release for given version
    """
    release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    if version:
        release_url += '_{}'.format(version)
    try:
        response = open_url(release_url)
        if response.getcode() != 200:
            raise URLError('Not Found')
        return response.read().decode('utf-8').strip()
    except URLError:
        raise RuntimeError('Failed to find release information: {}'.format(release_url))


def get_chrome_major_version():
    """
    Detects the major version number of the installed chrome/chromium browser.
    :return: The browsers major version number or None
    """
    browser_executables = ['google-chrome', 'chrome', 'chrome-browser', 'google-chrome-stable', 'chromium', 'chromium-browser']
    if sys.platform == "darwin":
        browser_executables.insert(0, "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

    for browser_executable in browser_executables:
        try:
            version = subprocess.check_output([browser_executable, '--version'])
            return re.match(r'.*?((?P<major>\d+)\.(\d+\.){2,3}\d+).*?', version.decode('utf-8')).group('major')
        except Exception:
            pass


def check_version(binary, required_version):
    try:
        version = subprocess.check_output([binary, '-v'])
        version = re.match(r'.*?([\d.]+).*?', version.decode('utf-8'))[1]
        if version == required_version:
            return True
    except Exception:
        return False
    return False


def get_chromedriver_path():
    """
    :return: path of the chromedriver binary
    """
    return os.path.abspath(os.path.dirname(__file__))


def print_chromedriver_path():
    """
    Print the path of the chromedriver binary.
    """
    print(get_chromedriver_path())
