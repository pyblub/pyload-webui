#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: vuolter
#      ____________
#   _ /       |    \ ___________ _ _______________ _ ___ _______________
#  /  |    ___/    |   _ __ _  _| |   ___  __ _ __| |   \\    ___  ___ _\
# /   \___/  ______/  | '_ \ || | |__/ _ \/ _` / _` |    \\  / _ \/ _ `/ \
# \       |   o|      | .__/\_, |____\___/\__,_\__,_|    // /_//_/\_, /  /
#  \______\    /______|_|___|__/________________________//______ /___/__/
#          \  /
#           \/

import io
import os
import re
import shutil
import subprocess
from itertools import chain

from setuptools import Command, distutils, find_packages, setup
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


_NAMESPACE = 'pyload'
_PACKAGE = 'pyload.webui'
_PACKAGE_NAME = 'pyload.webui'
_PACKAGE_PATH = 'src/pyload/webui'
_CREDITS = (('Walter Purcaro', 'vuolter@gmail.com', '2015-2017'),
            ('pyLoad Team', 'info@pyload.net', '2009-2015'))


def _read_text(file):
    with io.open(file, encoding='utf-8')  as fp:
        return fp.read().strip()


def _write_text(file, text):
    with io.open(file, mode='w', encoding='utf-8') as fp:
        fp.write(text.strip() + os.linesep)


def _pandoc_convert(text):
    import pypandoc
    return pypandoc.convert_text(text, 'rst', 'markdown').replace('\r', '')


def _docverter_convert(text):
    import requests
    req = requests.post(
        url='http://c.docverter.com/convert',
        data={'from': 'markdown', 'to': 'rst'},
        files={'input_files[]': ('.md', text)}
    )
    req.raise_for_status()
    return req.text


def _convert_text(text):
    try:
        return _pandoc_convert(text)
    except Exception as e:
        print(str(e))
        return _docverter_convert(text)


def _purge_text(text):
    return re.sub('.*<.+>.*', '', text).strip()


def _gen_long_description():
    readme = _purge_text(_read_text('README.md').split(os.linesep * 3, 1)[0])
    history = _purge_text(_read_text('CHANGELOG.md'))
    desc = os.linesep.join((readme, history))
    return _convert_text(desc)


def _get_long_description():
    try:
        return _read_text('README.rst')
    except IOError:
        return _gen_long_description()


__re_section = re.compile(r'^\s*\[(.*?)\]\s+([^[]*)')
__re_deps = re.compile(r'^\s*(?![#; ]+)([^\s]+)')

def _extract_requires(text):
    deps = __re_deps.findall(__re_section.split(text, maxsplit=1))
    extras = dict((opt, deps) for opt, entries in __re_section.findall(text)
                  for deps in __re_deps.findall(entries) if deps)
    return deps, extras


def _get_requires(name):
    file = os.path.join('requirements', name + '.txt')
    text = _read_text(file)
    deps, extras = _extract_requires(text)
    if name.startswith('extra'):
        extras['full'] = list(set(chain(*list(extras.values()))))
        return extras
    return deps


def _get_version():
    return _read_text('VERSION')


class MakeReadme(Command):
    """
    Create a valid README.rst file
    """
    READMEFILE = 'README.rst'

    description = 'create a valid README.rst file'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.path.isfile(self.READMEFILE):
            return None
        _write_text(self.READMEFILE, _gen_long_description())


class BuildLocale(Command):
    """
    Build the locales
    """
    description = 'build the locales'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            os.makedirs(os.path.join(_PACKAGE_PATH, 'locale'))
        except OSError as e:
            print(str(e))
        self.run_command('extract_messages')
        self.run_command('init_catalog')
        # self.run_command('download_catalog')
        self.run_command('compile_catalog')


class BuildNode(Command):
    """
    BuildPy the nodejs app
    """
    NODEDIR = os.path.join(_PACKAGE_PATH, 'node_modules')

    description = 'build the nodejs app'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if os.path.isdir(self.NODEDIR):
            return None
        try:
            # if os.name == 'nt':
                # # : Required by npm package `grunt-contrib-compress` under Windows
                # subprocess.check_call(
                    # 'npm install --global windows-build-tools', shell=True)
            subprocess.check_call(
                'cd {0} && npm install --only=dev'.format(_PACKAGE_PATH), shell=True)
            subprocess.check_call(
                'cd {0} && node node_modules/grunt-cli/bin/grunt build'.format(_PACKAGE_PATH),
                shell=True)
        except subprocess.CalledProcessError:
            distutils.log.warn("Failed to build the nodejs app")
        shutil.rmtree(self.NODEDIR, ignore_errors=True)
        return subprocess.call(
            'cd {0} && npm install --production'.format(_PACKAGE_PATH), shell=True)


# class DownloadCatalog(Command):
    # """
    # Download the translation catalog from the remote repository
    # """
    # description = 'download the translation catalog from the remote repository'
    # user_options = []

    # def initialize_options(self):
        # pass

    # def finalize_options(self):
        # pass

    # def run(self):
        # raise NotImplementedError


class PreBuild(Command):
    """
    Prepare for build
    """
    description = 'prepare for build'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _makeabout(self):
        file = os.path.join(_PACKAGE_PATH, '__about__.py')
        credits = ', '.join(str(info) for info in _CREDITS)
        text = """# -*- coding: utf-8 -*-

from semver import parse_version_info

__namespace__ = {0}
__package__ = {1}
__package_name__ = {2}
__version__ = {3}
__version_info__ = parse_version_info(__version__)
__credits__ = ({4})
""".format(_NAMESPACE, _PACKAGE, _PACKAGE_NAME, _get_version(), credits)
        _write_text(file, text)

    def run(self):
        self._makeabout()
        self.run_command('build_node')
        self.run_command('build_locale')


class BdistEgg(bdist_egg):
    """
    Custom ``bdist_egg`` command
    """
    def run(self):
        if not self.dry_run:
            self.run_command('prebuild')
        bdist_egg.run(self)


class BuildPy(build_py):
    """
    Custom ``build_py`` command
    """
    def run(self):
        if not self.dry_run:
            self.run_command('prebuild')
        build_py.run(self)


class Sdist(sdist):
    """
    Custom ``sdist`` command
    """
    def run(self):
        if not self.dry_run:
            self.run_command('makereadme')
        sdist.run(self)


NAME = _PACKAGE_NAME
VERSION = _get_version()
STATUS = "1 - Planning"
DESC = """pyLoad WebUI module"""
LONG_DESC = _get_long_description()
KEYWORDS = ["pyload"]
URL = "https://pyload.net"
DOWNLOAD_URL = "https://github.com/pyload/webui/releases"
LICENSE = "GNU Affero General Public License v3"
AUTHOR = _CREDITS[0][0]
AUTHOR_EMAIL = _CREDITS[0][1]
PLATFORMS = ['any']
PACKAGES = find_packages('src')
PACKAGE_DIR = {'': 'src'}
INCLUDE_PACKAGE_DATA = True
NAMESPACE_PACKAGES = [_NAMESPACE]
INSTALL_REQUIRES = _get_requires('install')
SETUP_REQUIRES = _get_requires('setup')
# TEST_SUITE = ''
# TESTS_REQUIRE = []
EXTRAS_REQUIRE = _get_requires('extra')
PYTHON_REQUIRES = ">=2.6,!=3.0,!=3.1,!=3.2"
CMDCLASS = {
    'bdist_egg': BdistEgg,
    'build_locale': BuildLocale,
    'build_node': BuildNode,
    'build_py': BuildPy,
    # 'download_catalog': DownloadCatalog,
    'makereadme': MakeReadme,
    'prebuild': PreBuild,
    'sdist': Sdist
}
MESSAGE_EXTRACTORS = {
    _PACKAGE_PATH: [
        ('**.py', 'python', None),
        ('app/scripts/**.js', 'javascript', None)
    ]
}
ZIP_SAFE = True
CLASSIFIERS = [
    "Development Status :: {0}".format(STATUS),
    "Environment :: Web Environment",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: {0}".format(LICENSE),
    "Natural Language :: English",
    # "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation :: CPython",
    # "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Communications",
    "Topic :: Communications :: File Sharing",
    "Topic :: Internet",
    "Topic :: Internet :: File Transfer Protocol (FTP)",
    "Topic :: Internet :: WWW/HTTP"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    long_description=LONG_DESC,
    keywords=KEYWORDS,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    platforms=PLATFORMS,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    include_package_data=INCLUDE_PACKAGE_DATA,
    namespace_packages=NAMESPACE_PACKAGES,
    install_requires=INSTALL_REQUIRES,
    setup_requires=SETUP_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=PYTHON_REQUIRES,
    cmdclass=CMDCLASS,
    message_extractors=MESSAGE_EXTRACTORS,
    # test_suite=TEST_SUITE,
    # tests_require=TESTS_REQUIRE,
    zip_safe=ZIP_SAFE,
    classifiers=CLASSIFIERS
)
