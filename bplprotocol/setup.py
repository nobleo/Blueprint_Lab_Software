from distutils.core import setup

setup(
    name='bplprotocol',
    version='0.1dev',
    packages=['bplprotocol'],
    install_requires=['cobs', 'crcmod'],
    long_description=open('README.txt').read(),
)