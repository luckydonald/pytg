# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from setuptools import setup  # Always prefer setuptools over distutils

long_description = """A Python module that connects to a Telegram messenger CLI, allowing to interact with Telegram users or groups.
Report any issues at https://github.com/luckydonald/pytg/issues/"""

setup(
    name='pytg',
    version="0.4.5",
    description='Connect to the Telegram CLI, receive and send Telegram messages.',
    long_description=long_description,
    # The project's main homepage.
    url='https://github.com/luckydonald/pytg',
    # Author details
        author='luckydonald',
        author_email='code@luckydonald.de',
        # Choose your license
        license='GPLv3+',
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 4 - Beta',  # 3 - Alpha, 4 - Beta, 5 - Production/Stable
            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            # 'Programming Language :: Python :: 2',
            # 'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            # 'Programming Language :: Python :: 3',
            # 'Programming Language :: Python :: 3.2',
            # 'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3',
            'Topic :: Communications',
            'Topic :: Communications :: Chat',
            'Topic :: Software Development :: Libraries'
        ],
    # What does your project relate to?
    keywords='telegram cli python message send receive python secure fast answer reply image voice picture location contacts typing multi messanger',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['pytg'],  # find_packages(exclude=['contrib', 'docs', 'tests*']),
    # List run-time dependencies here. These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["DictObject", "luckydonald-utils>=0.17"]
    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    # extras_require = {
    #'dev': ['check-manifest'],
    #'test': ['coverage'],
    #},
    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #'sample': ['package_data.dat'],
    #},
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
)
