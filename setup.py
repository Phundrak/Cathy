from setuptools import setup

setup(
    name='cathy',
    version='1.1.5',
    description='Discord chat bot using AIML artificial intelligence.',
    long_description=open('README.rst').read(),
    url='https://github.com/DevDungeon/ChattyCathy',
    author='DevDungeon',
    author_email='nanodano@devdungeon.com',
    license='GPL-3.0',
    packages=['cathy'],
    scripts=[
        'bin/cathy',
        'bin/cathy.bat',
    ],
    package_data={
        'cathy': [
            'std-startup.xml',
            'aiml/custom/*.aiml',
            'aiml/einlant-guide/*.aiml'
        ],
    },
    zip_safe=False,
    install_requires=[
        'docopt',
        'python-aiml',
        'python-slugify',
        'discord.py==0.16.12',
        'requests',
    ],
    python_requires='<3.7',
)
