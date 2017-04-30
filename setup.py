from setuptools import setup

setup (
    name                 = 'beets-userrating',
    author               = 'Michael Alan Dorman',
    author_email         = 'mdorman@jaunder.io',
    description          = "A plugin for managing user's per-track ratings in the music geek's media organizer",
    install_requires     = ['beets >= 1.4.3'],
    license              = 'GLPv3',
    namespace_packages   = ['beetsplug'],
    packages             = ['beetsplug'],
    platforms            = 'ALL',
    url                  = 'https://github.com/mdorman/beets-userrating',
    version              = '0.0.1',
)
